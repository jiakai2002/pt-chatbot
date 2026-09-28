# Fitness intent and entity labelling guide

This guide defines the `data_v2` labels. Each message receives one primary intent. The primary intent is the **first actionable request** in a multi-intent message. `secondary_intent` may contain the additional intent when it is explicit and useful; otherwise it is blank.

## Intent labels

### `generate_plan`

Use when the user requests a structured routine, schedule, programme, or multi-session plan.

Positive examples:

- Make me a three-day workout plan.
- I need a weekly strength routine.
- Build a home programme for the next month.
- Can you plan my workouts around Monday and Friday?
- Give me a 20-minute full-body routine.

Boundary rules:

- A schedule, multiple days, duration, or routine structure indicates `generate_plan`.
- “Recommend a chest workout” without schedule or plan structure is `find_exercise`.
- If the message first asks for a plan and then asks about form, primary is `generate_plan`; secondary may be `ask_form`.

### `find_exercise`

Use when the user wants exercise suggestions or information about suitable exercises, without requesting a complete schedule.

Positive examples:

- Recommend a chest workout.
- What exercises target the hamstrings?
- What can I do with dumbbells?
- Give me an alternative to lunges.
- Which exercises are good for core strength?

Boundary rules:

- “Recommend a chest workout” is `find_exercise`.
- If the request includes a schedule, number of days, or a complete routine, use `generate_plan`.
- A question about how to perform one named exercise is `ask_form`.

### `ask_form`

Use when the user asks how to perform an exercise or improve technique.

Positive examples:

- How do I perform a squat?
- What is the correct push-up technique?
- How should I hold the bar during a deadlift?
- Show me the form for a plank.
- What is a common mistake during a lunge?

Boundary rules:

- Technique questions without an injury or medical concern are `ask_form`.
- “My knee hurts when I squat; should I continue?” is `medical_or_injury`, not `ask_form`.
- If the user asks for several exercises in a routine, use `generate_plan` or `find_exercise` depending on whether a schedule is requested.

### `get_nutrition`

Use for general food, meal, calorie, macro, hydration, or nutrition questions related to fitness.

Positive examples:

- What should I eat to build muscle?
- Give me some post-workout meal ideas.
- How much protein is in a fitness diet?
- What foods are useful before training?
- Should I focus on calories during a cut?

Boundary rules:

- General fitness nutrition is `get_nutrition`.
- Requests involving a medical condition, prescribed diet, symptoms, or medication are `medical_or_injury`.
- Food questions unrelated to fitness are `out_of_scope`.

### `log_progress`

Use when the user reports a completed or attempted workout, exercise, set, repetition, weight, distance, or time.

Positive examples:

- I finished a chest workout.
- I did three sets of squats this morning.
- Yesterday I ran five kilometres.
- Just completed 10 push-ups.
- My bench press was 50 kilograms for 5 reps.

Boundary rules:

- Do not rely on the word “today”; a workout report without a time word is still `log_progress`.
- “I need help getting started” is `motivation`, not `log_progress`.
- A future plan such as “I want to do three sets tomorrow” is usually `generate_plan` or `motivation`, depending on the request.

### `motivation`

Use for encouragement, readiness, habit support, greetings, or general fitness conversation without a specific task.

Positive examples:

- I feel unmotivated.
- I need help getting started.
- Give me some encouragement.
- Hi, can you help me stay consistent?
- I keep skipping my workouts.

Boundary rules:

- A completed workout report is `log_progress`.
- A specific plan request is `generate_plan`.
- A specific exercise suggestion is `find_exercise`.

### `medical_or_injury`

Use for pain, injury, symptoms, diagnosis, treatment, medication, medical clearance, or questions about exercising with a medical concern.

Positive examples:

- I have sharp knee pain.
- Can you diagnose my shoulder injury?
- Should I keep squatting if my knee is sore?
- What medicine should I take for back pain?
- Do I need medical clearance before exercising?

Boundary rules:

- Any exercise question containing a meaningful injury, pain, symptom, or medical-condition concern is `medical_or_injury`, even if it also asks about form.
- The chatbot must not diagnose, prescribe, or provide treatment instructions.
- General safety reminders without a personal symptom may remain part of another intent.

### `out_of_scope`

Use for non-fitness topics and fitness-adjacent requests unsupported by this project.

Positive examples:

- Tell me about the Cold War.
- How do I hack an account?
- What is the tallest building in the world?
- Which laptop should I buy?
- Can you help with my homework?

Boundary rules:

- Medical and injury requests belong to `medical_or_injury`, not `out_of_scope`.
- Basic fitness, exercise, nutrition, progress, and motivation requests belong to the relevant fitness intent.
- Buying equipment, hacking, unrelated trivia, and homework are `out_of_scope` unless a later project decision adds support for them.

## Multi-intent messages

Label the first actionable request as the primary intent. Add the second explicit request to `secondary_intent` when it is clear.

Example:

```text
Create a three-day plan and explain how to squat.
primary intent: generate_plan
secondary_intent: ask_form
```

If a medical concern appears anywhere in the request, `medical_or_injury` takes priority over normal exercise guidance.

## Entity labels

The current schema contains:

- `EXERCISE`: squat, deadlift, push-up
- `BODY_PART`: chest, back, legs, hamstrings
- `GOAL`: build muscle, lose weight, strength
- `EQUIPMENT`: dumbbells, barbell, resistance bands
- `EXPERIENCE_LEVEL`: beginner, intermediate, advanced
- `DURATION`: 20 minutes, half an hour
- `DAYS`: three days a week, Monday/Wednesday/Friday
- `FOOD`: oats, eggs, tofu, rice
- `MEAL_TIME`: breakfast, lunch, post-workout, rest day

Entity spans use zero-based character offsets with an end-exclusive end index. Spans must match the exact text, must not overlap, and must use only the allowed label names.
