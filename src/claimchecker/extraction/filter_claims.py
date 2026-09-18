"""Filter sentences to identify likely factual claims."""

import spacy

nlp = spacy.load("en_core_web_sm")

# Verbs commonly used to state facts/events (vs. opinion verbs like "believes", "hopes")
FACTUAL_VERBS = {
    "announce", "confirm", "report", "reveal", "disclose", "state",
    "find", "show", "record", "rise", "fall", "increase", "decrease",
    "reach", "hit", "release", "publish", "declare",
}

# spaCy's built-in entity categories worth treating as "checkable" signals
RELEVANT_ENTITY_LABELS = {"PERSON", "ORG", "GPE", "MONEY", "PERCENT", "DATE", "CARDINAL", "QUANTITY"}


def is_likely_claim(sentence) -> bool:
    """Check whether a spaCy sentence looks like a checkable factual claim."""
    has_entity = any(ent.label_ in RELEVANT_ENTITY_LABELS for ent in sentence.ents)
    has_factual_verb = any(
        token.lemma_.lower() in FACTUAL_VERBS for token in sentence if token.pos_ == "VERB"
    )
    has_number = any(token.like_num for token in sentence)
    return has_entity or has_factual_verb or has_number


def extract_claims(text: str) -> list[str]:
    """Extract sentences from article text that look like checkable factual claims."""
    doc = nlp(text)
    claims = []
    for sentence in doc.sents:
        if is_likely_claim(sentence):
            claims.append(sentence.text)
    return claims