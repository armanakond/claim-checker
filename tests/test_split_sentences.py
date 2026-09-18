from claimchecker.extraction.split_sentences import split_into_sentences


def test_splits_multiple_sentences():
    text = "The economy grew by 2% last quarter. Analysts were surprised by the figures."
    result = split_into_sentences(text)
    assert len(result) == 2
    assert result[0] == "The economy grew by 2% last quarter."