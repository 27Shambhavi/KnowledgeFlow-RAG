import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

UPLOAD_DIR = "data/uploads"
VECTORSTORE_DIR = "vectorstore/chroma"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

TOP_K = 5
RELEVANCE_THRESHOLD = 0.5