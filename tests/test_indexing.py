"""Manual integration script for ChromaDB indexing.

Run:
    python tests/test_indexing.py
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.rag.loader import load_resumes  # noqa: E402
from app.rag.vector_store import ResumeVectorStore  # noqa: E402
from app.utils.config import CHROMA_DIR, RESUME_DIR  # noqa: E402


def print_separator(title: str) -> None:
    """Print a readable console section separator."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main() -> None:
    """Index local PDF resumes into ChromaDB."""
    print_separator("Chroma Indexing Debug Script")
    print(f"Resume directory: {RESUME_DIR}")
    print(f"Chroma directory: {CHROMA_DIR}")

    try:
        resumes = load_resumes(RESUME_DIR)
        print(f"Readable resumes found: {len(resumes)}")
        if not resumes:
            print("No PDF resumes found. Generate data with:")
            print("  python scripts/generate_test_data.py --clean")
            return

        print("Initializing vector store...")
        store = ResumeVectorStore()

        print("Indexing resumes. First run may download the embedding model.")
        chunk_count = store.index_resumes(RESUME_DIR)

        print_separator("Indexing Complete")
        print(f"Indexed chunks: {chunk_count}")
        print("You can now run:")
        print("  python tests/test_retrieval.py")
    except Exception as exc:
        print(f"Indexing script failed gracefully: {exc}")


if __name__ == "__main__":
    main()
