from claimchecker.ingestion.fetch_article import extract_article_text
from claimchecker.extraction.filter_claims import extract_claims
from claimchecker.retrieval.search_evidence import search_evidence

url = "https://www.bbc.co.uk/news/articles/cm0463619r1no"

text = extract_article_text(url)
claims = extract_claims(text)

print(f"Found {len(claims)} claims.\n")

for i, claim in enumerate(claims, start=1):
    print(f"Claim {i}: {claim}")
    evidence = search_evidence(claim, max_results=3)
    print(f"  Found {len(evidence)} related articles:")
    for e in evidence:
        print(f"   - {e['title']} ({e['url']})")
    print()