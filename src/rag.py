"""Small deterministic retriever for the local exercise knowledge base.

This keeps the MVP fully offline while giving the dialogue layer a single
place to retrieve relevant exercise records.
"""


def retrieve_exercises(query: str, exercises: list[dict], limit: int = 3) -> list[dict]:
    """Return the best matching exercises for an exercise/body-part query."""
    if not query or limit <= 0:
        return []

    terms = {term for term in query.lower().split() if term}
    scored = []
    for index, exercise in enumerate(exercises):
        name = str(exercise.get("name", "")).lower()
        body_part = str(exercise.get("body_part", "")).lower()
        score = 0
        if query.lower() in name:
            score += 3
        if query.lower() in body_part:
            score += 2
        score += len(terms & set(name.split()))
        score += len(terms & set(body_part.split()))
        if score:
            scored.append((score, index, exercise))

    scored.sort(key=lambda item: (-item[0], item[1]))
    return [exercise for _, _, exercise in scored[:limit]]
