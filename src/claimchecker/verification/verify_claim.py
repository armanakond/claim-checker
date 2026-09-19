"""Verify a claim against a piece of evidence using an NLI model."""

from transformers import pipeline

nli_model = pipeline("text-classification", model="roberta-large-mnli")


def verify_claim(claim: str, evidence: str) -> dict:
    """Check whether evidence supports, refutes, or is unrelated to a claim."""
    input_text = f"{evidence} </s></s> {claim}"
    result = nli_model(input_text)[0]

    return {
        "label": result["label"],
        "confidence": result["score"],
    }