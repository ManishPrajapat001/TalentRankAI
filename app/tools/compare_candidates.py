"""Candidate comparison tool."""

from __future__ import annotations


def compare_candidates(candidates: list[dict], limit: int = 3) -> str:
    """Compare top candidates in concise recruiter-friendly text."""
    selected = candidates[:limit]
    if not selected:
        return "No candidates available to compare."

    lines = ["Candidate comparison:"]
    for index, candidate in enumerate(selected, start=1):
        explanation = candidate.get("explanation", {})
        lines.append(
            f"{index}. {candidate.get('candidate_id', 'Unknown')} "
            f"(score {candidate.get('score', 0):.2f}, {candidate.get('final_recommendation', 'Review')})"
        )
        lines.append("   Strengths: " + "; ".join(explanation.get("strengths", [])))
        lines.append("   Gaps: " + "; ".join(explanation.get("gaps", [])))
    return "\n".join(lines)
