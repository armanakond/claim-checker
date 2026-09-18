import pytest
from claimchecker.ingestion.fetch_article import extract_article_text, ArticleFetchError

def test_extract_real_article():
    text = extract_article_text("https://www.bbc.co.uk/news")
    print(text[:500])  # Print the first 500 characters of the extracted text 
    assert len(text) > 100

def test_nonexistent_domain_raises_error():
    with pytest.raises(ArticleFetchError):
        extract_article_text("https://this-domain-does-not-exist-xyz123.com")

def test_404_page_raises_error():
    with pytest.raises(ArticleFetchError):
        extract_article_text("https://www.bbc.co.uk/this-page-does-not-exist-404")