import chromadb
from src.config import CHROMA_DIR, COLLECTION_NAME


def get_client():
    """Create a persistent ChromaDB client (saves to disk)."""
    return chromadb.PersistentClient(path=CHROMA_DIR)


def get_collection(reset: bool = False):
    """
    Get the collection. If reset=True, delete existing data first
    so we can re-index from scratch.
    """
    client = get_client()

    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass  # collection didn't exist yet — that's fine

    return client.get_or_create_collection(COLLECTION_NAME)


def store_chunks(chunks: list[dict], embeddings: list[list[float]], reset: bool = True) -> int:
    """
    Store chunks + their embeddings in ChromaDB.
    Returns the number of chunks stored.
    """
    collection = get_collection(reset=reset)

    ids = [f"{c['source']}::chunk{c['chunk_id']}" for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"], "chunk_id": c["chunk_id"]} for c in chunks]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(chunks)


def collection_count() -> int:
    """How many chunks are currently stored."""
    collection = get_collection()
    return collection.count()
