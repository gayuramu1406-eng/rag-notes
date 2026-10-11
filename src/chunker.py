from src.config import CHUNK_SIZE, CHUNK_OVERLAP


def split_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text into overlapping chunks of roughly `chunk_size` characters.

    Example (chunk_size=10, overlap=3):
        "abcdefghijklmnop"
        → "abcdefghij"
        → "hijklmnop"   (starts 3 chars before the previous ended)
    """
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []
    start = 0
    step = chunk_size - overlap

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += step

    return chunks


def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Take documents and produce chunks.
    Each chunk keeps track of which file it came from.

    Returns: [{"source": "file.pdf", "text": "chunk text", "chunk_id": 0}]
    """
    all_chunks = []

    for doc in documents:
        pieces = split_text(doc["text"])

        for i, piece in enumerate(pieces):
            all_chunks.append({
                "source": doc["source"],
                "text": piece,
                "chunk_id": i,
            })

    return all_chunks