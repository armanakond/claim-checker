from claimchecker.verification.verify_claim import verify_claim


def test_supporting_evidence_gives_entailment():
    claim = "The company's profits increased last year."
    evidence = "The company reported a significant rise in annual profits."
    result = verify_claim(claim, evidence)
    assert result["label"] == "ENTAILMENT"