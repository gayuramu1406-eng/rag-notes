from src.chunker import chunk_documents
from src.embedder import embed_texts
from src.store import store_chunks, collection_count


def index_documents(documents: list[dict]) -> dict:
    """
    Given a list of documents [{"source": ..., "text": ...}],
    run the full indexing pipeline:
        chunk → embed → store in ChromaDB

    Returns stats: {"documents": N, "chunks": M, "stored": M}
    """
    if not documents:
        return {"documents": 0, "chunks": 0, "stored": 0}

    chunks = chunk_documents(documents)
    if not chunks:
        return {"documents": len(documents), "chunks": 0, "stored": 0}

    texts = [c["text"] for c in chunks]
    vectors = embed_texts(texts)

    store_chunks(chunks, vectors, reset=True)

    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "stored": collection_count(),
    }