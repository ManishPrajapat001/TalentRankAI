"""Candidate reranking and multi-round screening."""

from __future__ import annotations

from app.prompts.ranking_prompts import DEEP_ANALYSIS_PROMPT
from app.ranking.explainability import explain_candidate
from app.ranking.scorer import score_candidate
from app.utils.helper import safe_json_loads
from app.utils.llm import llm


def rank_candidates(candidates: list[dict], requirements: dict, top_n: int = 10) -> list[dict]:
    """Run hybrid ranking plus optional LLM analysis for top candidates."""
    round_one = candidates[:top_n]
    scored = [score_candidate(candidate, requirements) for candidate in round_one]
    scored.sort(key=lambda item: item.get("score", 0), reverse=True)

    for candidate in scored:
        candidate["explanation"] = explain_candidate(candidate)

    for candidate in scored[:5]:
        analysis = _deep_analysis(candidate, requirements)
        if analysis:
            candidate["llm_analysis"] = analysis.get("analysis", "")
            candidate["risks"] = analysis.get("risks", [])
            candidate["final_recommendation"] = analysis.get(
                "recommendation",
                candidate["explanation"]["recommendation"],
            )
        else:
            candidate["final_recommendation"] = candidate["explanation"]["recommendation"]

    for candidate in scored[5:]:
        candidate["final_recommendation"] = candidate["explanation"]["recommendation"]
    return scored


def _deep_analysis(candidate: dict, requirements: dict) -> dict:
    prompt = DEEP_ANALYSIS_PROMPT.format(requirements=requirements, candidate=candidate)
    response = llm.complete(prompt)
    return safe_json_loads(response, {})
