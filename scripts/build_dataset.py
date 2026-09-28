"""Build the task-2 data_v2 copy without changing the original data.

This stage only applies the intent-schema change and copies the existing
entity annotations. Augmentation and new leakage-safe splitting are added in
later dataset-building stages.
"""

import csv
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data"
OUTPUT = ROOT / "data_v2"
SPLITS = ("train", "val", "test")

MEDICAL_RE = re.compile(
    r"\b(?:pain|sore|hurt|injur\w*|diagnos\w*|medic\w*|symptom\w*|fractur\w*|"
    r"swoll\w*|torn|dislocat\w*|numb\w*|dizz\w*|prescrib\w*|illness\w*|"
    r"doctor|medical|treatment|clearance|condition|surgery|broken|painkill\w*)\b",
    re.IGNORECASE,
)


def relabel_intent(text: str, intent: str) -> tuple[str, str]:
    """Return (new intent, review reason); empty reason means no review."""
    if intent != "out_of_scope":
        return intent, ""
    if MEDICAL_RE.search(text):
        return "medical_or_injury", ""
    return "out_of_scope", ""


def main():
    (OUTPUT / "intent").mkdir(parents=True, exist_ok=True)
    (OUTPUT / "ner").mkdir(parents=True, exist_ok=True)
    (OUTPUT / "lexicons").mkdir(parents=True, exist_ok=True)

    review_rows = []
    for split in SPLITS:
        source_path = SOURCE / "intent" / f"{split}.csv"
        with source_path.open(encoding="utf-8", newline="") as file:
            rows = list(csv.DictReader(file))
        target_path = OUTPUT / "intent" / f"{split}.csv"
        with target_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["text", "intent", "secondary_intent"])
            writer.writeheader()
            for row in rows:
                intent, reason = relabel_intent(row["text"], row["intent"])
                writer.writerow({"text": row["text"], "intent": intent, "secondary_intent": ""})
                if reason:
                    review_rows.append({"split": split, "text": row["text"], "original_intent": row["intent"], "suggested_intent": intent, "reason": reason})

        shutil.copy2(SOURCE / "ner" / f"{split}.jsonl", OUTPUT / "ner" / f"{split}.jsonl")

    with (OUTPUT / "relabel_review.csv").open("w", encoding="utf-8", newline="") as file:
        fields = ["split", "text", "original_intent", "suggested_intent", "reason"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(review_rows)

    sources = SOURCE / "intent" / "SOURCES.md"
    (OUTPUT / "SOURCES.md").write_text(
        sources.read_text(encoding="utf-8")
        + "\n\n## data_v2 processing\n\n"
        + "data_v2 is a relabelled copy of the original data. Existing source rows and wording are preserved; no synthetic augmentation has been added at this stage. The original files under data/ remain unchanged.\n",
        encoding="utf-8",
    )
    print(f"Built {OUTPUT} from the original data.")
    print(f"Rows requiring manual review: {len(review_rows)}")


if __name__ == "__main__":
    main()
