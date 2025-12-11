import os
import pandas as pd
from src.config import Config

def read_dataset(dataset_name: str) -> pd.DataFrame:
    path = os.path.join(Config.BASE_DIR, dataset_name)
    if not os.path.exists(path):
        raise FileNotFoundError(
            "The requested file was not found. Please try again later or contact an administrator."
        )
    try:
        return pd.read_csv(path, dtype=str)
    except Exception:
        raise IOError(
            "An error occurred while reading the dataset data. Please try again later or contact an administrator."
        )