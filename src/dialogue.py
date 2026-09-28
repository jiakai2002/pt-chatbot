"""Manage profile state and select task-oriented response templates."""

from src.response_templates import (
    clarification_response,
    exercise_response,
    motivation_response,
    nutrition_response,
    plan_response,
    progress_response,
    safety_response,
)
from src.rag import retrieve_exercises


DEFAULT_PROFILE = {
    "goal": None,
    "experience_level": None,
    "equipment": None,
    "days": None,
    "duration": None,
}


def new_profile() -> dict:
    return DEFAULT_PROFILE.copy()


def update_profile(profile: dict, entities: dict) -> dict:
    for field in DEFAULT_PROFILE:
        if field in entities:
            profile[field] = entities[field]
    return profile


def profile_text(profile: dict) -> str:
    values = [f"{key}: {value}" for key, value in profile.items() if value]
    return ", ".join(values) if values else "No preferences saved yet."


def build_response(intent: str, entities: dict, profile: dict, exercises: list[dict]) -> str:
    """Select and fill a fixed response template; no text generation is used."""
    if intent == "out_of_scope":
        return safety_response()
    if intent == "motivation":
        return motivation_response()
    if intent == "log_progress":
        return progress_response()
    if intent == "get_nutrition":
        return nutrition_response()
    if intent == "generate_plan":
        return plan_response(profile)

    requested = entities.get("exercise") or entities.get("body_part")
    if requested:
        matches = retrieve_exercises(requested, exercises, limit=1)
        if matches:
            return exercise_response(matches[0], intent == "ask_form")

    return clarification_response(intent == "ask_form")
