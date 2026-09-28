"""Quick checks for the rule-based entity extractor."""

from src.entity_extractor import extract_entities


def main():
    examples = [
        ("Make a 3-day beginner dumbbell plan", {"days": 3, "experience_level": "beginner", "equipment": "dumbbells"}),
        ("I did 3 sets 10 reps of pushups", {"exercise": "push-up", "sets": 3, "reps": 10}),
        ("Give me a 45 minute chest workout", {"duration": "45 minutes", "body_part": "chest"}),
        ("I have sharp knee pain", {"injury": True}),
    ]

    for message, expected in examples:
        actual = extract_entities(message)
        for key, value in expected.items():
            assert actual.get(key) == value, f"{message!r}: expected {key}={value!r}, got {actual}"
    print(f"Passed {len(examples)} entity extraction checks.")


if __name__ == "__main__":
    main()
