"""Ranking explanation helpers."""

from __future__ import annotations


def explain_candidate(candidate: dict) -> dict:
    """Generate a readable ranking explanation."""
    strengths: list[str] = []
    gaps: list[str] = []

    if candidate.get("matched_skills"):
        strengths.append("Matches required skills: " + ", ".join(candidate["matched_skills"]))
    if candidate.get("matched_nice_to_have"):
        strengths.append("Adds nice-to-have skills: " + ", ".join(candidate["matched_nice_to_have"]))
    if candidate.get("score_breakdown", {}).get("experience_match", 0) >= 1:
        strengths.append("Meets or exceeds the experience requirement")
    if candidate.get("semantic_score", 0) >= 0.75:
        strengths.append("Resume is semantically close to the role")

    if candidate.get("missing_skills"):
        gaps.append("Missing: " + ", ".join(candidate["missing_skills"]))
    if candidate.get("score_breakdown", {}).get("experience_match", 0) < 1:
        gaps.append("Experience may be below the stated requirement")

    score = candidate.get("score", 0)
    if score >= 0.8:
        recommendation = "Strong Hire"
    elif score >= 0.65:
        recommendation = "Hire"
    elif score >= 0.45:
        recommendation = "Borderline"
    else:
        recommendation = "Reject"

    return {
        "strengths": strengths or ["Relevant background found in resume"],
        "gaps": gaps or ["No major gaps detected from available evidence"],
        "recommendation": recommendation,
    }
