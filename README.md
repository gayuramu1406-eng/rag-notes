# rag-notes

A Retrieval-Augmented Generation (RAG) system that answers questions about your own PDFs, Markdown, and text files. Built from scratch — no LangChain, no frameworks — using Streamlit for the UI.

## What it does

- Upload PDF, Markdown, or text files through a web UI
- Automatically chunks, embeds, and indexes them into a local vector database
- Ask questions in a chat interface — get grounded answers with source citations
- Refuses to answer when information isn't in the documents (no hallucinations)

## Demo

Tried on real documents:
- **HDFC Bank Integrated Annual Report 2025-26** (~629 pages)
- **Tesco PLC Annual Report and Financial Statements 2026** (~236 pages)

Example queries that work:
- "How is Tesco reducing store emissions?"
- "What did Gerry Murphy say?"
- "How many colleagues does Tesco employ?"

Example of the "no hallucination" guard:
- Q: "What is the capital of France?"
- A: "I don't have enough information in the provided documents to answer that."

## Architecture

PDFs → Loader → Chunker → Embedder → ChromaDB
↑
User Question → Embed → Retriever ────────┘
↓
Question + Top chunks → Groq LLM → Grounded answer


## Stack

- **Python 3.13**
- **Streamlit** — web UI
- **sentence-transformers** (`all-MiniLM-L6-v2`) — local embeddings, no API cost
- **ChromaDB** — persistent vector database
- **Groq** (`gpt-oss-120b`) — fast LLM inference
- **PyPDF** — PDF text extraction

## Project structure
rag-notes/
├── app.py # Streamlit UI
├── main.py # CLI version (alternative to UI)
├── src/
│ ├── config.py # Settings (chunk size, model, prompts)
│ ├── loader.py # Reads PDFs, .md, .txt files
│ ├── chunker.py # Splits text into overlapping chunks
│ ├── embedder.py # Converts text → vectors
│ ├── store.py # ChromaDB read/write
│ ├── retriever.py # Finds most relevant chunks for a query
│ ├── indexer.py # Orchestrates load → chunk → embed → store
│ └── rag.py # Retrieves context + calls Groq
├── test_*.py # Test scripts for each stage
└── requirements.txt
