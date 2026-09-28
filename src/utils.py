"""Small local-data helpers for the offline chatbot."""

import json
from pathlib import Path


def load_exercises() -> list[dict]:
    path = Path(__file__).resolve().parent.parent / "data" / "knowledge" / "exercises.json"
    with path.open(encoding="utf-8") as file:
        return json.load(file)
