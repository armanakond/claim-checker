"""Fetch and extract clean article text from a URL."""

import trafilatura
from tenacity import retry, stop_after_attempt, wait_exponential


class ArticleFetchError(Exception):
    """Raised when an article cannot be fetched or has no extractable content."""


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
)
def fetch_html(url: str) -> str:
    """Download raw HTML for a URL, retrying on transient failures."""
    downloaded = trafilatura.fetch_url(url)
    if downloaded is None:
        raise ArticleFetchError(f"Could not download content from: {url}")
    return downloaded


def extract_article_text(url: str) -> str:
    """Fetch a URL and return its clean, extracted article text."""
    html = fetch_html(url)
    text = trafilatura.extract(html)
    if not text:
        raise ArticleFetchError(f"No extractable article text found at: {url}")
    return text