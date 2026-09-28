"""Fine-tune DistilBERT locally for intent classification."""

import csv
from pathlib import Path

import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer


ROOT = Path(__file__).resolve().parent.parent
BASE_MODEL = "distilbert-base-uncased"
OUTPUT = ROOT / "models" / "intent_classifier" / "distilbert"


class IntentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=128)
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        item = {key: torch.tensor(value[index]) for key, value in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[index])
        return item


def load_csv(path):
    with path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    return [row["text"] for row in rows], [row["intent"] for row in rows]


def evaluate(model, loader, device):
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for batch in loader:
            batch = {key: value.to(device) for key, value in batch.items()}
            predictions = model(**batch).logits.argmax(dim=-1)
            correct += (predictions == batch["labels"]).sum().item()
            total += len(batch["labels"])
    return correct / total if total else 0.0


def main():
    torch.manual_seed(42)
    train_texts, train_labels_text = load_csv(ROOT / "data" / "intent" / "train.csv")
    val_texts, val_labels_text = load_csv(ROOT / "data" / "intent" / "val.csv")
    labels = sorted(set(train_labels_text))
    label_to_id = {label: index for index, label in enumerate(labels)}
    train_labels = [label_to_id[label] for label in train_labels_text]
    val_labels = [label_to_id[label] for label in val_labels_text]

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL,
        num_labels=len(labels),
        id2label={index: label for label, index in label_to_id.items()},
        label2id=label_to_id,
    )
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    train_loader = DataLoader(IntentDataset(train_texts, train_labels, tokenizer), batch_size=8, shuffle=True)
    val_loader = DataLoader(IntentDataset(val_texts, val_labels, tokenizer), batch_size=8)
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

    for epoch in range(3):
        model.train()
        total_loss = 0.0
        for batch in train_loader:
            batch = {key: value.to(device) for key, value in batch.items()}
            optimizer.zero_grad()
            loss = model(**batch).loss
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch + 1}/3 loss: {total_loss / len(train_loader):.4f} validation accuracy: {evaluate(model, val_loader, device):.3f}")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(OUTPUT)
    tokenizer.save_pretrained(OUTPUT)
    print(f"Saved DistilBERT model to {OUTPUT}")


if __name__ == "__main__":
    main()
