"""Manual integration script for candidate ranking.

Run:
    python tests/test_ranking.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.rag.retriever import CandidateRetriever  # noqa: E402
from app.ranking.reranker import rank_candidates  # noqa: E402
from app.tools.extract_requirements import extract_requirements  # noqa: E402


JD_TEXT = """
Find React developers with 3+ years experience. Must have React, TypeScript,
Node.js, and JavaScript. Nice to have AWS, GraphQL, PostgreSQL, and Docker.
"""


def print_separator(title: str) -> None:
    """Print a readable console section separator."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main() -> None:
    """Retrieve candidates and run the ranking engine."""
    print_separator("Ranking Engine Debug Script")
    print("JD / Query:")
    print(JD_TEXT.strip())

    try:
        print("Extracting requirements...")
        requirements = extract_requirements(JD_TEXT)
        print(json.dumps(requirements, indent=2))

        print("Retrieving candidates...")
        retriever = CandidateRetriever()
        candidates = retriever.retrieve(JD_TEXT, top_k=10)
        print(f"Retrieved candidates: {len(candidates)}")
        if not candidates:
            print("No candidates returned. Try indexing first:")
            print("  python tests/test_indexing.py")
            return

        print("Running reranker...")
        ranked = rank_candidates(candidates, requirements)

        print_separator("Ranked Candidates")
        for index, candidate in enumerate(ranked, start=1):
            explanation = candidate.get("explanation", {})
            print(f"Rank: {index}")
            print(f"Candidate ID: {candidate.get('candidate_id')}")
            print(f"Score: {candidate.get('score')}")
            print(f"Score breakdown: {json.dumps(candidate.get('score_breakdown', {}), indent=2)}")
            print(f"Strengths: {explanation.get('strengths')}")
            print(f"Gaps: {explanation.get('gaps')}")
            print(f"Final recommendation: {candidate.get('final_recommendation')}")
            print("-" * 80)

        print("Ranking script completed successfully.")
    except Exception as exc:
        print(f"Ranking script failed gracefully: {exc}")


if __name__ == "__main__":
    main()
