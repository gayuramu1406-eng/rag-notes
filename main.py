from src.loader import load_all_documents
from src.chunker import chunk_documents
from src.embedder import embed_texts
from src.store import store_chunks, collection_count
from src.rag import answer


def index_documents():
    """Load, chunk, embed, and store all documents in data/."""
    print("📂 Indexing data/...")

    docs = load_all_documents()
    if not docs:
        print("   ⚠️  No documents found in data/. Add files and try again.")
        return False

    print(f"   Loaded {len(docs)} documents")

    chunks = chunk_documents(docs)
    print(f"   Created {len(chunks)} chunks")

    texts = [c["text"] for c in chunks]
    vectors = embed_texts(texts)

    store_chunks(chunks, vectors, reset=True)
    print(f"   Stored in ChromaDB (total: {collection_count()} items)\n")

    return True


def main():
    print("🤖 RAG Notes — ask questions about your documents\n")

    if not index_documents():
        return

    print("Type your question, or 'exit' to quit.\n")

    while True:
        try:
            query = input("❓ ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not query:
            continue

        if query.lower() == "exit":
            print("Goodbye!")
            break

        try:
            result = answer(query, top_k=3)
        except Exception as e:
            print(f"⚠️  Error: {e}\n")
            continue

        print(f"\n💡 {result['answer']}\n")

        print("📚 Sources:")
        for s in result["sources"]:
            print(f"   - {s['source']} (chunk {s['chunk_id']}, distance {s['distance']:.3f})")
        print()


if __name__ == "__main__":
    main()