"""Create weakly labelled spaCy NER data from the fitness intent CSV files.

The generated labels are a starting point and should be manually reviewed
before being treated as a gold-standard NER dataset.
"""

import csv
import json
import re
from pathlib import Path

from src.entity_extractor import ENTITY_ALIASES


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "ner"


def _add_span(spans, text, start, end, label):
    if any(start < other_end and end > other_start for other_start, other_end, _ in spans):
        return
    spans.append((start, end, label))


def label_text(text: str) -> dict:
    lowered = text.lower()
    candidates = []
    for entity, aliases in ENTITY_ALIASES.items():
        for variants in aliases.values():
            for variant in variants:
                for match in re.finditer(r"(?<!\w)" + re.escape(variant) + r"(?!\w)", lowered):
                    candidates.append((match.start(), match.end(), entity.upper()))

    spans = []
    for start, end, label in sorted(candidates, key=lambda item: (-(item[1] - item[0]), item[0])):
        _add_span(spans, text, start, end, label)

    for match in re.finditer(r"\b[1-7][- ]*(?:day|days)\b", lowered):
        _add_span(spans, text, match.start(), match.end(), "DAYS")
    for match in re.finditer(r"\b\d+\s*(?:minute|minutes|min)\b", lowered):
        _add_span(spans, text, match.start(), match.end(), "DURATION")

    spans.sort()
    return {"text": text, "entities": [[start, end, label] for start, end, label in spans]}


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for split in ("train", "val", "test"):
        source = ROOT / "data" / "intent" / f"{split}.csv"
        rows = list(csv.DictReader(source.open(encoding="utf-8", newline="")))
        target = OUTPUT / f"{split}.jsonl"
        with target.open("w", encoding="utf-8") as file:
            for row in rows:
                file.write(json.dumps(label_text(row["text"]), ensure_ascii=False) + "\n")
        print(f"{split}: {len(rows)} labelled sentences -> {target}")


if __name__ == "__main__":
    main()
