import os
from pathlib import Path

from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
QUOTES_FILE = DATA_DIR / "quotes.json"
AUTHORS_FILE = DATA_DIR / "authors.json"

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "hw9")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))


def connect_db():
    connect(db=MONGO_DB, host=MONGO_URI)
