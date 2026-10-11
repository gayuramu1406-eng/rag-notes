from src.loader import load_all_documents
from src.chunker import chunk_documents
from src.embedder import embed_texts

print("=== STAGE 1: LOADER ===")
docs = load_all_documents()
for d in docs:
    print(d)
    print()

print("=== STAGE 2: CHUNKER ===")
chunks = chunk_documents(docs)
for c in chunks:
    print(c)
    print()

print("=== STAGE 3: EMBEDDER (first 5 numbers only) ===")
vectors = embed_texts([c["text"] for c in chunks])
for i, v in enumerate(vectors):
    print(f"Vector {i} (showing first 5): {v[:5]}")