"""Streamlit frontend for the claim verification pipeline."""

import streamlit as st

from claimchecker.ingestion.fetch_article import extract_article_text, ArticleFetchError
from claimchecker.extraction.filter_claims import extract_claims
from claimchecker.retrieval.search_evidence import search_evidence, EvidenceSearchError
from claimchecker.verification.verify_claim import verify_claim

st.set_page_config(page_title="Claim Checker", page_icon="🔍")
st.title("🔍 News Claim Checker")
st.write("Paste a news article URL to extract and verify its factual claims.")

url = st.text_input("Article URL")

if st.button("Check Article") and url:
    with st.spinner("Fetching article..."):
        try:
            text = extract_article_text(url)
        except ArticleFetchError as e:
            st.error(f"Could not fetch article: {e}")
            st.stop()

    claims = extract_claims(text)
    st.success(f"Found {len(claims)} claims.")

    for i, claim in enumerate(claims, start=1):
        st.subheader(f"Claim {i}")
        st.write(claim)

        try:
            evidence_list = search_evidence(claim, source_url=url, max_results=2)
        except EvidenceSearchError:
            evidence_list = []

        if not evidence_list:
            st.caption("No evidence found.")
            continue

        for evidence in evidence_list:
            verdict = verify_claim(claim, evidence["description"] or evidence["title"])
            label = verdict["label"]
            confidence = verdict["confidence"]

            color = {"ENTAILMENT": "green", "CONTRADICTION": "red", "NEUTRAL": "gray"}[label]
            st.markdown(f":{color}[**{label}**] ({confidence:.0%}) — {evidence['title']}")