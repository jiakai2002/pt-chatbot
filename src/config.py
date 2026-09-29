"""Shared project paths and constants."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DATA_DIR = ROOT_DIR / "data" / "processed"
MODEL_DIR = ROOT_DIR / "models" / "intent_classifier"

INTENT_LABELS = (
    "generate_plan",
    "find_exercise",
    "get_nutrition_info",
    "log_feeling",
    "general_chat",
    "out_of_scope",
)

TEXT_COLUMNS = ("text", "utterance", "sentence", "query", "input")
LABEL_COLUMNS = ("label", "intent", "category")

