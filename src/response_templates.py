"""Deterministic response templates for the task-oriented chatbot."""


def safety_response() -> str:
    return "I can help with general fitness and nutrition. I cannot diagnose pain or injuries. Stop exercising if you feel sharp pain and consult a qualified professional."


def motivation_response() -> str:
    return "Keep it small today: choose one exercise and do one easy set. Consistency matters more than perfection."


def progress_response() -> str:
    return "Nice work. Your progress is worth tracking. Tell me the exercise, sets, repetitions, or weight if you want to record more detail."


def nutrition_response() -> str:
    return "For general fitness, build meals around protein, vegetables or fruit, carbohydrates for training energy, and water. For medical or highly specific nutrition advice, consult a registered professional."


def plan_response(profile: dict) -> str:
    days = profile.get("days") or 3
    level = profile.get("experience_level") or "beginner"
    equipment = profile.get("equipment") or "bodyweight"
    sessions = [
        "Day 1: Squats, push-ups, and plank — 2 to 3 easy sets.",
        "Day 2: Rest or light walking.",
        "Day 3: Lunges, rows, and glute bridges — 2 to 3 easy sets.",
    ]
    return f"Here is a simple {days}-day {level} plan using {equipment}:\n\n" + "\n".join(sessions[:days]) + "\n\nStart comfortably and stop if you feel sharp pain."


def exercise_response(exercise: dict, form_request: bool) -> str:
    steps = "\n".join(f"{index}. {step}" for index, step in enumerate(exercise["steps"], 1))
    if form_request:
        return f"{exercise['name']} form:\n\n{steps}\n\nCommon mistake: {exercise['common_mistake']}"
    return f"Try {exercise['name']} for your {exercise.get('body_part', 'fitness')} goal.\n\nForm basics:\n{steps}"


def clarification_response(form_request: bool) -> str:
    if form_request:
        return "Tell me the exercise name, such as squat, push-up, or plank, and I will give basic form guidance."
    return "Tell me a body part, exercise, goal, or experience level so I can give a more specific suggestion."
