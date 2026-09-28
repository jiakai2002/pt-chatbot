# Intent dataset source

The downloaded `fitness-intent.parquet` file comes from:

`harshmakwana/fitness-intent` on Hugging Face

The source dataset is MIT licensed. Its labels are mapped to this project's intents:

- `general_chat` → `motivation`
- `get_nutrition_info` → `get_nutrition`
- `log_feeling` → `log_progress`
- Other labels are kept with the matching project intent.


## data_v2 processing

The data_v2 intent files contain original and HF examples plus deterministic synthetic template examples. Synthetic rows are marked `augmented_template`. Entity labels are generated from versioned fitness lexicons and structured regex patterns, with conflicts recorded in `entity_conflicts.csv`. The original files under data/ remain unchanged.
