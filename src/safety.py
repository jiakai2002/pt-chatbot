"""Safety and routing rules for unsupported or medical requests."""

from __future__ import annotations

import re

MEDICAL_TERMS = (
    "injury", "injured", "pain", "hurts", "hurt", "medication", "medicine",
    "diagnose", "diagnosis", "symptom", "swelling", "fracture", "sprain",
    "prescription", "disease", "doctor",
)
OUT_OF_SCOPE_TERMS = ("politics", "joan of arc", "weather", "stock market")

MEDICAL_RESPONSE = (
    "I can’t provide medical advice or diagnose injuries. "
    "Please consult a qualified healthcare professional."
)
OUT_OF_SCOPE_RESPONSE = (
    "I can help with fitness, exercise, nutrition facts and workout logging. "
    "Please ask a fitness-related question."
)


def contains_term(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.casefold()
    return any(re.search(rf"\b{re.escape(term)}\b", lowered) for term in terms)


def safety_route(text: str) -> str | None:
    if contains_term(text, MEDICAL_TERMS):
        return "medical"
    if contains_term(text, OUT_OF_SCOPE_TERMS):
        return "out_of_scope"
    return None

