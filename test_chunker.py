from src.loader import load_all_documents
from src.chunker import chunk_documents

docs = load_all_documents()
print(f"Loaded {len(docs)} documents\n")

chunks = chunk_documents(docs)
print(f"Created {len(chunks)} chunks\n")

for i, c in enumerate(chunks):
    preview = c["text"][:120].replace("\n", " ")
    print(f"--- Chunk {i} ({len(c['text'])} chars) from {c['source']} ---")
    print(preview)
    print()