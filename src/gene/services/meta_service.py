from src.gene.repository.csv_repository import load_meta_df


def get_meta(organism: str, feature: str) -> list[dict]:
    """
    Return metadata records for a given organism and feature.
    Each record is a dictionary containing:
    - "library": Library identifier.
    - "information": A dictionary with metadata fields:
        - "organism"
        - "cultivar"
        - "genotype"
        - "tissue_organ"
        - "treatment"
        - "inocula"
        - "time_post_treatment"
        - "additional_info"
        - "reference"
        - "doi"
    """

    df = load_meta_df(
        organism=organism,
        feature=feature,
    )

    df = df.astype(str).fillna("")

    records = df.to_dict("records")

    data = [
        {
            "library": r["library"],
            "information": {
                "organism": r["organism"],
                "cultivar": r["cultivar"],
                "genotype": r["genotype"],
                "tissue_organ": r["tissue_organ"],
                "treatment": r["treatment"],
                "inocula": r["inocula"],
                "time_post_treatment": r["time_post_treatment"],
                "additional_info": r["additional_info"],
                "reference": r["reference"],
                "doi": r["doi"],
            }
        }
        for r in records
    ]

    return data
