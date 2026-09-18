import spacy


nlp = spacy.load("en_core_web_sm") #loads the pre-trained language model for English


def split_into_sentences(text: str) -> list[str]:
    """Split a block of article text into a list of individual sentences."""
    doc = nlp(text)
    sentences = []
    for sentence in doc.sents:
        sentences.append(sentence.text)
    return sentences
