"""Build a concise search query from a claim, using key entities and terms."""

import spacy

nlp = spacy.load("en_core_web_sm")


def build_search_query(claim: str, max_terms: int = 8) -> str:
    """Extract key entities/nouns from a claim to form a short, search-friendly query."""
    doc = nlp(claim)

    key_terms = []

    # Prioritise named entities (people, orgs, places, numbers)
    for ent in doc.ents:
        key_terms.append(ent.text)

    # Add important nouns not already captured as part of an entity
    entity_words = {token.text for ent in doc.ents for token in ent}
    for token in doc:
        if token.pos_ in ("NOUN", "PROPN") and token.text not in entity_words:
            key_terms.append(token.text)

    # Deduplicate while preserving order, then cap the length
    seen = set()
    unique_terms = []
    for term in key_terms:
        if term.lower() not in seen:
            seen.add(term.lower())
            unique_terms.append(term)

    return " ".join(unique_terms[:max_terms])