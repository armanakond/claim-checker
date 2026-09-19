"""FastAPI application wiring together the full claim-checking pipeline."""

from fastapi import FastAPI, HTTPException

from claimchecker.ingestion.fetch_article import extract_article_text, ArticleFetchError
from claimchecker.extraction.filter_claims import extract_claims
from claimchecker.retrieval.search_evidence import search_evidence, EvidenceSearchError
from claimchecker.verification.verify_claim import verify_claim
from claimchecker.api.schemas import CheckArticleRequest, CheckArticleResponse, ClaimResult

app = FastAPI(title="Claim Checker API")


@app.post("/check-article", response_model=CheckArticleResponse)
def check_article(request: CheckArticleRequest) -> CheckArticleResponse:
    """Fetch an article, extract claims, and verify each against retrieved evidence."""
    try:
        text = extract_article_text(request.url)
    except ArticleFetchError as e:
        raise HTTPException(status_code=422, detail=str(e))

    claims = extract_claims(text)
    results = []

    for claim in claims:
        verdicts = []
        try:
            evidence_list = search_evidence(claim, source_url=request.url, max_results=2)
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

    return CheckArticleResponse(url=request.url, claims=results)