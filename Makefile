.PHONY: run lint

run:
	streamlit run synthesizer_app.py

lint:
	pre-commit run --all-files
