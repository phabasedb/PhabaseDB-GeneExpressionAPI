import os
import pandas as pd


def read_dataset(file_path: str) -> pd.DataFrame:
    """
    Read a CSV dataset and return it as a DataFrame.
    exceptions:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "The requested dataset file does not exist."
        )

    try:
        return pd.read_csv(file_path, dtype=str)
    except Exception as exc:
        raise IOError(
            "An error occurred while reading the dataset file."
        ) from exc
