from pathlib import Path
from pypdf import PdfReader
from src.config import DATA_DIR


def load_pdf(path: Path) -> str:
    """Extract all text from a PDF file."""
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n".join(pages)


def load_text(path: Path) -> str:
    """Read a plain text or markdown file."""
    return path.read_text(encoding="utf-8", errors="ignore")


def load_file(path: Path) -> str:
    """Load one file based on its extension."""
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return load_pdf(path)
    elif suffix in (".txt", ".md"):
        return load_text(path)
    else:
        return ""  # unsupported file type — skip
def load_all_documents(folder: str | Path = None) -> list[dict]:
    """
    Read every supported file in `folder` (default: config DATA_DIR).

    Returns a list of dicts: [{"source": "filename", "text": "..."}]
    """
    data_dir = Path(folder) if folder is not None else Path(DATA_DIR)

    if not data_dir.exists():
        raise FileNotFoundError(f"'{data_dir}' folder not found.")

    documents = []

    for path in sorted(data_dir.rglob("*")):
        if not path.is_file():
            continue

        text = load_file(path)
        if not text.strip():
            continue

        documents.append({
            "source": path.name,
            "text": text,
        })

    return documents