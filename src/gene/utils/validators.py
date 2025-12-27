# --------------------
# EXCEPTIONS
# --------------------
class ValidationError(Exception):
    pass

# --------------------
# VARIABLE REUSABLES
# --------------------
ALLOWED_DATA_TYPES = {"raw", "scorez"}
ALLOWED_FEATURES = {"genes", "mirna"}


# --------------------
# META VALIDATION
# --------------------
def validate_meta_request(
        organism: str,
        feature: str
):
    if not organism or not isinstance(organism, str):
        raise ValidationError("Organism is required.")

    if not feature or not isinstance(feature, str):
        raise ValidationError("Feature is required.")


# --------------------
# GENE ID VALIDATION
# --------------------
def validate_gene_request(
    organism: str,
    data_type: str,
    feature: str,
    gene_id: str,
):
    if not organism or not isinstance(organism, str):
        raise ValueError("Organism is required.")

    if data_type not in ALLOWED_DATA_TYPES:
        raise ValidationError(
            f"Invalid data_type. Expected one of {ALLOWED_DATA_TYPES}."
        )

    if feature not in ALLOWED_FEATURES:
        raise ValidationError(
            f"Invalid feature. Expected one of {ALLOWED_FEATURES}."
        )

    if not gene_id or not isinstance(gene_id, str):
        raise ValidationError("Gene ID is required.")


# --------------------
# IDS MULTI-QUERY VALIDATION
# --------------------
def validate_expression_query_request(
    organism: str,
    data_type: str,
    feature: str,
    ids: list[str],
    columns: list[str]
):
    """
    Validates the input for querying multiple expressions by IDs and columns.
    """
    if not organism or not isinstance(organism, str):
        raise ValidationError("Organism is required.")

    if data_type not in ALLOWED_DATA_TYPES:
        raise ValidationError(
            f"Invalid data_type. Expected one of {ALLOWED_DATA_TYPES}."
        )

    if feature not in ALLOWED_FEATURES:
        raise ValidationError(
            f"Invalid feature. Expected one of {ALLOWED_FEATURES}."
        )

    if not ids or not isinstance(ids, list):
        raise ValidationError("ids must be a non-empty list of strings.")

    if not all(isinstance(g, str) for g in ids):
        raise ValidationError("All ids must be strings.")

    if not columns or not isinstance(columns, list):
        raise ValidationError("columns must be a non-empty list of strings.")

    if not all(isinstance(c, str) for c in columns):
        raise ValidationError("All columns must be strings.")


