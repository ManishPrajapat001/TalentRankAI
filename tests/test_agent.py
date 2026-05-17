"""Manual integration script for the complete LangGraph hiring agent.

Run:
    python tests/test_agent.py
"""

from __future__ import annotations

import sys
import warnings
from contextlib import contextmanager
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))


@contextmanager
def quiet_startup_warnings():
    """Suppress noisy third-party startup warnings in this debug script."""
    original_showwarning = warnings.showwarning
    warnings.showwarning = lambda *args, **kwargs: None
    try:
        yield
    finally:
        warnings.showwarning = original_showwarning


with quiet_startup_warnings():
    from app.agent.matching_agent import MatchingAgent  # noqa: E402


SEARCH_QUERY = "Find React developers with 3 years experience"
REFINEMENT_QUERY = "Only consider candidates with AWS"
COMPARISON_QUERY = "Compare top 3 candidates"
QUESTIONS_QUERY = "Generate interview questions"


def print_separator(title: str) -> None:
    """Print a readable console section separator."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main() -> None:
    """Run the complete conversational agent flow."""
    print_separator("Complete Agent Debug Script")

    try:
        with quiet_startup_warnings():
            agent = MatchingAgent()

        print(f"Search query: {SEARCH_QUERY}")
        final_report = agent.ask(SEARCH_QUERY)
        print_separator("Final Report")
        print(final_report)

        ranked = agent.state.get("ranked_candidates", [])
        print_separator("Ranked Candidate Summary")
        print(f"Ranked candidates: {len(ranked)}")
        if not ranked:
            print("No ranked candidates found. Try indexing first:")
            print("  python tests/test_indexing.py")
            return

        for index, candidate in enumerate(ranked, start=1):
            print(
                f"{index}. {candidate.get('candidate_id')} | "
                f"score={candidate.get('score')} | "
                f"recommendation={candidate.get('final_recommendation')}"
            )

        print_separator("Refinement Query")
        print(f"Recruiter: {REFINEMENT_QUERY}")
        refinement_response = agent.ask(REFINEMENT_QUERY)
        print(refinement_response)

        print_separator("Comparison Query")
        print(f"Recruiter: {COMPARISON_QUERY}")
        comparison_response = agent.ask(COMPARISON_QUERY)
        print(comparison_response)

        print_separator("Interview Question Generation")
        print(f"Recruiter: {QUESTIONS_QUERY}")
        question_response = agent.ask(QUESTIONS_QUERY)
        print(question_response)

        print("Agent script completed successfully.")
    except Exception as exc:
        print(f"Agent script failed gracefully: {exc}")
        print("If retrieval returned nothing, run:")
        print("  python scripts/generate_test_data.py --clean")
        print("  python tests/test_indexing.py")


if __name__ == "__main__":
    main()
