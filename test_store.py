from src.loader import load_all_documents
from src.chunker import chunk_documents
from src.embedder import embed_texts
from src.store import store_chunks, collection_count

print("1. Loading documents...")
docs = load_all_documents()
print(f"   → {len(docs)} documents\n")

print("2. Chunking...")
chunks = chunk_documents(docs)
print(f"   → {len(chunks)} chunks\n")
print("Chunks preview:",chunks)



print("3. Embedding...")
texts = [c["text"] for c in chunks]
vectors = embed_texts(texts)
print(f"   → {len(vectors)} vectors, each {len(vectors[0])} dimensions\n")

# print("=== SAMPLE CHUNK + VECTOR ===")
# print(f"Chunk text (first 120 chars): {[ texts[0][:120].replace(chr(10), ' ') for i in texts]}")
# print(f"Vector (first 5 dims): {[vectors[0][:5] for i in vectors]}\n")

print("4. Storing in ChromaDB...")
count = store_chunks(chunks, vectors, reset=True)
print(f"   → {count} chunks stored\n")

print(f"✅ Collection now has {collection_count()} items")