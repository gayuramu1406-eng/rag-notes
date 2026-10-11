from src.embedder import embed_query
from src.store import get_collection
from src.config import TOP_K


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    """
    Given a query string, find the top_k most similar chunks in ChromaDB.

    Returns a list of dicts like:
        [{"text": "...", "source": "file.pdf", "chunk_id": 0, "distance": 0.23}, ...]
    """
    collection = get_collection()

    query_vector = embed_query(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
    )

    # ChromaDB returns nested lists (one entry per query).
    # We only sent one query, so unpack index [0].
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    hits = []
    for text, meta, dist in zip(documents, metadatas, distances):
        hits.append({
            "text": text,
            "source": meta.get("source", "unknown"),
            "chunk_id": meta.get("chunk_id", -1),
            "distance": dist,
        })

    return hits