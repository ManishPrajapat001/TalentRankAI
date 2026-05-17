"""Manual integration script for semantic candidate retrieval.

Run:
    python tests/test_retrieval.py
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.rag.retriever import CandidateRetriever  # noqa: E402


QUERY = "React developer with Node.js and 3 years experience"


def print_separator(title: str) -> None:
    """Print a readable console section separator."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main() -> None:
    """Run semantic retrieval and print structured candidate data."""
    print_separator("Semantic Retrieval Debug Script")
    print(f"Query: {QUERY}")

    try:
        retriever = CandidateRetriever()
        candidates = retriever.retrieve(QUERY, top_k=10)

        print(f"Candidates returned: {len(candidates)}")
        if not candidates:
            print("No candidates returned. Try indexing first:")
            print("  python tests/test_indexing.py")
            return

        print_separator("Retrieved Candidates")
        for candidate in candidates:
            evidence = " ".join(candidate.get("evidence", "").split()[:40])
            print(f"Candidate ID: {candidate.get('candidate_id')}")
            print(f"Semantic score: {candidate.get('semantic_score')}")
            print(f"Skills: {candidate.get('skills')}")
            print(f"Experience: {candidate.get('experience')}")
            print(f"Evidence preview: {evidence}...")
            print("-" * 80)

        print("Retrieval script completed successfully.")
    except Exception as exc:
        print(f"Retrieval script failed gracefully: {exc}")
        print("If this is a Chroma or embedding error, run:")
        print("  python tests/test_indexing.py")


if __name__ == "__main__":
    main()
