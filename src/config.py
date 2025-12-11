import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = os.getenv("BASE_DIR", "/expdb/")
