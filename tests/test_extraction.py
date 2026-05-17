"""Manual integration script for requirement extraction.

Run:
    python tests/test_extraction.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.tools.extract_requirements import extract_requirements  # noqa: E402


SAMPLE_JD = """
We are hiring a React Developer with 3+ years of experience building production
web applications. Must have React, TypeScript, Node.js, and strong JavaScript
fundamentals. Nice to have AWS, GraphQL, PostgreSQL, Docker, and experience
working with product designers. Bachelor's degree preferred.
"""


def print_separator(title: str) -> None:
    """Print a readable console section separator."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main() -> None:
    """Run extraction against a sample job description."""
    print_separator("Requirement Extraction Debug Script")
    print("Sample JD:")
    print(SAMPLE_JD.strip())

    try:
        requirements = extract_requirements(SAMPLE_JD)
        print_separator("Extracted Requirements")
        print(json.dumps(requirements, indent=2))

        print_separator("Structure Check")
        must_have_ok = isinstance(requirements.get("must_have"), list)
        nice_to_have_ok = isinstance(requirements.get("nice_to_have"), list)
        print(f"must_have is list: {must_have_ok}")
        print(f"nice_to_have is list: {nice_to_have_ok}")
        print(f"experience: {requirements.get('experience')}")
        print(f"education: {requirements.get('education')}")

        if not must_have_ok or not nice_to_have_ok:
            print("Result shape is not valid. Check extraction prompt or fallback parsing.")
            return

        print("Extraction script completed successfully.")
    except Exception as exc:
        print(f"Extraction script failed gracefully: {exc}")


if __name__ == "__main__":
    main()
