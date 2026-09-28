# Personal Fitness Chatbot – Full MVP Plan

**Project Type:** AI / NLP Module  
**Goal:** Build a practical, educational personal fitness chatbot  
**UI:** Streamlit only  
**Last Updated:** September 2026

---

## 1. Project Overview

### Goal
Create a conversational fitness assistant that can:
- Understand user requests through **Intent Classification**
- Extract key information through **Entity Extraction**
- Maintain basic user context (profile)
- Deliver useful responses for common fitness needs

### Target Features (MVP)
- Generate simple personalised workout plans
- Recommend exercises and explain form
- Answer basic nutrition questions
- Provide motivation and general chat
- Handle out-of-scope / unsafe queries safely

---

## 2. Scope

### In Scope
- Intent Classification (6–8 intents)
- Entity Extraction (exercise, body part, equipment, goal, experience level, etc.)
- Simple user profile system
- Basic workout plan generation
- Exercise information & form tips
- Basic nutrition advice
- Motivation / general conversation
- Clear safety disclaimers and out-of-scope handling

### Out of Scope (Future Work)
- Advanced progressive programming
- Real-time form checking (video/pose estimation)
- Complex medical advice
- Heavy generative LLM fine-tuning
- Mobile app or production deployment

---

## 3. Architecture

```
User Message
     ↓
Preprocessing
     ↓
Intent Classifier          ← Main trained model
     ↓
Entity Extractor           ← Rules + spaCy or small model
     ↓
Dialogue State / User Profile
     ↓
┌─────────────────────┬──────────────────────┐
│  Template Responses │      RAG Pipeline    │
│  (simple cases)     │ (exercise knowledge) │
└─────────────────────┴──────────────────────┘
     ↓
Final Response + Safety Disclaimer
```

---

## 4. Intents

| Intent            | Description                          | Example                              |
|-------------------|--------------------------------------|--------------------------------------|
| `generate_plan`   | Create a workout plan                | "Make me a 3-day beginner plan"     |
| `find_exercise`   | Recommend or get exercise info       | "Best exercises for chest"          |
| `ask_form`        | Technique / how to perform           | "How do I do a proper squat?"       |
| `get_nutrition`   | Basic nutrition advice               | "What should I eat for muscle gain?"|
| `log_progress`    | Log workout or feeling               | "I did 3x10 bench today"            |
| `motivation`      | Encouragement / general chat         | "I'm feeling unmotivated"           |
| `out_of_scope`    | Medical, unrelated, or unsafe        | "I have sharp knee pain"            |

---

## 5. Entities to Extract

- `exercise` (e.g. squat, bench press)
- `body_part` (chest, back, legs, etc.)
- `equipment` (dumbbells, barbell, bodyweight, gym)
- `goal` (lose weight, build muscle, endurance, strength)
- `experience_level` (beginner, intermediate, advanced)
- `duration` / `days` (3 days, 45 minutes)
- `injury` (optional but useful)

---

## 6. Data Plan

### A. Intent Classification Dataset
- Start with Hugging Face dataset: `harshmakwana/fitness-intent` (1,200 examples)
- Expand to approximately 150–250 examples per intent
- Methods: Manual writing + LLM paraphrasing + real-user style examples

### B. Entity Extraction
- Annotate 300–600 sentences (BIO format) **or**
- Start with rule-based + spaCy, then upgrade later

### C. Knowledge Base (for RAG)
- Primary source: [Free Exercise DB](https://github.com/yuhonas/free-exercise-db) (800+ exercises)
- Add 20–40 basic nutrition tips and sample workout templates
- Store as structured JSON or markdown chunks

### D. Synthetic Data (Optional)
- Generate 100–200 multi-turn dialogues for testing

---

## 7. Models to Train (MVP)

| Priority   | Model                    | Base Model                  | Notes                                      |
|------------|--------------------------|-----------------------------|--------------------------------------------|
| **Must**   | Intent Classifier        | `distilbert-base-uncased`  | Core model. Fast to train, strong results |
| **Should** | Entity Extractor (NER)   | DistilBERT or spaCy        | Can start with rules + spaCy              |
| Optional   | Embedding model          | `all-MiniLM-L6-v2`         | Use off-the-shelf first                   |

**Important:** Do **not** fine-tune a large generative LLM for the MVP. Use templates + RAG + free LLM API instead.

---

## 8. Tech Stack

- **Language:** Python 3.10+
- **Core NLP:** Hugging Face Transformers + Datasets
- **NER (easy start):** spaCy
- **RAG:** LangChain or LlamaIndex + Chroma / FAISS
- **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`)
- **LLM (generation):** Free API (Gemini, Groq, OpenRouter, etc.)
- **UI:** Streamlit
- **Storage:** JSON / simple SQLite for user profiles
- **Version Control:** Git + GitHub

---

## 9. Folder Structure (Simple MVP)

```text
fitness-chatbot/
│
├── data/
│   ├── intent/                     # Intent classification data
│   │   ├── train.csv
│   │   ├── val.csv
│   │   └── test.csv
│   │
│   ├── knowledge/                  # Exercise + nutrition knowledge base
│   │   └── exercises.json
│   │
│   └── user_profiles/              # Optional saved profiles
│
├── models/
│   └── intent_classifier/          # Saved DistilBERT model
│
├── src/
│   ├── __init__.py
│   ├── intent_classifier.py        # Load & predict intent
│   ├── entity_extractor.py         # Extract entities
│   ├── dialogue.py                 # User profile + conversation logic
│   ├── rag.py                      # Retrieval + response generation
│   └── utils.py                    # Helpers + safety checks
│
├── app.py                          # Main Streamlit application
│
├── notebooks/                      # Experimentation only
│   ├── train_intent.ipynb
│   └── test_rag.ipynb
│
├── .env                            # API keys (optional)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 10. Implementation Roadmap

### Week 1 – Foundation
- Finalise intents and entities
- Collect and clean intent dataset
- Set up project structure + Git
- Train first Intent Classifier (DistilBERT)
- Evaluate Accuracy and Macro-F1

### Week 2 – Understanding Layer
- Improve intent model with more data
- Build entity extraction (start with rules + spaCy)
- Create simple dialogue state / user profile system
- Implement out-of-scope and safety responses

### Week 3 – Response Generation
- Build knowledge base from exercise dataset
- Implement RAG pipeline
- Create template responses for simple intents
- Connect everything into a working chatbot loop

### Week 4 – Polish & Evaluation
- Multi-turn conversation testing
- Add basic personalisation (inject user profile)
- Full evaluation (metrics + human testing)
- Finalise Streamlit demo
- Write documentation and prepare presentation

---

## 11. Evaluation Plan

### Quantitative Metrics
- Intent Classification: Accuracy, Macro-F1
- Entity Extraction: Entity-level F1
- Retrieval (RAG): Recall@3 / Recall@5

### Qualitative Evaluation
- 20–30 realistic multi-turn test conversations
- Human ratings (Helpfulness, Correctness, Safety) on 1–5 scale
- Check for hallucinations and unsafe advice

### Success Criteria for MVP
- Intent accuracy ≥ 85–90%
- Bot can generate a basic personalised plan
- Handles common exercise questions reasonably well
- Clear and safe behaviour on medical / out-of-scope queries

---

## 12. Deliverables

1. Working Streamlit chatbot demo
2. Trained models (saved locally)
3. Datasets used (with documentation)
4. Clean GitHub repository with README
5. Short technical report covering:
   - Architecture
   - Data process
   - Model training & results
   - Limitations & future improvements
6. Presentation / demo (recommended)

---

## 13. Important Tips

- Start simple → get an end-to-end working version first, then improve.
- Data quality is more important than model size.
- Always include a clear disclaimer that the bot does not replace professional medical advice.
- Keep the user profile very simple (a Python dictionary is enough for MVP).
- Log conversations during testing — they become valuable training data later.
- Focus on 2–3 impressive demo scenarios rather than trying to cover everything.

---

## 14. Next Recommended Steps

1. Create the folder structure above
2. Download and explore the `harshmakwana/fitness-intent` dataset
3. Train the first DistilBERT intent classifier
4. Build a basic Streamlit interface that shows the predicted intent

---

**Good luck with your project!**  
This plan balances educational value, practicality, and demo quality for an NLP module.
