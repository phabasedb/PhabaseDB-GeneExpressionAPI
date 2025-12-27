from src.gene.repository.csv_repository import load_expression_df
from src.gene.services.expression_helpers import safe_float


def get_expression_by_gene_id(
    organism: str,
    data_type: str,
    feature: str,
    gene_id: str,
) -> list[dict]:
    """
    Return expression data for a specific gene ID.
    The response is a list of dictionaries, each containing:
    - "id_gen": Gene ID.
    - "transcripts": List of transcripts with their expression data.
        Each transcript is a dictionary with:
        - "id_transcript": Transcript ID.
        - "expression": List of expression values across conditions.
    """

    df = load_expression_df(
        organism=organism,
        data_type=data_type,
        feature=feature,
    )

    df_gene = df[df["id_gen"] == gene_id]

    if df_gene.empty:
        return []

    expression_cols = [
        c for c in df_gene.columns
        if c not in {"id_gen", "id_transcript"}
    ]

    transcripts = []

    for _, row in df_gene.iterrows():
        expressions = [
            {
                "condition": col,
                "value": safe_float(row[col])
            }
            for col in expression_cols
        ]

        transcripts.append({
            "id_transcript": row["id_transcript"],
            "expression": expressions
        })

    return [
        {
            "id_gen": gene_id,
            "transcripts": transcripts
        }
    ]
