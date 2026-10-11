import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# --- Groq / LLM settings ---
MODEL_NAME = "openai/gpt-oss-120b"

RAG_SYSTEM_PROMPT = """You are a helpful assistant that answers questions using ONLY the provided context.

Rules:
- If the answer is in the context, use it and cite the source file.
- If the answer is NOT in the context, say: "I don't have enough information in the provided documents to answer that."
- Do not make up information. Do not use outside knowledge.
- Do NOT add citation markers like 【1†L1-L4】 or [1] in your answer. Just write the answer normally. The app already shows sources separately.
"""

# --- Embedding settings ---
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- Chunking settings ---
CHUNK_SIZE = 1000       # characters per chunk
CHUNK_OVERLAP = 200    # characters shared between consecutive chunks

# --- Retrieval settings ---
TOP_K = 5             # how many chunks to retrieve per question

# --- Storage ---
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "documents"

# --- Input data ---
DATA_DIR = "data"