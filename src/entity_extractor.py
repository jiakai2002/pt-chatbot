"""spaCy EntityRuler plus simple rules for normalized fitness entities."""

import re

try:
    import spacy
except (ImportError, OSError):
    spacy = None


ENTITY_ALIASES = {
    "exercise": {
        "squat": ["squat", "squats"], "push-up": ["push-up", "pushup", "push ups", "push-ups"],
        "bench press": ["bench press", "bench"], "deadlift": ["deadlift", "deadlifts"],
        "lunge": ["lunge", "lunges"], "plank": ["plank", "planks"],
        "row": ["row", "rows"], "shoulder press": ["shoulder press", "shoulder presses"],
    },
    "body_part": {
        "chest": ["chest", "pecs"], "back": ["back"], "legs": ["leg", "legs"],
        "shoulders": ["shoulder", "shoulders"], "arms": ["arm", "arms", "biceps", "triceps"],
        "core": ["core", "abs", "abdominals"], "glutes": ["glute", "glutes"],
    },
    "equipment": {
        "dumbbells": ["dumbbell", "dumbbells"], "barbell": ["barbell", "barbells"],
        "kettlebell": ["kettlebell", "kettlebells"], "resistance band": ["resistance band", "bands"],
        "bodyweight": ["bodyweight", "no equipment", "without equipment"], "gym": ["gym"],
    },
    "goal": {
        "build muscle": ["build muscle", "muscle gain", "gain muscle", "hypertrophy"],
        "lose weight": ["lose weight", "weight loss", "fat loss"], "strength": ["strength", "get stronger"],
        "endurance": ["endurance", "stamina"], "general fitness": ["fitness", "get fit", "healthy"],
    },
    "experience_level": {
        "beginner": ["beginner", "new to training", "new to exercise"],
        "intermediate": ["intermediate"], "advanced": ["advanced", "experienced"],
    },
}


def _build_nlp():
    if spacy is None:
        return None
    nlp = spacy.blank("en")
    ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})
    patterns = []
    for entity, aliases in ENTITY_ALIASES.items():
        for normalized, variants in aliases.items():
            for variant in variants:
                patterns.append({"label": entity.upper(), "pattern": variant, "id": normalized})
    ruler.add_patterns(patterns)
    return nlp


NLP = _build_nlp()


def _rule_entities(text: str) -> dict:
    entities = {}
    for entity, aliases in ENTITY_ALIASES.items():
        for normalized, variants in aliases.items():
            if any(variant in text for variant in variants):
                entities[entity] = normalized
                break
    return entities


def extract_entities(message: str) -> dict:
    text = message.lower().strip()
    entities = _rule_entities(text)
    if NLP is not None:
        doc = NLP(text)
        for ent in doc.ents:
            entities[ent.label_.lower()] = ent.ent_id_ or ent.text

    days = re.search(r"\b([1-7])[- ]*(?:day|days)\b", text)
    if days:
        entities["days"] = int(days.group(1))
    duration = re.search(r"\b(\d+)\s*(?:minute|minutes|min)\b", text)
    if duration:
        entities["duration"] = f"{duration.group(1)} minutes"
    sets_reps = re.search(r"\b(\d+)\s*(?:sets?\s*(?:x\s*)?|x\s*)(\d+)\s*(?:reps?|repetitions?)\b", text)
    shorthand = re.search(r"\b(\d+)\s*x\s*(\d+)\b", text)
    match = sets_reps or shorthand
    if match:
        entities["sets"] = int(match.group(1))
        entities["reps"] = int(match.group(2))
    if any(word in text for word in ["pain", "injury", "injured", "hurt"]):
        entities["injury"] = True
    return entities
