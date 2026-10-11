from src.retriever import retrieve

queries = [
    "How tall is the Eiffel Tower?",
    "How much do cats sleep?",
    "What is quantum entanglement?",
    "How do I cook pasta?",
    "What is the capital of Japan?",   # not in our docs!
]

for q in queries:
    print(f"\n❓ {q}")
    print("-" * 60)
    hits = retrieve(q, top_k=2)
    for h in hits:
        preview = h["text"][:100].replace("\n", " ")
        print(f"  [{h['distance']:.3f}] {h['source']} #{h['chunk_id']}: {preview}...")