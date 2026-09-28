# Dataset Audit

## Original data

Data root: `C:\Users\jiakai\Projects\pt\data`
Total rows: **452**

### Class counts
- **train**: {'ask_form': 60, 'find_exercise': 60, 'generate_plan': 58, 'get_nutrition': 58, 'log_progress': 58, 'motivation': 58, 'out_of_scope': 58}
- **val**: {'ask_form': 3, 'find_exercise': 3, 'generate_plan': 3, 'get_nutrition': 3, 'log_progress': 3, 'motivation': 3, 'out_of_scope': 3}
- **test**: {'ask_form': 3, 'find_exercise': 3, 'generate_plan': 3, 'get_nutrition': 3, 'log_progress': 3, 'motivation': 3, 'out_of_scope': 3}

### Duplicate and near-duplicate checks
- Exact duplicate groups: **2**
- Exact duplicate groups across splits: **2**
- TF-IDF cosine > 0.9 near-duplicate pairs: **0**
- Near-duplicate pairs across splits: **0**

### Entity annotation checks
- Offset/overlap/schema errors: **0**
- Unlabelled lexicon candidates: **0** occurrences

### Text length distribution
- Characters: min=18, median=39, max=84
- Words: min=3, median=7, max=15

### Repeated openers and trigrams
- **ask_form** — openers: [('how do i', 22), ('what is the', 9), ('can you explain', 8), ('how should i', 7), ('how should my', 2)]; repeated trigrams: [('how do i', 22), ('what is the', 9), ('can you explain', 8), ('how should i', 7), ('do i perform', 6)]
- **find_exercise** — openers: [('how to do', 5), ('what are good', 4), ('show me some', 3), ('what can i', 3), ('recommend a chest', 2)]; repeated trigrams: [('can i do', 5), ('how to do', 5), ('to do a', 5), ('exercises for a', 5), ('good exercises for', 4)]
- **generate_plan** — openers: [('i want a', 8), ('i need a', 5), ('give me a', 4), ('make me a', 3), ('can you create', 2)]; repeated trigrams: [('i want a', 8), ('i need a', 5), ('give me a', 4), ('meal plan for', 4), ('plan for someone', 4)]
- **get_nutrition** — openers: [('what should i', 8), ('what is a', 6), ('how can i', 6), ('what are some', 5), ('tell me about', 4)]; repeated trigrams: [('should i eat', 9), ('what should i', 8), ('what is a', 6), ('how can i', 6), ('what are some', 5)]
- **log_progress** — openers: [('i want to', 5), ('i completed my', 4), ('i finished a', 3), ('i finished my', 3), ('i did three', 2)]; repeated trigrams: [('i completed my', 5), ('i want to', 5), ('record that i', 4), ('i finished a', 3), ('i finished my', 3)]
- **motivation** — openers: [('i want to', 4), ('can you help', 3), ('i feel discouraged', 3), ('motivate me to', 2), ('i need a', 2)]; repeated trigrams: [('i want to', 4), ('can you help', 3), ('you help me', 3), ('i feel discouraged', 3), ('motivate me to', 2)]
- **out_of_scope** — openers: [('can you diagnose', 5), ('what is the', 4), ('can you tell', 4), ('i think i', 3), ("what's the best", 3)]; repeated trigrams: [('can you diagnose', 5), ('should i take', 4), ('what is the', 4), ('can you tell', 4), ('you tell me', 4)]

## data_v2

Data root: `C:\Users\jiakai\Projects\pt\data_v2`
Total rows: **2052**

### Class counts
- **train**: {'ask_form': 210, 'find_exercise': 210, 'generate_plan': 208, 'get_nutrition': 208, 'log_progress': 208, 'medical_or_injury': 183, 'motivation': 208, 'out_of_scope': 175}
- **val**: {'ask_form': 28, 'find_exercise': 28, 'generate_plan': 28, 'get_nutrition': 28, 'log_progress': 28, 'medical_or_injury': 28, 'motivation': 28, 'out_of_scope': 25}
- **test**: {'ask_form': 28, 'find_exercise': 28, 'generate_plan': 28, 'get_nutrition': 28, 'log_progress': 28, 'medical_or_injury': 28, 'motivation': 28, 'out_of_scope': 25}

### Duplicate and near-duplicate checks
- Exact duplicate groups: **2**
- Exact duplicate groups across splits: **2**
- TF-IDF cosine > 0.9 near-duplicate pairs: **396**
- Near-duplicate pairs across splits: **72**
  - `0.905` `train`: 3 days plan / `val`: 4 days plan
  - `0.911` `train`: yesterday i did tricep dip: 3 sets of 10 reps with a barbell and a 30 minute session / `val`: yesterday i did tricep dip: 3 sets of 10 reps with a gym and a 30 minute session
  - `0.906` `train`: record my tricep dip: 3 sets of 10 reps with a barbell and a 30 minute session I am not sure where to start and would appreciate a simple answer that fits my week. / `val`: for my record i did tricep dip: 3 sets of 10 reps with a gym and a 30 minute session I am not sure where to start and would appreciate a simple answer that fits my week.
  - `0.905` `train`: help me bulk; I keep skipping sessions and need a realistic way to begin I am not sure where to start and would appreciate a simple answer that fits my week. / `val`: why cant i bulk; I keep skipping sessions and need a realistic way to begin I am not sure where to start and would appreciate a simple answer that fits my week.
  - `0.910` `train`: help me bulk; I keep skipping sessions and need a realistic way to begin I am not sure where to start and would appreciate a simple answer that fits my week. / `val`: i need help staying bulk; I keep skipping sessions and need a realistic way to begin I am not sure where to start and would appreciate a simple answer that fits my week.
  - `0.903` `train`: help me bulk; I keep skipping sessions and need a realistic way to begin I am not sure where to start and would appreciate a simple answer that fits my week. / `val`: how can i restart bulk; I keep skipping sessions and need a realistic way to begin I am not sure where to start and would appreciate a simple answer that fits my week.
  - `0.915` `train`: help me bulk; I keep skipping sessions and need a realistic way to begin I am not sure where to start and would appreciate a simple answer that fits my week. / `test`: help me cut; I keep skipping sessions and need a realistic way to begin I am not sure where to start and would appreciate a simple answer that fits my week.
  - `0.965` `train`: motivate me bulk; I keep skipping sessions and need a realistic way to begin / `val`: pls motivate bulk; I keep skipping sessions and need a realistic way to begin
  - `0.912` `train`: i need encouragement bulk; i keep skipping sessions and need a realistic way to begin / `val`: i need encouragement cut; I keep skipping sessions and need a realistic way to begin
  - `0.900` `train`: im struggling bulk; I keep skipping sessions and need a realistic way to begin / `test`: im struggling cut; I keep skipping sessions and need a realistic way to begin

### Entity annotation checks
- Offset/overlap/schema errors: **0**
- Unlabelled lexicon candidates: **0** occurrences

### Text length distribution
- Characters: min=5, median=76, max=204
- Words: min=1, median=14, max=41

### Repeated openers and trigrams
- **ask_form** — openers: [('how do i', 47), ('what is the', 15), ('how should i', 12), ('can you explain', 12), ('how should my', 9)]; repeated trigrams: [('the main form', 194), ('main form cues', 194), ('and tell me', 193), ('tell me the', 193), ('me the main', 193)]
- **find_exercise** — openers: [('what can i', 17), ('what should i', 13), ('what are good', 10), ('im looking for', 7), ('what are my', 7)]; repeated trigrams: [('i am not', 42), ('am not sure', 42), ('not sure where', 42), ('sure where to', 42), ('where to start', 42)]
- **generate_plan** — openers: [('i want a', 13), ('give me a', 9), ('design a a', 7), ('im trying to', 7), ('got time for', 7)]; repeated trigrams: [('workout plan for', 108), ('plan for lose', 67), ('for lose weight', 67), ('someone new to', 50), ('days someone new', 49)]
- **get_nutrition** — openers: [('what should i', 20), ('what is a', 12), ('how can i', 12), ('tell me about', 10), ('what foods are', 8)]; repeated trigrams: [('what should i', 217), ('should i eat', 212), ('i eat after', 198), ('work and what', 197), ('and what should', 197)]
- **log_progress** — openers: [('record that i', 9), ('today i did', 7), ('for my record', 7), ('this morning i', 7), ('i knocked out', 6)]; repeated trigrams: [('3 sets of', 195), ('sets of 10', 195), ('of 10 reps', 195), ('10 reps with', 195), ('and a 30', 195)]
- **medical_or_injury** — openers: [('can you diagnose', 10), ('i have a', 9), ('is it safe', 8), ('pls diagnose knee', 8), ('numb during knee', 8)]; repeated trigrams: [('knee pain after', 197), ('should i keep', 197), ('i keep training', 197), ('keep training or', 197), ('training or seek', 197)]
- **motivation** — openers: [('i need a', 10), ('i want to', 10), ('how can i', 10), ('give me a', 9), ('i need encouragement', 8)]; repeated trigrams: [('i keep skipping', 197), ('keep skipping sessions', 197), ('skipping sessions and', 197), ('sessions and need', 197), ('and need a', 197)]
- **out_of_scope** — openers: [('what is the', 12), ('how do i', 8), ('what are the', 7), ('tell me about', 7), ('what is a', 7)]; repeated trigrams: [('i am not', 43), ('am not sure', 43), ('not sure where', 43), ('sure where to', 43), ('where to start', 43)]
