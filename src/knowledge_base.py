"""Local exercise and nutrition knowledge-base access."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.config import PROCESSED_DATA_DIR


def _tokens(text: str) -> set[str]:
    # Keep a compact normalized form so queries such as ``push-ups`` match
    # records that use ``push up`` (or vice versa).
    tokens = re.findall(r"[a-z0-9]+", text.casefold())
    return {token[:-1] if len(token) > 3 and token.endswith("s") else token for token in tokens}


class KnowledgeBase:
    def __init__(self, data_dir: Path = PROCESSED_DATA_DIR):
        self.data_dir = Path(data_dir)
        self.exercises = self._load_json("exercises.json")
        self.nutrition = self._load_json("nutrition.json")

    def _load_json(self, filename: str) -> list[dict[str, Any]]:
        path = self.data_dir / filename
        if not path.exists():
            return []
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, list) else []

    def find_exercises(
        self,
        exercise: str | None = None,
        body_part: str | None = None,
        equipment: str | None = None,
        level: str | None = None,
        limit: int = 8,
    ) -> list[dict[str, Any]]:
        limit = max(0, int(limit))
        query_tokens = _tokens(exercise or "")
        requested_equipment = _tokens(equipment or "")
        scored: list[tuple[int, dict[str, Any]]] = []
        for item in self.exercises:
            name = str(item.get("name", ""))
            searchable = _tokens(
                " ".join(
                    [
                        name,
                        str(item.get("equipment", "")),
                        " ".join(item.get("primary_muscles", [])),
                        " ".join(item.get("secondary_muscles", [])),
                    ]
                )
            )
            score = len(query_tokens & searchable) if query_tokens else 0
            name_tokens = _tokens(name)
            if exercise:
                name_overlap = len(query_tokens & name_tokens)
                if not name_overlap or name_overlap / len(query_tokens) < 0.5:
                    continue
            muscles = {str(value).casefold() for value in item.get("primary_muscles", [])}
            muscles.update(str(value).casefold() for value in item.get("secondary_muscles", []))
            if body_part and not (_tokens(body_part) & muscles):
                continue
            item_equipment = str(item.get("equipment") or "bodyweight").casefold()
            normalized_item_equipment = _tokens(item_equipment)
            if equipment and requested_equipment.isdisjoint(normalized_item_equipment) and equipment.casefold() != "bodyweight":
                continue
            if equipment and equipment.casefold() == "bodyweight" and item_equipment not in {"body only", "bodyweight", "none"}:
                continue
            if level and str(item.get("level", "")).casefold() not in {level.casefold(), ""}:
                continue
            score += len(query_tokens & name_tokens) * 3
            scored.append((score, item))
        scored.sort(key=lambda pair: (-pair[0], str(pair[1].get("name", ""))))
        return [item for _, item in scored[:limit]]

    def search_food(self, query: str, limit: int = 6) -> list[dict[str, Any]]:
        limit = max(0, int(limit))
        query_tokens = _tokens(query)
        if not query_tokens:
            return []
        matches: list[tuple[int, dict[str, Any]]] = []
        for item in self.nutrition:
            description = str(item.get("description", ""))
            description_tokens = _tokens(description)
            score = len(query_tokens & description_tokens)
            first_word = re.search(r"[a-z0-9]+", description.casefold())
            if first_word and _tokens(first_word.group(0)) & query_tokens:
                score += 2
            if query.casefold().strip() in description.casefold():
                score += len(query_tokens) * 2
            if score:
                matches.append((score, item))
        matches.sort(key=lambda pair: (-pair[0], len(str(pair[1].get("description", "")))))
        return [item for _, item in matches[:limit]]
