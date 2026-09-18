from claimchecker.extraction.filter_claims import extract_claims


def test_filters_out_opinion_keeps_facts():
    text = (
        "The Bank of England announced interest rates would rise to 5%. "
        "Critics said the decision was disappointing."
    )
    claims = extract_claims(text)
    assert len(claims) == 1
    assert "Bank of England" in claims[0]