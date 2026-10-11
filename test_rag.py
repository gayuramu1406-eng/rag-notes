from src.rag import answer

questions = [
    "How tall is the Eiffel Tower?",
    "How long do cats sleep?",
    "How do I cook pasta?",
    "What is the capital of Japan?",   # not in our docs
]

for q in questions:
    print(f"\n❓ {q}")
    print("=" * 60)
    result = answer(q, top_k=3)
    print(f"💡 {result['answer']}\n")
    print("📚 Sources:")
    for s in result["sources"]:
        print(f"   - {s['source']} (chunk {s['chunk_id']}, distance {s['distance']:.3f})")