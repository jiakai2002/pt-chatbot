"""Train and evaluate the local intent classifier."""

import csv
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.pipeline import Pipeline


ROOT = Path(__file__).resolve().parent.parent


def load_csv(path: Path):
    with path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    return [row["text"] for row in rows], [row["intent"] for row in rows]


def main():
    train_x, train_y = load_csv(ROOT / "data" / "intent" / "train.csv")
    val_x, val_y = load_csv(ROOT / "data" / "intent" / "val.csv")
    test_x, test_y = load_csv(ROOT / "data" / "intent" / "test.csv")

    model = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2))),
        ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
    ])
    model.fit(train_x, train_y)

    for name, texts, labels in [("Validation", val_x, val_y), ("Test", test_x, test_y)]:
        predictions = model.predict(texts)
        print(f"{name} accuracy: {accuracy_score(labels, predictions):.3f}")
        print(f"{name} macro-F1: {f1_score(labels, predictions, average='macro'):.3f}")
        if name == "Test":
            print(classification_report(labels, predictions, zero_division=0))

    output = ROOT / "models" / "intent_classifier" / "model.joblib"
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output)
    print(f"Saved model to {output}")


if __name__ == "__main__":
    main()
