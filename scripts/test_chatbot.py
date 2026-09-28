"""Smoke tests for the offline chatbot behavior."""

from src.dialogue import build_response, new_profile, update_profile
from src.entity_extractor import extract_entities
from src.intent_classifier import classify_intent
from src.utils import load_exercises


def main():
    cases = {
        "Make me a 3-day beginner plan": "generate_plan",
        "How do I perform a squat?": "ask_form",
        "What should I eat for muscle gain?": "get_nutrition",
        "I feel unmotivated": "motivation",
        "I have sharp knee pain": "out_of_scope",
    }
    for message, expected in cases.items():
        actual = classify_intent(message)
        assert actual == expected, f"{message!r}: expected {expected}, got {actual}"

    profile = new_profile()
    entities = extract_entities("Make me a 3-day beginner dumbbell plan")
    update_profile(profile, entities)
    response = build_response("generate_plan", entities, profile, load_exercises())
    assert "3-day" in response
    assert "beginner" in response

    safety = build_response("out_of_scope", {"injury": True}, profile, load_exercises())
    assert "medical" in safety or "pain" in safety
    print("Passed chatbot intent, profile, response, and safety checks.")


if __name__ == "__main__":
    main()
