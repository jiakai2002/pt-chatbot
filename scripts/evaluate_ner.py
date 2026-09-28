"""Evaluate the saved custom spaCy NER model."""

import json
from pathlib import Path

import spacy
from spacy.training import Example


ROOT = Path(__file__).resolve().parent.parent
MODEL = ROOT / "models" / "ner" / "fitness_ner"
TEST = ROOT / "data" / "ner" / "test.jsonl"


def main():
    nlp = spacy.load(MODEL)
    examples = []
    with TEST.open(encoding="utf-8") as file:
        for line in file:
            item = json.loads(line)
            examples.append(Example.from_dict(nlp.make_doc(item["text"]), {"entities": item["entities"]}))
    scores = nlp.evaluate(examples)
    print(f"Entity precision: {scores['ents_p']:.3f}")
    print(f"Entity recall: {scores['ents_r']:.3f}")
    print(f"Entity F1: {scores['ents_f']:.3f}")
    print(f"Test examples: {len(examples)}")


if __name__ == "__main__":
    main()
