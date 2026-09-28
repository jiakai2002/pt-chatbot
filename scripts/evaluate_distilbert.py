"""Evaluate the saved DistilBERT intent classifier."""

import csv
from pathlib import Path

import torch
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from scripts.train_intent_distilbert import IntentDataset, load_csv


ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "intent_classifier" / "distilbert"


def main():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, local_files_only=True)
    model.eval()
    labels = model.config.label2id
    texts, label_names = load_csv(ROOT / "data" / "intent" / "test.csv")
    label_ids = [labels[name] for name in label_names]
    loader = DataLoader(IntentDataset(texts, label_ids, tokenizer), batch_size=8)
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in loader:
            labels_batch = batch.pop("labels")
            predictions = model(**batch).logits.argmax(dim=-1)
            correct += (predictions == labels_batch).sum().item()
            total += len(labels_batch)
    print(f"Test accuracy: {correct / total:.3f}")
    print(f"Test examples: {total}")


if __name__ == "__main__":
    main()
