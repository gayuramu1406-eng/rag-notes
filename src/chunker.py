from src.config import CHUNK_SIZE, CHUNK_OVERLAP


def split_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text recursively at natural boundaries:
      1. Paragraph breaks (\n\n)
      2. Line breaks (\n)
      3. Sentence endings (. )
      4. Word boundaries ( )
      5. Character (last resort)

    This preserves meaning better than fixed-size chunking.
    """
    separators = ["\n\n", "\n", ". ", " ", ""]

    def _split(text: str, seps: list[str]) -> list[str]:
        # Base case: text fits, or we've run out of separators
        if len(text) <= chunk_size or not seps:
            return [text]

        separator = seps[0]
        next_seps = seps[1:]

        if separator == "":
            # Last resort: chop into fixed-size pieces
            return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

        parts = text.split(separator)
        chunks = []
        current = ""

        for part in parts:
            # Reattach the separator we split on
            piece = part + separator if part != parts[-1] else part

            if len(current) + len(piece) <= chunk_size:
                current += piece
            else:
                # Current chunk is full
                if current:
                    chunks.append(current)
                # If piece itself is too big, recurse with next separator
                if len(piece) > chunk_size:
                    chunks.extend(_split(piece, next_seps))
                    current = ""
                else:
                    current = piece

        if current:
            chunks.append(current)

        return chunks

    raw_chunks = _split(text, separators)

    # Apply overlap by combining the tail of the previous chunk
    if overlap <= 0 or len(raw_chunks) <= 1:
        return [c.strip() for c in raw_chunks if c.strip()]

    final_chunks = []
    for i, chunk in enumerate(raw_chunks):
        if i == 0:
            final_chunks.append(chunk.strip())
        else:
            prev_tail = raw_chunks[i - 1][-overlap:] if len(raw_chunks[i - 1]) > overlap else raw_chunks[i - 1]
            merged = prev_tail + chunk
            final_chunks.append(merged.strip())

    return [c for c in final_chunks if c]


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