from groq import Groq
from src.config import GROQ_API_KEY, MODEL_NAME, RAG_SYSTEM_PROMPT, TOP_K
from src.retriever import retrieve

client = Groq(api_key=GROQ_API_KEY)


def build_context(hits: list[dict]) -> str:
    """
    Format retrieved chunks into a single text block for the LLM.
    Each chunk gets a numbered label so the model can cite it.
    """
    lines = []
    for i, hit in enumerate(hits, start=1):
        lines.append(f"[{i}] (from {hit['source']})")
        lines.append(hit["text"])
        lines.append("")
    return "\n".join(lines).strip()


def answer(question: str, top_k: int = TOP_K) -> dict:
    """
    Full RAG pipeline:
      1. Retrieve relevant chunks
      2. Build a context block
      3. Send question + context to the LLM
      4. Return the answer + sources
    """
    hits = retrieve(question, top_k=top_k)
    context = build_context(hits)

    user_prompt = f"""Use the context below to answer the question.

--- CONTEXT ---
{context}
--- END CONTEXT ---

Question: {question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": RAG_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    reply = response.choices[0].message.content

    return {
        "answer": reply,
        "sources": [
            {"source": h["source"], "chunk_id": h["chunk_id"], "distance": h["distance"]}
            for h in hits
        ],
    }