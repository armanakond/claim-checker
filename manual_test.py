from claimchecker.ingestion.fetch_article import extract_article_text
from claimchecker.extraction.filter_claims import extract_claims
from claimchecker.retrieval.search_evidence import search_evidence
from claimchecker.verification.verify_claim import verify_claim

url = "https://www.bbc.co.uk/news/articles/c2dwg9n8gw7o"

text = extract_article_text(url)
claims = extract_claims(text)

print(f"Found {len(claims)} claims.\n")

for i, claim in enumerate(claims, start=1):
    print(f"Claim {i}: {claim}")
    evidence_list = search_evidence(claim, max_results=2)

    if not evidence_list:
        print("  No evidence found.\n")
        continue

    for e in evidence_list:
        result = verify_claim(claim, e["description"] or e["title"])
        print(f"  Evidence: {e['title']}")
        print(f"    -> {result['label']} (confidence: {result['confidence']:.2f})")
    print()