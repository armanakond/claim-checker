from unittest.mock import patch, MagicMock

from claimchecker.retrieval.search_evidence import search_evidence


@patch("claimchecker.retrieval.search_evidence.requests.get")
def test_search_returns_results(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "articles": [
            {"title": "Bank raises rates", "url": "https://example.com/1", "description": "Rates went up."}
        ]
    }
    mock_get.return_value = mock_response

    results = search_evidence("Bank of England interest rates")

    assert len(results) == 1
    assert results[0]["title"] == "Bank raises rates"