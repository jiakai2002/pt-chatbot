"""Audit intent and NER data for quality, leakage, and annotation errors."""

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.entity_extractor import ENTITY_ALIASES


ALLOWED_LABELS = {name.upper() for name in ENTITY_ALIASES} | {"DURATION", "DAYS", "FOOD", "MEAL_TIME", "FREQUENCY"}


def load_dataset(data_root: Path):
    records = []
    ner_by_text = {}
    for split in ("train", "val", "test"):
        ner_path = data_root / "ner" / f"{split}.jsonl"
        if ner_path.exists():
            with ner_path.open(encoding="utf-8") as file:
                for line in file:
                    item = json.loads(line)
                    ner_by_text.setdefault((split, item["text"]), item.get("entities", []))
        csv_path = data_root / "intent" / f"{split}.csv"
        if not csv_path.exists():
            continue
        with csv_path.open(encoding="utf-8", newline="") as file:
            for row_number, row in enumerate(csv.DictReader(file), start=2):
                records.append({
                    "split": split,
                    "row": row_number,
                    "text": row["text"],
                    "intent": row["intent"],
                    "entities": ner_by_text.get((split, row["text"]), []),
                })
    return records


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def duplicate_report(records):
    exact = []
    by_text = defaultdict(list)
    for record in records:
        by_text[normalise(record["text"])].append(record)
    for key, matches in by_text.items():
        if len(matches) > 1:
            exact.append((key, matches))

    texts = [record["text"] for record in records]
    near = []
    if len(texts) > 1:
        matrix = cosine_similarity(TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5)).fit_transform(texts))
        for left in range(len(records)):
            for right in range(left + 1, len(records)):
                if matrix[left, right] > 0.9 and normalise(texts[left]) != normalise(texts[right]):
                    near.append((matrix[left, right], records[left], records[right]))
    return exact, near


def entity_report(records):
    errors = []
    candidates = Counter()
    for record in records:
        text = record["text"]
        spans = record["entities"]
        valid_spans = []
        for span in spans:
            if len(span) != 3:
                errors.append((record, span, "span must contain start, end, label"))
                continue
            start, end, label = span
            if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end > len(text) or start >= end:
                errors.append((record, span, "invalid character offsets"))
                continue
            if text[start:end].strip() == "":
                errors.append((record, span, "span contains no text"))
            if label not in ALLOWED_LABELS:
                errors.append((record, span, "label is not in allowed schema"))
            valid_spans.append((start, end, label))
        for left, right in zip(sorted(valid_spans), sorted(valid_spans)[1:]):
            if right[0] < left[1]:
                errors.append((record, [left, right], "overlapping entity spans"))

        covered = [(start, end) for start, end, _ in valid_spans]
        lowered = text.lower()
        for entity, aliases in ENTITY_ALIASES.items():
            for variants in aliases.values():
                for variant in variants:
                    for match in re.finditer(r"(?<!\w)" + re.escape(variant) + r"(?!\w)", lowered):
                        if not any(start <= match.start() and end >= match.end() for start, end in covered):
                            candidates[f"{entity.upper()}: {match.group(0)}"] += 1
    return errors, candidates


def ngram_report(records):
    by_intent = defaultdict(list)
    for record in records:
        by_intent[record["intent"]].append(record["text"])
    lines = []
    for intent, texts in sorted(by_intent.items()):
        ngrams = Counter()
        openers = Counter()
        for text in texts:
            tokens = re.findall(r"[a-z0-9']+", text.lower())
            if len(tokens) >= 3:
                openers[" ".join(tokens[:3])] += 1
            ngrams.update(" ".join(tokens[i:i + 3]) for i in range(len(tokens) - 2))
        lines.append(f"- **{intent}** — openers: {openers.most_common(5)}; repeated trigrams: {ngrams.most_common(5)}")
    return lines


def audit_dataset(data_root: Path, title: str):
    records = load_dataset(data_root)
    lines = [f"## {title}", "", f"Data root: `{data_root}`", f"Total rows: **{len(records)}**", ""]
    counts = defaultdict(Counter)
    for record in records:
        counts[record["split"]][record["intent"]] += 1
    lines.append("### Class counts")
    for split in ("train", "val", "test"):
        lines.append(f"- **{split}**: {dict(sorted(counts[split].items()))}")

    exact, near = duplicate_report(records)
    cross_exact = [item for item in exact if len({row["split"] for row in item[1]}) > 1]
    cross_near = [item for item in near if item[1]["split"] != item[2]["split"]]
    lines += ["", "### Duplicate and near-duplicate checks", f"- Exact duplicate groups: **{len(exact)}**", f"- Exact duplicate groups across splits: **{len(cross_exact)}**", f"- TF-IDF cosine > 0.9 near-duplicate pairs: **{len(near)}**", f"- Near-duplicate pairs across splits: **{len(cross_near)}**"]
    for score, left, right in cross_near[:10]:
        lines.append(f"  - `{score:.3f}` `{left['split']}`: {left['text']} / `{right['split']}`: {right['text']}")

    errors, candidates = entity_report(records)
    lines += ["", "### Entity annotation checks", f"- Offset/overlap/schema errors: **{len(errors)}**", f"- Unlabelled lexicon candidates: **{sum(candidates.values())}** occurrences"]
    for candidate, count in candidates.most_common(20):
        lines.append(f"  - `{candidate}`: {count}")
    for record, span, reason in errors[:20]:
        lines.append(f"  - `{record['split']}` row {record['row']}: `{span}` — {reason}")

    lengths = [len(record["text"]) for record in records]
    lines += ["", "### Text length distribution", f"- Characters: min={min(lengths) if lengths else 0}, median={sorted(lengths)[len(lengths)//2] if lengths else 0}, max={max(lengths) if lengths else 0}", f"- Words: min={min(len(record['text'].split()) for record in records) if records else 0}, median={sorted(len(record['text'].split()) for record in records)[len(records)//2] if records else 0}, max={max(len(record['text'].split()) for record in records) if records else 0}", "", "### Repeated openers and trigrams"]
    lines.extend(ngram_report(records))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, default=None, help="Audit one dataset root instead of original plus data_v2")
    parser.add_argument("--output", type=Path, default=ROOT / "data_v2" / "AUDIT.md")
    args = parser.parse_args()
    if args.data_root:
        report = audit_dataset(args.data_root, args.data_root.name)
    else:
        report = "# Dataset Audit\n\n" + audit_dataset(ROOT / "data", "Original data")
        if (ROOT / "data_v2" / "intent").exists():
            report += "\n\n" + audit_dataset(ROOT / "data_v2", "data_v2")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n", encoding="utf-8")
    print(f"Wrote audit report to {args.output}")


if __name__ == "__main__":
    main()
