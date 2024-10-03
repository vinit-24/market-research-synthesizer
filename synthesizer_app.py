import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Market Research Synthesizer", page_icon="📰")

st.title("📰 Market Research Synthesizer")

question = st.text_input("Business question", placeholder="e.g. What's new in the European cosmetics market?")

if st.button("Generate summary") and question:
    with st.spinner("Crunching numbers and reading reports..."):
        # TODO: Load PDFs, create embeddings, query with LangChain
        # For now, show a stub response
        st.subheader("Executive summary")
        st.write("""
        • European cosmetics grew 5% YoY in 2023, driven by premium skincare.  
        • Gen‑Z consumers favour clinically‑backed claims; 'derm‑beauty' searches +72%.  
        • Sephora’s loyalty revamp captured +1.2 M new members.  
        """)
        st.subheader("Key metrics")
        st.metric("Market size", "€89 B", "▲ 5% vs 2022")
        st.metric("Online share", "26 %", "▲ 2 pp")
        st.info("PDF citation: Cosmetics Europe Market Report 2024")
        st.download_button("Download slide deck (coming soon)", data=b"", file_name="cosmetics_summary.pptx", disabled=True)
else:
    st.info("Enter a question above and hit *Generate summary*")
