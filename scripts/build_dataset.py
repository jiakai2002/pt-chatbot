"""Build the reproducible data_v2 dataset for tasks 2–4.

Original files under data/ are never modified. This stage relabels the
existing examples, adds deterministic template data, and recomputes entity
spans from versioned lexicons.
"""

import csv
import json
import random
import re
import shutil
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data"
OUTPUT = ROOT / "data_v2"
SPLITS = ("train", "val", "test")
INTENTS = (
    "generate_plan", "find_exercise", "ask_form", "get_nutrition",
    "log_progress", "motivation", "medical_or_injury", "out_of_scope",
)
SEED = 42

MEDICAL_RE = re.compile(
    r"\b(?:pain|sore|hurt|injur\w*|diagnos\w*|medic\w*|symptom\w*|fractur\w*|"
    r"swoll\w*|torn|dislocat\w*|numb\w*|dizz\w*|prescrib\w*|illness\w*|"
    r"doctor|medical|treatment|clearance|condition|surgery|broken|painkill\w*)\b",
    re.IGNORECASE,
)

LEXICONS = {
    "EXERCISE": [
        "squat", "squats", "push-up", "pushups", "push ups", "push-ups", "plank", "planks",
        "lunge", "lunges", "deadlift", "deadlifts", "bench press", "bench", "overhead press",
        "shoulder press", "pull-up", "pullup", "pull ups", "row", "rows", "bicep curl", "bicep curls",
        "curl", "curls", "tricep dip", "tricep dips", "dips", "hip thrust", "hip thrusts",
        "glute bridge", "glute bridges", "calf raise", "calf raises", "burpee", "burpees",
        "mountain climber", "mountain climbers", "leg press", "leg curl", "chest fly", "step-up", "step ups",
    ],
    "BODY_PART": [
        "chest", "pecs", "back", "legs", "leg", "shoulder", "shoulders", "arms", "arm", "biceps",
        "triceps", "core", "abs", "abdominals", "glutes", "glute", "hamstrings", "hamstring",
        "quadriceps", "quads", "calves", "calf", "forearms", "lower back", "upper back",
    ],
    "GOAL": [
        "build muscle", "muscle gain", "gain muscle", "hypertrophy", "lose weight", "weight loss",
        "fat loss", "cut", "cutting", "strength", "get stronger", "endurance", "stamina",
        "general fitness", "fitness", "get fit", "healthy", "bulk", "bulking", "conditioning",
    ],
    "EQUIPMENT": [
        "dumbbell", "dumbbells", "barbell", "barbells", "kettlebell", "kettlebells", "resistance band",
        "resistance bands", "bands", "bodyweight", "no equipment", "without equipment", "home", "gym",
        "cable machine", "cables", "bench", "pull-up bar", "yoga mat",
    ],
    "EXPERIENCE_LEVEL": ["beginner", "beginners", "new to training", "new to exercise", "intermediate", "advanced", "experienced"],
    "FOOD": [
        "oats", "oatmeal", "eggs", "chicken", "salmon", "tuna", "tofu", "beans", "lentils", "rice",
        "potatoes", "sweet potato", "greek yogurt", "yogurt", "cottage cheese", "banana", "berries",
        "spinach", "vegetables", "fruit", "whole grain bread", "peanut butter", "nuts", "protein shake",
    ],
    "MEAL_TIME": ["breakfast", "lunch", "dinner", "snack", "pre-workout", "post-workout", "rest day", "before training", "after training"],
    "DAYS": ["1 day", "2 days", "3 days", "4 days", "5 days", "one day", "two days", "three days", "four days", "five days", "three days a week", "Monday and Wednesday", "Monday Wednesday Friday"],
    "DURATION": ["15 minutes", "20 minutes", "30 minutes", "45 minutes", "an hour", "half an hour"],
}

SLOTS = {
    "exercise": ["squat", "deadlift", "bench press", "overhead press", "pull-up", "row", "bicep curl", "tricep dip", "hip thrust", "glute bridge", "calf raise", "burpee"],
    "body": ["chest", "back", "legs", "hamstrings", "shoulders", "arms", "core", "glutes", "calves", "quads"],
    "equipment": ["dumbbells", "a barbell", "a kettlebell", "resistance bands", "bodyweight", "no equipment", "home equipment", "a gym", "a pull-up bar", "a yoga mat"],
    "goal": ["build muscle", "lose weight", "get stronger", "improve endurance", "general fitness", "bulk", "cut", "conditioning"],
    "level": ["beginner", "intermediate", "advanced", "someone new to training"],
    "days": ["2 days", "3 days", "4 days", "5 days", "Monday and Wednesday", "Monday Wednesday Friday", "three days a week"],
    "duration": ["15 minutes", "20 minutes", "30 minutes", "45 minutes", "an hour", "half an hour"],
    "food": ["oats", "eggs", "chicken", "tofu", "rice", "salmon", "Greek yogurt", "a banana", "beans", "a protein shake"],
    "meal": ["breakfast", "lunch", "dinner", "a snack", "pre-workout", "post-workout", "a rest day"],
    "topic": ["a laptop for school", "a history topic", "the Cold War", "a homework question", "a photography project", "a car problem", "a recipe", "a puppy", "an account security issue", "a maths problem", "a movie", "a travel plan"],
}

OPENERS = {
    "generate_plan": ["could you map out", "im looking for", "help me build", "need a", "plan out", "what would a", "put together", "id like", "can we create", "design a", "make", "build", "write", "set up", "give me", "looking for", "coach me through", "im trying to start", "gym bro question i need", "got time for a", "can u make", "pls make", "my week needs", "please map", "could i get", "thinking about a", "schedule a", "how about a", "i want", "help me plan", "can someone create", "show me a"],
    "find_exercise": ["which moves target", "what can i use for", "show me options for", "im after exercises for", "what works my", "point me to moves for", "give me ideas for", "what should i try for", "recommend movements for", "any good exercises for", "how can i train my", "what hits my", "can you list moves for", "need exercises for", "gym bro what trains", "what are good moves for", "help me find work for", "which exercises help", "id like options for", "what can i do for", "name some exercises for", "suggest moves for", "got anything for", "which lifts work", "what should i use to train", "can u recommend", "pls suggest", "im looking for moves for", "give me a few for", "what are my options for", "help with exercises for", "which move is good for"],
    "ask_form": ["how do i perform", "what is the form for", "can you explain", "show me how to do", "how should i do", "whats the safest way to do", "walk me through", "how do you do", "i need help with", "form check for", "what are the cues for", "how can i improve", "what does good form look like for", "could you teach me", "tell me how to perform", "how am i meant to do", "can u explain", "pls show me", "im confused about", "what should i focus on for", "how do i set up", "how should my form look for", "can someone explain", "technique tips for", "how is this exercise done", "what is a good setup for", "help me learn", "how do i correctly do", "what mistakes happen in", "how do i nail", "explain the setup for", "what cues help with"],
    "get_nutrition": ["what should i eat for", "give me food ideas for", "how can i fuel", "what meals help with", "im trying to eat for", "which foods support", "what are good foods for", "tell me about eating for", "can you suggest meals for", "what macros suit", "how much protein for", "meal ideas for", "what would you eat for", "help me plan food for", "is this good nutrition for", "what should my diet look like for", "gym bro what do i eat for", "what foods are useful for", "can u give meal ideas for", "pls suggest food for", "how should i fuel", "what can i have for", "what works as a meal for", "any food tips for", "im unsure what to eat for", "what snacks help with", "what should i prep for", "help with meals for", "which food supports", "what do i eat when trying to", "what is a good meal for", "can you help with nutrition for"],
    "log_progress": ["i completed", "i finished", "log this", "record that i did", "just did", "my workout was", "i managed", "i got through", "please note", "save my", "i hit", "i achieved", "mark down", "i trained", "my session included", "i lifted", "i ran", "i walked", "i knocked out", "i got my", "finished a", "done with", "just completed", "for my record i did", "today i did", "yesterday i did", "this morning i did", "last night i did", "no time word i did", "gym bro log", "quick log", "record my", "can you track"],
    "motivation": ["i feel", "help me", "give me", "motivate me", "i need encouragement", "im struggling", "can you keep me", "i want to stay", "how do i stay", "im losing", "say something to", "i need a push", "fitness is hard and", "i keep", "im not feeling", "could you encourage", "please motivate", "why cant i", "starting again and", "gym bro i need", "can u hype me", "pls encourage", "i need help staying", "what can keep me", "im tempted to skip", "help me get", "i want consistency", "how can i restart", "i need support", "my motivation is", "im finding it hard", "give me a reason"],
    "medical_or_injury": ["my", "i have", "should i train with", "can you diagnose", "what do i do about", "is it safe with", "i feel", "im experiencing", "could this be", "do i need clearance for", "what medicine for", "my doctor said", "after an injury", "pain started in", "i am worried about", "can i exercise with", "what treatment for", "help with my", "is this symptom", "i hurt my", "my joint is", "i have a medical", "should i ignore", "gym bro my", "can u help with my", "pls diagnose", "sore after", "numb during", "dizzy while", "what is wrong with", "do these symptoms", "is this concerning"],
    "out_of_scope": ["tell me about", "what is", "how do i", "can you help with", "who was", "which one is", "explain", "i need help with", "what should i buy", "recommend a", "is it possible to", "show me how to", "can you solve", "why did", "give me facts about", "what happened in", "where can i", "which laptop", "help with my homework", "gym bro unrelated question", "can u tell me", "pls explain", "i wonder", "what are the rules for", "how can i hack", "what is the best", "who wrote", "how does", "could you answer", "off topic question", "not fitness but", "random question"],
}


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def relabel_intent(text: str, intent: str) -> str:
    if intent == "out_of_scope" and MEDICAL_RE.search(text):
        return "medical_or_injury"
    return intent


def read_original_rows():
    hf_path = SOURCE / "intent" / "fitness-intent.parquet"
    hf_texts = set()
    try:
        import pandas as pd
        hf_texts = {normalise(value) for value in pd.read_parquet(hf_path)["text"].astype(str)}
    except Exception:
        pass
    all_rows = {}
    for split in SPLITS:
        with (SOURCE / "intent" / f"{split}.csv").open(encoding="utf-8", newline="") as file:
            rows = list(csv.DictReader(file))
        with (SOURCE / "ner" / f"{split}.jsonl").open(encoding="utf-8") as file:
            ner_rows = [json.loads(line) for line in file]
        output = []
        for row, ner in zip(rows, ner_rows):
            output.append({
                "text": row["text"],
                "intent": relabel_intent(row["text"], row["intent"]),
                "secondary_intent": "",
                "source": "hf" if normalise(row["text"]) in hf_texts else "original",
                "manual_entities": ner.get("entities", []),
            })
        all_rows[split] = output
    return all_rows


def write_lexicons():
    lexicon_dir = OUTPUT / "lexicons"
    lexicon_dir.mkdir(parents=True, exist_ok=True)
    for label, values in LEXICONS.items():
        (lexicon_dir / f"{label.lower()}.txt").write_text("\n".join(sorted(set(values))) + "\n", encoding="utf-8")


def regex_spans(text):
    lowered = text.lower()
    spans = []
    day_name = r"(?:mon|monday|tue|tues|tuesday|wed|wednesday|thu|thurs|thursday|fri|friday|sat|saturday|sun|sunday)"
    patterns = {
        "DAYS": rf"\b(?:[1-7]|one|two|three|four|five|six|seven)[- ]*(?:day|days)(?:\s+a\s+week|\s+per\s+week|\s+weekly)?\b|\b{day_name}(?:\s+(?:and\s+)?{day_name})+\b|\b{day_name}(?:\s*[/,&-]\s*{day_name})+\b",
        "DURATION": r"\b(?:\d+\s*(?:minute|minutes|min|hour|hours|hr|hrs)|half an hour|an hour)\b",
    }
    for label, pattern in patterns.items():
        spans.extend((match.start(), match.end(), label) for match in re.finditer(pattern, lowered))
    return spans


def lexicon_spans(text):
    lowered = text.lower()
    spans = []
    for label, values in LEXICONS.items():
        for value in values:
            pattern = r"(?<!\w)" + re.escape(value.lower()) + r"(?!\w)"
            spans.extend((match.start(), match.end(), label) for match in re.finditer(pattern, lowered))
    return sorted(spans, key=lambda span: (-(span[1] - span[0]), span[0], span[2]))


def annotate(text, manual, conflicts, row_id):
    candidates = [(int(start), int(end), str(label)) for start, end, label in manual]
    candidates.extend(lexicon_spans(text))
    candidates.extend(regex_spans(text))
    selected = []
    for candidate in sorted(candidates, key=lambda span: (-(span[1] - span[0]), span[0], span[2])):
        start, end, label = candidate
        if start < 0 or end > len(text) or start >= end:
            conflicts.append({"row": row_id, "text": text, "existing": "", "candidate": str(candidate), "reason": "invalid candidate span"})
            continue
        overlaps = [span for span in selected if span[0] < end and start < span[1]]
        if not overlaps:
            selected.append(candidate)
            continue
        if any(span == candidate for span in overlaps):
            continue
        winner = max(overlaps + [candidate], key=lambda span: span[1] - span[0])
        conflicts.append({"row": row_id, "text": text, "existing": json.dumps(overlaps), "candidate": json.dumps(candidate), "reason": f"overlap; longest span kept: {winner}"})
        if winner == candidate:
            selected = [span for span in selected if span not in overlaps]
            selected.append(candidate)
    return sorted(set(selected))


def add_noise(text, index):
    mode = index % 5
    if mode == 0:
        return re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())
    if mode == 1:
        for old, new in (("workout", "workuot"), ("exercise", "exersize"), ("recommend", "recomend"), ("routine", "routne"), ("nutrition", "nutriton")):
            if old in text.lower():
                return re.sub(old, new, text, count=1, flags=re.IGNORECASE)
    if mode == 2:
        return text.lower()
    if mode == 3:
        return text.replace("please", "pls").replace("can you", "can u").replace("repetitions", "reps").replace("workout", "wo")
    if mode == 4:
        return text + " I am not sure where to start and would appreciate a simple answer that fits my week."
    return text


def short_message(intent, slots):
    short = {
        "generate_plan": ["plan please", f"{slots['days']} plan", "beginner routine"],
        "find_exercise": [f"{slots['body']}?", "leg exercises", "chest moves"],
        "ask_form": [f"{slots['exercise']} form", "squat technique", "form help"],
        "get_nutrition": ["meal ideas", "protein foods", "post workout meal"],
        "log_progress": [f"did {slots['exercise']}", "finished workout", "log my sets"],
        "motivation": ["motivate me", "need a push", "feeling stuck"],
        "medical_or_injury": ["knee pain", "injury question", "feel dizzy"],
        "out_of_scope": ["homework help", "random trivia", "buy a laptop"],
    }
    return short[intent]


def generate_text(intent, index):
    opener_index = index % len(OPENERS[intent])
    slot_index = index // len(OPENERS[intent])
    exercise = SLOTS["exercise"][slot_index % len(SLOTS["exercise"])]
    body = SLOTS["body"][slot_index % len(SLOTS["body"])]
    equipment = SLOTS["equipment"][slot_index % len(SLOTS["equipment"])]
    goal = SLOTS["goal"][slot_index % len(SLOTS["goal"])]
    level = SLOTS["level"][slot_index % len(SLOTS["level"])]
    days = SLOTS["days"][slot_index % len(SLOTS["days"])]
    duration = SLOTS["duration"][slot_index % len(SLOTS["duration"])]
    food = SLOTS["food"][slot_index % len(SLOTS["food"])]
    meal = SLOTS["meal"][slot_index % len(SLOTS["meal"])]
    topic = SLOTS["topic"][slot_index % len(SLOTS["topic"])]
    opener = OPENERS[intent][opener_index]
    slots = locals()
    if index % 10 == 0:
        return random.Random(SEED + index).choice(short_message(intent, slots))
    templates = {
        "generate_plan": f"{opener} a {days} {level} {equipment} workout plan for {goal}",
        "find_exercise": f"{opener} {body} using {equipment}",
        "ask_form": f"{opener} {exercise} and tell me the main form cues",
        "get_nutrition": f"{opener} {goal} at {meal}; would {food} work and what should I eat after training",
        "log_progress": f"{opener} {exercise}: 3 sets of 10 reps with {equipment} and a 30 minute session",
        "motivation": f"{opener} {goal}; I keep skipping sessions and need a realistic way to begin",
        "medical_or_injury": f"{opener} knee pain after {exercise}; should I keep training or seek medical advice",
        "out_of_scope": f"{opener} {topic}",
    }
    return add_noise(templates[intent], index)


def secondary_for(intent, index):
    if index % 10 != 5:
        return ""
    return {
        "generate_plan": "ask_form", "find_exercise": "ask_form", "ask_form": "find_exercise",
        "get_nutrition": "generate_plan", "log_progress": "motivation", "motivation": "generate_plan",
        "medical_or_injury": "ask_form", "out_of_scope": "motivation",
    }[intent]


def build_augmented(intent, count, seen, start_index, source):
    rows = []
    index = start_index
    while len(rows) < count:
        text = generate_text(intent, index)
        key = normalise(text)
        if key not in seen:
            seen.add(key)
            rows.append({"text": text, "intent": intent, "secondary_intent": secondary_for(intent, index), "source": source, "manual_entities": []})
        index += 1
    return rows


def main():
    random.seed(SEED)
    (OUTPUT / "intent").mkdir(parents=True, exist_ok=True)
    (OUTPUT / "ner").mkdir(parents=True, exist_ok=True)
    write_lexicons()
    rows_by_split = read_original_rows()
    seen = {normalise(row["text"]) for rows in rows_by_split.values() for row in rows}

    # Task 3 target: 150 new training rows per intent. Additional validation
    # and test rows supply enough entity coverage for task 4.
    for intent in INTENTS:
        rows_by_split["train"].extend(build_augmented(intent, 150, seen, 1000 + INTENTS.index(intent) * 1000, "augmented_template"))
        rows_by_split["val"].extend(build_augmented(intent, 25, seen, 20000 + INTENTS.index(intent) * 1000, "augmented_template"))
        rows_by_split["test"].extend(build_augmented(intent, 25, seen, 30000 + INTENTS.index(intent) * 1000, "augmented_template"))

    conflicts = []
    review_rows = []
    for split in SPLITS:
        csv_path = OUTPUT / "intent" / f"{split}.csv"
        ner_path = OUTPUT / "ner" / f"{split}.jsonl"
        with csv_path.open("w", encoding="utf-8", newline="") as csv_file, ner_path.open("w", encoding="utf-8") as ner_file:
            writer = csv.DictWriter(csv_file, fieldnames=["text", "intent", "secondary_intent", "source"])
            writer.writeheader()
            for row_index, row in enumerate(rows_by_split[split], start=2):
                entities = annotate(row["text"], row["manual_entities"], conflicts, f"{split}:{row_index}")
                writer.writerow({key: row[key] for key in ("text", "intent", "secondary_intent", "source")})
                ner_file.write(json.dumps({"text": row["text"], "entities": [list(span) for span in entities]}, ensure_ascii=False) + "\n")

    with (OUTPUT / "entity_conflicts.csv").open("w", encoding="utf-8", newline="") as file:
        fields = ["row", "text", "existing", "candidate", "reason"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(conflicts)

    (OUTPUT / "relabel_review.csv").write_text("split,text,original_intent,suggested_intent,reason\n", encoding="utf-8")
    sources = SOURCE / "intent" / "SOURCES.md"
    (OUTPUT / "SOURCES.md").write_text(
        sources.read_text(encoding="utf-8")
        + "\n\n## data_v2 processing\n\n"
        + "The data_v2 intent files contain original and HF examples plus deterministic synthetic template examples. Synthetic rows are marked `augmented_template`. Entity labels are generated from versioned fitness lexicons and structured regex patterns, with conflicts recorded in `entity_conflicts.csv`. The original files under data/ remain unchanged.\n",
        encoding="utf-8",
    )
    print(f"Built {OUTPUT} with {sum(len(rows) for rows in rows_by_split.values())} rows.")
    print(f"Entity conflicts logged: {len(conflicts)}")


if __name__ == "__main__":
    main()
