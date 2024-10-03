# Market Research Synthesizer

Ask a plain–English business question such as **“What’s going on in the European cosmetics market?”**  
and get back:

* A concise bullet‑point executive summary  
* Key metrics and citations pulled from industry PDFs / articles  
* An auto‑generated mini slide deck (optional export)

Built with **LangChain**, **OpenAI GPT‑4o**, and **Streamlit**.

> **Original build:** Sep–Oct 2024 – converted to open‑source for my portfolio in 2025.

---

## Quick start

```bash
# 1. Create and activate a virtual environment
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run synthesizer_app.py
```

The first load will index PDFs from `data/raw/`.  
Set your `OPENAI_API_KEY` in the environment or a `.env` file before launch.

---

## Project structure

```
.
├── synthesizer_app.py   # Streamlit UI + LangChain pipeline
├── requirements.txt
├── data/
│   └── raw/             # Drop your PDF or HTML sources here
├── notebooks/
│   └── 01_e2e_demo.ipynb
└── tests/
    └── test_pipeline.py
```

## License

[MIT](LICENSE) – free to use with attribution.
