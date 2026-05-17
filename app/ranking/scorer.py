"""Hybrid candidate scoring."""

from __future__ import annotations

from app.utils.helper import extract_years, normalize_skill


def score_candidate(candidate: dict, requirements: dict) -> dict:
    """Score a candidate using skill, experience, semantic, and bonus signals."""
    must_have = requirements.get("must_have", [])
    nice_to_have = requirements.get("nice_to_have", [])
    candidate_skills = candidate.get("skills", [])

    skill_match, matched_skills, missing_skills = _skill_match(candidate_skills, must_have)
    nice_bonus, matched_nice = _nice_to_have_bonus(candidate_skills, nice_to_have)
    experience_match = _experience_match(candidate.get("experience", 0), requirements.get("experience", ""))
    semantic = float(candidate.get("semantic_score", 0))

    missing_penalty = min(0.25, 0.05 * len(missing_skills))
    final_score = (
        (skill_match * 0.4)
        + (experience_match * 0.3)
        + (semantic * 0.2)
        + (nice_bonus * 0.1)
        - missing_penalty
    )

    scored = dict(candidate)
    scored.update(
        {
            "score": round(max(0.0, min(1.0, final_score)), 4),
            "score_breakdown": {
                "skill_match": round(skill_match, 4),
                "experience_match": round(experience_match, 4),
                "semantic_similarity": round(semantic, 4),
                "nice_to_have_bonus": round(nice_bonus, 4),
                "missing_skill_penalty": round(missing_penalty, 4),
            },
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "matched_nice_to_have": matched_nice,
        }
    )
    return scored


def _skill_match(candidate_skills: list[str], required_skills: list[str]) -> tuple[float, list[str], list[str]]:
    if not required_skills:
        return 1.0, [], []
    normalized_candidate = {normalize_skill(skill): skill for skill in candidate_skills}
    matched: list[str] = []
    missing: list[str] = []
    for required in required_skills:
        if normalize_skill(required) in normalized_candidate:
            matched.append(required)
        else:
            missing.append(required)
    return len(matched) / len(required_skills), matched, missing


def _nice_to_have_bonus(candidate_skills: list[str], nice_skills: list[str]) -> tuple[float, list[str]]:
    if not nice_skills:
        return 0.0, []
    normalized = {normalize_skill(skill) for skill in candidate_skills}
    matched = [skill for skill in nice_skills if normalize_skill(skill) in normalized]
    return len(matched) / len(nice_skills), matched


def _experience_match(candidate_years: int | float, requirement: str) -> float:
    required_years = extract_years(requirement or "")
    if not required_years:
        return 1.0
    return min(1.0, float(candidate_years or 0) / required_years)
