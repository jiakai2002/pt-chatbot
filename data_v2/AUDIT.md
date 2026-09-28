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
Total rows: **452**

### Class counts
- **train**: {'ask_form': 60, 'find_exercise': 60, 'generate_plan': 58, 'get_nutrition': 58, 'log_progress': 58, 'medical_or_injury': 33, 'motivation': 58, 'out_of_scope': 25}
- **val**: {'ask_form': 3, 'find_exercise': 3, 'generate_plan': 3, 'get_nutrition': 3, 'log_progress': 3, 'medical_or_injury': 3, 'motivation': 3}
- **test**: {'ask_form': 3, 'find_exercise': 3, 'generate_plan': 3, 'get_nutrition': 3, 'log_progress': 3, 'medical_or_injury': 3, 'motivation': 3}

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
- **medical_or_injury** — openers: [('can you diagnose', 5), ('what medicine should', 2), ('can you replace', 2), ('can you tell', 2), ('i have a', 2)]; repeated trigrams: [('can you diagnose', 5), ('you diagnose my', 3), ('should i take', 3), ('diagnose my shoulder', 2), ('what medicine should', 2)]
- **motivation** — openers: [('i want to', 4), ('can you help', 3), ('i feel discouraged', 3), ('motivate me to', 2), ('i need a', 2)]; repeated trigrams: [('i want to', 4), ('can you help', 3), ('you help me', 3), ('i feel discouraged', 3), ('motivate me to', 2)]
- **out_of_scope** — openers: [('what is the', 4), ("what's the best", 3), ('how do i', 2), ('can you tell', 2), ('who wrote the', 2)]; repeated trigrams: [('what is the', 4), ("what's the best", 3), ('how do i', 2), ('the best way', 2), ('best way to', 2)]
