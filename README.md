# Personal Fitness Chatbot

An offline, educational fitness chatbot built with Python and Streamlit. The project demonstrates a complete NLP pipeline for understanding common fitness requests, extracting useful details, retrieving exercise information, and producing safe, structured responses.

The chatbot is intended for general education only. It does not diagnose injuries or replace advice from a qualified fitness or healthcare professional.

## Features

- Intent classification for workout plans, exercise recommendations, exercise form, nutrition, progress logging, motivation, and out-of-scope queries.
- Rule-based entity extraction using spaCy's EntityRuler and regular expressions.
- Extraction of exercises, body parts, equipment, goals, experience level, duration, sets, repetitions, and injury indicators.
- Simple in-session user profile for goals, experience level, equipment, training days, and session duration.
- Local exercise knowledge base stored in JSON.
- Deterministic offline exercise retrieval.
- Template-based responses for predictable and controllable output.
- Safety response for pain and injury-related queries.
- Streamlit chat interface.
- TF-IDF/logistic regression fallback model when DistilBERT is unavailable.

## Architecture

```text
User message
     |
     v
Text preprocessing
     |
     v
Intent classification  <--- DistilBERT or TF-IDF/logistic regression
     |
     v
Entity extraction     <--- spaCy EntityRuler + regular expressions
     |
     v
Dialogue state and user profile
     |
     +--------------------+
     |                    |
     v                    v
Exercise retrieval   Response templates
     |                    |
     +---------+----------+
               v
       Safety-aware response
```

The application uses local models and local data at runtime. No external generative API is required.

## Project structure

```text
.
├── app.py                         # Streamlit application
├── data/
│   ├── intent/                    # Intent datasets and source information
│   ├── knowledge/                 # Exercise knowledge base
│   └── user_profiles/             # Reserved for saved profiles
├── models/
│   └── intent_classifier/         # Local model outputs; ignored by Git
├── notebooks/                     # Training experiment notebook
├── scripts/
│   ├── import_fitness_dataset.py  # Import and merge intent data
│   ├── train_intent.py            # Train classical baseline
│   ├── train_intent_distilbert.py # Fine-tune DistilBERT
│   ├── evaluate_distilbert.py     # Evaluate saved DistilBERT model
│   ├── test_entities.py           # Entity extraction checks
│   ├── test_rag.py                # Retrieval checks
│   └── test_chatbot.py            # End-to-end smoke tests
├── src/
│   ├── intent_classifier.py       # Model loading and intent prediction
│   ├── entity_extractor.py        # Entity extraction
│   ├── dialogue.py                # Profile updates and response selection
│   ├── rag.py                     # Local exercise retrieval
│   ├── response_templates.py      # Deterministic response templates
│   └── utils.py                   # Local data helpers
├── requirements.txt
└── README.md
```

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Running the chatbot

Start the Streamlit interface:

```powershell
streamlit run app.py
```

The application loads the saved DistilBERT model when it is available. If it is not available, it falls back to the saved classical classifier and then to keyword matching.

## Data and model preparation

The repository contains the intent CSV files and the local exercise knowledge base. To import the available fitness-intent Parquet data into the training data, run:

```powershell
python scripts/import_fitness_dataset.py
```

Train the TF-IDF/logistic regression baseline:

```powershell
python scripts/train_intent.py
```

Fine-tune the DistilBERT classifier:

```powershell
python scripts/train_intent_distilbert.py
```

The DistilBERT training script uses `distilbert-base-uncased`, trains for three epochs, and saves the tokenizer and model under `models/intent_classifier/distilbert/`.

Evaluate the saved DistilBERT model:

```powershell
python -m scripts.evaluate_distilbert
```

The trained model files are intentionally excluded from Git through `.gitignore`. This keeps the repository lightweight and avoids committing the approximately 268 MB local model artefacts.

## Testing

```powershell
python -m scripts.test_entities
python -m scripts.test_rag
python -m scripts.test_chatbot
python -m compileall -q app.py src scripts
```

These checks cover entity extraction, exercise retrieval, chatbot intent handling, profile updates, response generation, safety behaviour, and Python compilation.

## Example interactions

The chatbot is designed to handle messages such as:

- `Make me a 3-day beginner plan`
- `How do I perform a squat?`
- `What exercises are good for my chest?`
- `What should I eat for muscle gain?`
- `I completed 3 sets of bench press today`
- `I feel unmotivated`
- `I have sharp knee pain`

For `Make me a 3-day beginner dumbbell plan`, the system can identify:

```text
Intent: generate_plan
Days: 3
Experience level: beginner
Equipment: dumbbells
```

## Safety and limitations

- The chatbot provides general educational information only.
- It does not diagnose pain, injuries, or medical conditions.
- Users are advised to stop exercising when they experience sharp pain and consult a qualified professional.
- The current exercise knowledge base is intentionally small and can be expanded.
- Entity extraction is primarily rule-based, so unfamiliar wording may not be recognised.
- Template responses improve predictability but limit conversational flexibility.
- The local intent dataset and test set are limited, so additional data and human evaluation are needed before making stronger performance claims.
- User profiles currently exist only in the active Streamlit session and are not persisted between runs.

## Future improvements

- Expand and rebalance the intent dataset.
- Add more exercises, equipment types, and nutrition content.
- Train or fine-tune a dedicated named entity recognition model.
- Add richer retrieval with embeddings and semantic similarity.
- Improve multi-turn dialogue and profile persistence.
- Add macro-F1, confusion matrices, entity-level F1, and retrieval Recall@k reporting.
- Conduct structured human evaluation for helpfulness, correctness, clarity, and safety.

## Licence and source information

The intent data source and attribution information are documented in `data/intent/SOURCES.md`. Check the terms of any external dataset or exercise data before redistributing the project.
