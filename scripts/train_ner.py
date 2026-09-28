"""Train the custom fitness spaCy NER model."""

import json
import random
from pathlib import Path

import spacy
from spacy.training import Example
from spacy.util import fix_random_seed


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "ner"
OUTPUT = ROOT / "models" / "ner" / "fitness_ner"


def load_examples(nlp, path):
    examples = []
    with path.open(encoding="utf-8") as file:
        for line in file:
            item = json.loads(line)
            examples.append(Example.from_dict(nlp.make_doc(item["text"]), {"entities": item["entities"]}))
    return examples


def main():
    fix_random_seed(42)
    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")
    train_examples = load_examples(nlp, DATA / "train.jsonl")
    val_examples = load_examples(nlp, DATA / "val.jsonl")
    labels = sorted({label for example in train_examples for label in example.reference.ents for label in [label.label_]})
    for label in labels:
        ner.add_label(label)

    optimizer = nlp.initialize(get_examples=lambda: train_examples)
    for epoch in range(30):
        random.shuffle(train_examples)
        losses = {}
        batches = spacy.util.minibatch(train_examples, size=8)
        for batch in batches:
            nlp.update(batch, sgd=optimizer, drop=0.25, losses=losses)
        if (epoch + 1) % 10 == 0:
            scores = nlp.evaluate(val_examples)
            print(f"Epoch {epoch + 1}/30 loss={losses.get('ner', 0.0):.3f} validation F1={scores['ents_f']:.3f}")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    nlp.to_disk(OUTPUT)
    print(f"Saved custom NER model to {OUTPUT}")


if __name__ == "__main__":
    main()
