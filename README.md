# Fitness Chatbot

Personal fitness chatbot MVP built with Python and Streamlit.

## Project structure

- `app.py` — Streamlit entry point
- `src/` — intent classification, entity extraction, dialogue, and utilities
- `data/` — datasets, knowledge-base content, and optional user profiles
- `models/` — locally saved trained models
- `notebooks/` — experiments and evaluation

See [plan.md](plan.md) for the complete MVP plan.

## Getting started

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The chatbot is educational and does not replace professional medical advice.

## Train the local intent model

```bash
python scripts/train_intent.py
```

This trains a local TF-IDF and logistic regression classifier and saves it under `models/intent_classifier/`.

Fine-tune the local DistilBERT intent classifier with:

```bash
python scripts/train_intent_distilbert.py
python -m scripts.evaluate_distilbert
```

The chatbot prefers the saved DistilBERT model and falls back to the classical classifier if it is unavailable.

The training data includes the downloaded Hugging Face dataset. To repeat the import:

```bash
python scripts/import_fitness_dataset.py
```

Check entity extraction with:

```bash
python -m scripts.test_entities
```

Run chatbot smoke tests with:

```bash
python -m scripts.test_chatbot
```
