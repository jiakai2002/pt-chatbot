"""Merge the downloaded Hugging Face fitness-intent data into training data."""

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "intent" / "fitness-intent.parquet"
TARGET = ROOT / "data" / "intent" / "train.csv"
LABEL_MAP = {
    "general_chat": "motivation",
    "generate_plan": "generate_plan",
    "get_nutrition_info": "get_nutrition",
    "log_feeling": "log_progress",
    "out_of_scope": "out_of_scope",
    "find_exercise": "find_exercise",
}


def main():
    external = pd.read_parquet(SOURCE)
    external["intent"] = external["intent"].map(LABEL_MAP)
    external = external.dropna(subset=["intent"])[["text", "intent"]]

    with TARGET.open(encoding="utf-8", newline="") as file:
        existing = list(csv.DictReader(file))
    existing_keys = {(row["text"].strip().lower(), row["intent"]) for row in existing}

    added = []
    for row in external.to_dict("records"):
        key = (row["text"].strip().lower(), row["intent"])
        if key not in existing_keys:
            added.append({"text": row["text"].strip(), "intent": row["intent"]})
            existing_keys.add(key)

    rows = existing + added
    with TARGET.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "intent"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Added {len(added)} examples from the Hugging Face dataset.")
    for intent in sorted(LABEL_MAP.values()):
        print(f"{intent}: {sum(row['intent'] == intent for row in rows)}")


if __name__ == "__main__":
    main()
