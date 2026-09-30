"""Simple deterministic workout-plan generation."""

from __future__ import annotations

from typing import Any

from src.knowledge_base import KnowledgeBase


def build_three_day_plan(
    knowledge_base: KnowledgeBase,
    level: str = "beginner",
    equipment: str | None = None,
    body_part: str | None = None,
) -> list[dict[str, Any]]:
    """Create a three-day full-body plan from local exercises."""

    pool = knowledge_base.find_exercises(
        body_part=body_part,
        equipment=equipment,
        level=level,
        limit=24,
    )
    if len(pool) < 6:
        pool = knowledge_base.find_exercises(equipment=equipment, level=level, limit=24)
    if len(pool) < 6:
        pool = knowledge_base.find_exercises(limit=24)

    selected = []
    seen_muscles: set[str] = set()
    for item in pool:
        muscles = set(item.get("primary_muscles", []))
        if muscles - seen_muscles or len(selected) < 6:
            selected.append(item)
            seen_muscles.update(muscles)
        if len(selected) == 9:
            break

    # Repeat only when the local database has fewer than nine suitable
    # records. This keeps the UI useful with small test fixtures while still
    # preferring distinct exercises for the normal dataset.
    if selected and len(selected) < 9:
        selected = (selected * ((9 + len(selected) - 1) // len(selected)))[:9]

    days = []
    for index in range(3):
        exercises = selected[index * 3 : (index + 1) * 3]
        days.append(
            {
                "day": index + 1,
                "exercises": [
                    {
                        "name": item.get("name"),
                        "sets": 3 if level == "beginner" else 4,
                        "repetitions": "8-12",
                        "rest": "60-90 seconds",
                    }
                    for item in exercises
                ],
            }
        )
    return days
