from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR/"data"/"Raw"/"house_price_dataset_india_12k.csv"
PROCESSED_PATH = BASE_DIR/"data"/"processed"/"house_price_processed.csv"
