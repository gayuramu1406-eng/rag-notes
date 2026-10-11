import streamlit as st
from pathlib import Path
import tempfile

from src.loader import load_all_documents
from src.indexer import index_documents
from src.rag import answer
from src.store import collection_count


# ---------- Page setup ----------
st.set_page_config(page_title="RAG Notes", page_icon="📚", layout="wide")
st.title("📚 RAG Notes")
st.caption("Ask questions about your documents. Powered by Groq + ChromaDB.")


# ---------- Session state ----------
# Streamlit reruns the whole script on every interaction.
# Session state keeps things that should survive reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []   # chat history

if "indexed" not in st.session_state:
    st.session_state.indexed = False


# ---------- Sidebar: document upload & indexing ----------
with st.sidebar:
    st.header("📂 Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF, Markdown, or Text files",
        type=["pdf", "md", "txt"],
        accept_multiple_files=True,
    )

    use_sample_data = st.checkbox("Also include files from data/ folder", value=True)

    if st.button("🔄 Index documents", use_container_width=True):
        documents = []

        # 1. Files uploaded in this session
        if uploaded_files:
            for uf in uploaded_files:
                suffix = Path(uf.name).suffix.lower()

                if suffix == ".pdf":
                    # pypdf needs a path or file-like; write to temp
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(uf.getvalue())
                        tmp_path = tmp.name

                    from pypdf import PdfReader
                    reader = PdfReader(tmp_path)
                    text = "\n".join((page.extract_text() or "") for page in reader.pages)

                    Path(tmp_path).unlink()  # cleanup

                else:  # .md / .txt
                    text = uf.getvalue().decode("utf-8", errors="ignore")

                if text.strip():
                    documents.append({"source": uf.name, "text": text})

        # 2. Files from data/ folder (optional)
        if use_sample_data:
            try:
                documents.extend(load_all_documents("data"))
            except FileNotFoundError:
                pass  # no data/ folder → skip silently

        if not documents:
            st.warning("No documents found. Upload files or add to data/ folder.")
        else:
            with st.spinner("Indexing..."):
                stats = index_documents(documents)
            st.session_state.indexed = True
            st.success(
                f"✅ Indexed {stats['documents']} docs → "
                f"{stats['chunks']} chunks stored"
            )

    st.divider()
    st.metric("Chunks in DB", collection_count() if st.session_state.indexed else 0)

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ---------- Main chat area ----------
if not st.session_state.indexed:
    st.info("👈 Upload files and click **Index documents** to get started.")
else:
    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("📚 Sources"):
                    for s in msg["sources"]:
                        st.write(f"- `{s['source']}` (chunk {s['chunk_id']}, distance {s['distance']:.3f})")

    # Chat input at bottom
    if prompt := st.chat_input("Ask a question about your documents..."):
        # 1. Show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Get RAG answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = answer(prompt, top_k=3)

            st.markdown(result["answer"])

            with st.expander("📚 Sources"):
                for s in result["sources"]:
                    st.write(f"- `{s['source']}` (chunk {s['chunk_id']}, distance {s['distance']:.3f})")

        # 3. Save to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"],
        })