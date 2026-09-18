from claimchecker.ingestion.fetch_article import extract_article_text

text = extract_article_text("https://www.bbc.co.uk/news")
print(text)