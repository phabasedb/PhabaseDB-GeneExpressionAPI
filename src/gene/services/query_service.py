from src.gene.repository.csv_repository import load_expression_df
from src.gene.services.expression_helpers import safe_float
from src.gene.utils.validators import ValidationError

def get_expression_by_ids(
    organism: str,
    data_type: str,
    feature: str,
    ids: list[str],
    columns: list[str],
) -> list[dict]:
    """
    Return expression data for a list of gene or transcript IDs.
    The response is a list of dictionaries, each containing:
    - "id_gen": Gene ID.
    - "id_transcript": Transcript ID.
    - "expression": List of expression values across conditions.
    """

    df = load_expression_df(
        organism=organism,
        data_type=data_type,
        feature=feature,
    )

    # Column validation
    invalid_cols = [c for c in columns if c not in df.columns]
    if invalid_cols:
        raise ValidationError(f"Invalid columns requested: {invalid_cols}")

    data = []
    processed_transcripts = set()  # To avoid duplicates
    not_found_ids = [] # IDs not found

    if feature == "genes":
        # Separating genes and transcripts
        gene_ids = [i for i in ids if ".t" not in i]
        transcript_ids = [i for i in ids if ".t" in i]

        # Process genes (brings all their transcripts)
        for gene_id in gene_ids:
            df_gene = df[df["id_gen"] == gene_id]
            if df_gene.empty:
                not_found_ids.append(gene_id)
                continue
            for _, row in df_gene.iterrows():
                tid = row["id_transcript"]
                if tid in processed_transcripts:
                    continue
                processed_transcripts.add(tid)
                data.append({
                    "id_gen": row["id_gen"],
                    "id_transcript": row["id_transcript"],
                    "expression": [{"condition": col, "value": safe_float(row[col])} for col in columns]
                })

        # Process individual transcripts (if they were not included by a gene)
        for tid in transcript_ids:
            if tid in processed_transcripts:
                continue
            df_transcript = df[df["id_transcript"] == tid]
            if df_transcript.empty:
                not_found_ids.append(tid)
                continue
            for _, row in df_transcript.iterrows():
                processed_transcripts.add(tid)
                data.append({
                    "id_gen": row["id_gen"],
                    "id_transcript": row["id_transcript"],
                    "expression": [{"condition": col, "value": safe_float(row[col])} for col in columns]
                })

    else:
        # mirna
        for identifier in ids:
            df_mirna = df[df["id_gen"] == identifier]
            if df_mirna.empty:
                not_found_ids.append(identifier)
                continue
            for _, row in df_mirna.iterrows():
                data.append({
                    "id_gen": row["id_gen"],
                    "id_transcript": row["id_transcript"],
                    "expression": [{"condition": col, "value": safe_float(row[col])} for col in columns]
                })

    return data, not_found_ids
