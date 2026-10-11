from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL

# Load the model once when this module is imported
print(f"🔧 Loading embedding model: {EMBEDDING_MODEL}")
_model = SentenceTransformer(EMBEDDING_MODEL)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Convert a list of texts into a list of embedding vectors.
    Each vector is a list of floats.
    """
    embeddings = _model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()


def embed_query(query: str) -> list[float]:
    """Embed a single query string."""
    embedding = _model.encode(query, show_progress_bar=False)
    return embedding.tolist()