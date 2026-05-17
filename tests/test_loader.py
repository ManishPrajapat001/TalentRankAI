"""Manual integration script for PDF resume loading.

Run:
    python tests/test_loader.py
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.rag.loader import load_resumes  # noqa: E402
from app.utils.config import RESUME_DIR  # noqa: E402


def print_separator(title: str) -> None:
    """Print a readable console section separator."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main() -> None:
    """Load PDF resumes and print basic diagnostics."""
    print_separator("PDF Loader Debug Script")
    print(f"Resume directory: {RESUME_DIR}")

    try:
        resumes = load_resumes(RESUME_DIR)
        print(f"Number of resumes loaded: {len(resumes)}")

        if not resumes:
            print("No PDF resumes found. Generate data with:")
            print("  python scripts/generate_test_data.py --clean")
            return

        print_separator("Loaded Resume Previews")
        for resume in resumes:
            preview = " ".join(resume["text"].split()[:35])
            print(f"Candidate ID: {resume['candidate_id']}")
            print(f"Source: {resume['source']}")
            print(f"Preview: {preview}...")
            print("-" * 80)

        print("Loader script completed successfully.")
    except Exception as exc:
        print(f"Loader script failed gracefully: {exc}")


if __name__ == "__main__":
    main()
