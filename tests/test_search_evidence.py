from claimchecker.retrieval.search_evidence import search_evidence


def test_search_returns_results():
    results = search_evidence("Bank of England interest rates")
    assert len(results) > 0
    assert "title" in results[0]
    assert "url" in results[0]