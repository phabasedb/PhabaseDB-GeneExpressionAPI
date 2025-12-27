import pandas as pd
from src.gene.utils.resolve_file import resolve_dataset_file
from src.gene.utils.read_file import read_dataset
from src.gene.constants import (
    REQUIRED_GENE_COLUMNS,
    REQUIRED_META_COLUMNS,
)

# --------------------
# EXCEPTIONS
# --------------------
class DatasetSchemaError(Exception):
    pass


# --------------------
# FUNCTIONS
# --------------------
def load_expression_df(
    organism: str,
    data_type: str,
    feature: str,
) -> pd.DataFrame:
    """
    Load an expression dataset (raw / scorez).
    """
    df = _load_df(organism, data_type, feature)
    _validate_columns(df, REQUIRED_GENE_COLUMNS)
    return df


def load_meta_df(
    organism: str,
    feature: str,
) -> pd.DataFrame:
    """
    Load a metadata dataset.
    """
    df = _load_df(organism, "meta", feature)
    _validate_columns(df, REQUIRED_META_COLUMNS)
    return df


# --------------------
# INTERNAL HELPERS
# --------------------

def _load_df(
    organism: str,
    data_type: str,
    feature: str,
) -> pd.DataFrame:
    path = resolve_dataset_file(
        organism=organism,
        data_type=data_type,
        feature=feature,
    )
    return read_dataset(path)


def _validate_columns(df: pd.DataFrame, required: list[str]):
    # Validate that required columns are present
    if not set(required).issubset(df.columns):
        raise DatasetSchemaError("Dataset schema is invalid.")
