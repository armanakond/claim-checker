"""Request and response data shapes for the API."""

from pydantic import BaseModel, HttpUrl


class CheckArticleRequest(BaseModel):
    """Incoming request: a URL to fact-check."""
    url: HttpUrl


class ClaimResult(BaseModel):
    """Result for a single claim: the claim text and its verification verdicts."""
    claim: str
    verdicts: list[dict]


class CheckArticleResponse(BaseModel):
    """Full response: all claims found and their verification results."""
    url: str
    claims: list[ClaimResult]