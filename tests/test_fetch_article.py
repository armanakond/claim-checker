from claimchecker.ingestion.fetch_article import extract_article_text

def test_extract_real_article():
    text = extract_article_text("https://www.bbc.co.uk/news")
    assert len(text) > 100