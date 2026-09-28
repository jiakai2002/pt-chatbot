"""Local intent classifier with a trained-model and rule-based fallback."""

from pathlib import Path

import joblib


INTENT_KEYWORDS = {
    "out_of_scope": ["sharp pain", "injury", "injured", "medical", "diagnosis"],
    "generate_plan": ["workout plan", "training plan", "routine", "program", "plan"],
    "ask_form": ["how do i do", "how to perform", "proper form", "technique", "form"],
    "get_nutrition": ["nutrition", "what should i eat", "protein", "calories", "diet"],
    "find_exercise": ["exercise", "exercises", "workout for", "best for", "recommend"],
    "log_progress": ["i did", "i completed", "log", "finished", "today's workout"],
    "motivation": ["motivation", "motivated", "unmotivated", "encouragement", "hello", "hi"],
}

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "intent_classifier" / "model.joblib"
DISTILBERT_PATH = Path(__file__).resolve().parent.parent / "models" / "intent_classifier" / "distilbert"
_model = None
_distilbert = None


def _load_model():
    global _model
    if _model is None and MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    return _model


def _load_distilbert():
    global _distilbert
    if _distilbert is None and (DISTILBERT_PATH / "config.json").exists():
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(DISTILBERT_PATH, local_files_only=True)
        model = AutoModelForSequenceClassification.from_pretrained(DISTILBERT_PATH, local_files_only=True)
        model.eval()
        _distilbert = (tokenizer, model, torch)
    return _distilbert


def classify_intent(message: str) -> str:
    """Predict an intent locally, falling back to keywords if no model exists."""
    text = message.lower().strip()
    safety_terms = ["sharp pain", "severe pain", "injury", "injured", "diagnose", "diagnosis", "broken bone", "medicine for pain"]
    if any(term in text for term in safety_terms):
        return "out_of_scope"

    distilbert = _load_distilbert()
    if distilbert is not None:
        tokenizer, model, torch = distilbert
        inputs = tokenizer(message, return_tensors="pt", truncation=True, max_length=128)
        with torch.no_grad():
            prediction = model(**inputs).logits.argmax(dim=-1).item()
        return str(model.config.id2label[prediction])

    model = _load_model()
    if model is not None:
        return str(model.predict([message])[0])

    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return intent

    return "out_of_scope"
