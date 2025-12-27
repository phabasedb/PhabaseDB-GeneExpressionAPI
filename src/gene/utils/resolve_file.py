import os
import re
from src.config import Config


def resolve_dataset_file(
    organism: str,
    data_type: str,
    feature: str,
) -> str:
    """
    Resolve the latest version of a dataset file based on naming convention.

    Expected filename format:
    {organism}_{data_type}_{feature}_v#.csv
    Example:
    pvulgarisnj_meta_genes_v1.csv

    excptions:
        FileNotFoundError: If no matching file or folder is found.
    """

    # Normalize inputs
    organism = organism.lower()
    data_type = data_type.lower()
    feature = feature.lower()

    folder = os.path.join(Config.EXPDB_PATH, organism)

    if not os.path.isdir(folder):
        raise FileNotFoundError(
            f"Organism folder not found: {organism}"
        )

    pattern = re.compile(
        rf"{organism}_{data_type}_{feature}_v(\d+)\.csv"
    )

    candidates: list[tuple[int, str]] = []

    for fname in os.listdir(folder):
        match = pattern.fullmatch(fname)
        if match:
            version = int(match.group(1))
            candidates.append((version, fname))

    if not candidates:
        raise FileNotFoundError(
            "Dataset file not found for the given parameters."
        )

    # Select highest version
    latest_file = max(candidates, key=lambda x: x[0])[1]
    return os.path.join(folder, latest_file)