"""LangGraph state definition."""

from __future__ import annotations

from typing import TypedDict


class AgentState(TypedDict, total=False):
    """State tracked across the hiring agent workflow."""

    user_query: str
    jd_text: str
    requirements: dict
    retrieved_candidates: list[dict]
    ranked_candidates: list[dict]
    comparison_result: str
    interview_questions: list[str]
    final_report: str
    feedback: str
    iteration: int
    intent: str
