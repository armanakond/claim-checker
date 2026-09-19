"""FastAPI application wiring together the full claim-checking pipeline."""

from fastapi import FastAPI, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from claimchecker.ingestion.fetch_article import extract_article_text, ArticleFetchError
from claimchecker.extraction.filter_claims import extract_claims
from claimchecker.retrieval.search_evidence import search_evidence, EvidenceSearchError
from claimchecker.verification.verify_claim import verify_claim
from claimchecker.api.schemas import CheckArticleRequest, CheckArticleResponse, ClaimResult

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Claim Checker API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.post("/check-article", response_model=CheckArticleResponse)
@limiter.limit("5/minute")
def check_article(request: Request, body: CheckArticleRequest) -> CheckArticleResponse:
    """Fetch an article, extract claims, and verify each against retrieved evidence."""
    article_url = str(body.url)

    try:
        text = extract_article_text(article_url)
    except ArticleFetchError as e:
        raise HTTPException(status_code=422, detail=str(e))

    claims = extract_claims(text)
    results = []

    for claim in claims:
        verdicts = []
        try:
            evidence_list = search_evidence(claim, source_url=article_url, max_results=2)
        except EvidenceSearchError:
            evidence_list = []

        for evidence in evidence_list:
            verdict = verify_claim(claim, evidence["description"] or evidence["title"])
            verdicts.append({
                "source": evidence["title"],
                "url": evidence["url"],
                "label": verdict["label"],
                "confidence": verdict["confidence"],
            })

        results.append(ClaimResult(claim=claim, verdicts=verdicts))

    return CheckArticleResponse(url=article_url, claims=results)