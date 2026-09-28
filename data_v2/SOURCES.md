# Intent dataset source

The downloaded `fitness-intent.parquet` file comes from:

`harshmakwana/fitness-intent` on Hugging Face

The source dataset is MIT licensed. Its labels are mapped to this project's intents:

- `general_chat` → `motivation`
- `get_nutrition_info` → `get_nutrition`
- `log_feeling` → `log_progress`
- Other labels are kept with the matching project intent.


## data_v2 processing

data_v2 is a relabelled copy of the original data. Existing source rows and wording are preserved; no synthetic augmentation has been added at this stage. The original files under data/ remain unchanged.
