"""Search for news evidence related to a claim."""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"


class EvidenceSearchError(Exception):
    """Raised when evidence search fails."""


def search_evidence(claim: str, max_results: int = 5) -> list[dict]:
    """Search for news articles related to a claim, returning title/url/description."""
    if not NEWS_API_KEY:
        raise EvidenceSearchError("NEWS_API_KEY is not set in the environment.")

    params = {
        "q": claim,
        "apiKey": NEWS_API_KEY,
        "pageSize": max_results,
        "language": "en",
        "sortBy": "relevancy",
    }

    response = requests.get(NEWS_API_URL, params=params, timeout=10)

    if response.status_code != 200:
        raise EvidenceSearchError(
            f"NewsAPI request failed with status {response.status_code}: {response.text}"
        )

    data = response.json()
    articles = data.get("articles", [])

    return [
        {
            "title": article["title"],
            "url": article["url"],
            "description": article.get("description", ""),
        }
        for article in articles
    ]