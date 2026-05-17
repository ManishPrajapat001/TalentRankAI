"""Command-line interface for TalentRankAI."""

from __future__ import annotations

import warnings
from contextlib import contextmanager


@contextmanager
def quiet_startup_warnings():
    """Suppress noisy third-party import warnings during CLI startup."""
    original_showwarning = warnings.showwarning
    warnings.showwarning = lambda *args, **kwargs: None
    try:
        yield
    finally:
        warnings.showwarning = original_showwarning


with quiet_startup_warnings():
    from app.agent.matching_agent import MatchingAgent
    from app.utils.config import ensure_data_dirs


def main() -> None:
    """Run the interactive recruiter CLI."""
    with quiet_startup_warnings():
        ensure_data_dirs()
        agent = MatchingAgent()
    print("TalentRankAI recruiter CLI")
    print("Commands: index, quit")
    print("Example: Find React developers with 3+ years experience")

    while True:
        query = input("\nRecruiter: ").strip()
        if not query:
            continue
        if query.lower() in {"quit", "exit"}:
            print("Agent: Goodbye.")
            break
        if query.lower() == "index":
            print(f"Agent: {agent.index_resumes()}")
            continue

        try:
            response = agent.ask(query)
        except Exception as exc:
            response = f"Something went wrong: {exc}"
        print(f"Agent: {response}")


if __name__ == "__main__":
    main()
