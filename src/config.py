import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Path to expression database directory.
    # Uses EXPDB_PATH env var if defined, otherwise defaults to local /expdb folder.
    EXPDB_PATH = os.getenv(
        "EXPDB_PATH",
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "expdb")
        )
    )
