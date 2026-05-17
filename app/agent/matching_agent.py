"""High-level conversational hiring agent."""

from __future__ import annotations

import re

from app.agent.graph import build_graph
from app.agent.nodes import compare_candidates, generate_interview_questions
from app.agent.state import AgentState
from app.rag.vector_store import ResumeVectorStore


class MatchingAgent:
    """Recruiter-facing agent that keeps conversational state."""

    def __init__(self) -> None:
        self.graph = build_graph()
        self.state: AgentState = {"iteration": 0}

    def index_resumes(self) -> str:
        """Index local PDF resumes into ChromaDB."""
        count = ResumeVectorStore().index_resumes()
        return f"Indexed {count} resume chunks."

    def ask(self, query: str) -> str:
        """Handle a recruiter query."""
        intent = detect_intent(query)
        self.state["user_query"] = query
        self.state["intent"] = intent

        if intent == "compare":
            self.state.update(compare_candidates(self.state))
            return self.state.get("comparison_result", "")

        if intent == "questions":
            self.state.update(generate_interview_questions(self.state))
            questions = self.state.get("interview_questions", [])
            return "\n".join(f"- {question}" for question in questions) or "No candidate selected yet."

        if intent == "why":
            return self._explain_why(query)

        if intent == "refine":
            self.state["feedback"] = query
        else:
            self.state = {"user_query": query, "jd_text": query, "iteration": 0, "intent": intent}

        self.state = self.graph.invoke(self.state)
        return self.state.get("final_report", "")

    def _explain_why(self, query: str) -> str:
        ranked = self.state.get("ranked_candidates", [])
        if len(ranked) < 2:
            return "I need ranked candidates before I can explain a comparison."
        names = [candidate.get("candidate_id", "") for candidate in ranked]
        mentioned = [name for name in names if name and re.search(re.escape(name), query, re.I)]
        selected = [candidate for candidate in ranked if candidate.get("candidate_id") in mentioned]
        if len(selected) < 2:
            selected = ranked[:2]
        first, second = selected[0], selected[1]
        return (
            f"{first.get('candidate_id')} ranked higher than {second.get('candidate_id')} because "
            f"their score was {first.get('score', 0):.2f} vs {second.get('score', 0):.2f}. "
            f"Key strengths: {'; '.join(first.get('explanation', {}).get('strengths', []))}. "
            f"Key gaps for {second.get('candidate_id')}: "
            f"{'; '.join(second.get('explanation', {}).get('gaps', []))}."
        )


def detect_intent(query: str) -> str:
    """Simple intent detection for recruiter conversation."""
    lowered = query.lower()
    if "compare" in lowered:
        return "compare"
    if "interview" in lowered or "questions" in lowered:
        return "questions"
    if lowered.startswith("why") or "rank higher" in lowered:
        return "why"
    if any(token in lowered for token in ["only consider", "must have", "filter", "refine"]):
        return "refine"
    return "search"
