"""Thin LangGraph nodes for the hiring workflow."""

from __future__ import annotations

from app.agent.state import AgentState
from app.rag.retriever import CandidateRetriever
from app.ranking.reranker import rank_candidates as run_ranking
from app.tools.compare_candidates import compare_candidates as run_compare
from app.tools.extract_requirements import extract_requirements as run_extraction
from app.tools.generate_questions import generate_interview_questions as run_questions


def parse_jd(state: AgentState) -> AgentState:
    """Use explicit JD text, feedback, or user query as search input."""
    jd_text = state.get("jd_text") or state.get("feedback") or state.get("user_query", "")
    return {"jd_text": jd_text, "iteration": state.get("iteration", 0)}


def extract_requirements(state: AgentState) -> AgentState:
    """Extract requirements from the JD."""
    return {"requirements": run_extraction(state.get("jd_text", ""))}


def retrieve_candidates(state: AgentState) -> AgentState:
    """Retrieve matching resume profiles."""
    retriever = CandidateRetriever()
    query = state.get("jd_text", "") + " " + " ".join(state.get("requirements", {}).get("must_have", []))
    return {"retrieved_candidates": retriever.retrieve(query, top_k=10)}


def rank_candidates(state: AgentState) -> AgentState:
    """Rank retrieved candidates."""
    ranked = run_ranking(state.get("retrieved_candidates", []), state.get("requirements", {}))
    return {"ranked_candidates": ranked}


def generate_report(state: AgentState) -> AgentState:
    """Generate a concise final report from ranked candidates."""
    ranked = state.get("ranked_candidates", [])
    if not ranked:
        return {"final_report": "No matching candidates found. Add resumes to data/resumes and run indexing."}

    lines = ["Ranked candidates:"]
    for index, candidate in enumerate(ranked, start=1):
        lines.append(
            f"{index}. {candidate.get('candidate_id', 'Unknown')} - "
            f"score {candidate.get('score', 0):.2f} - "
            f"{candidate.get('final_recommendation', 'Review')}"
        )
        explanation = candidate.get("explanation", {})
        lines.append("   Strengths: " + "; ".join(explanation.get("strengths", [])))
        lines.append("   Gaps: " + "; ".join(explanation.get("gaps", [])))
    return {"final_report": "\n".join(lines)}


def compare_candidates(state: AgentState) -> AgentState:
    """Compare top ranked candidates."""
    return {"comparison_result": run_compare(state.get("ranked_candidates", []), limit=3)}


def generate_interview_questions(state: AgentState) -> AgentState:
    """Generate questions for the top candidate."""
    candidates = state.get("ranked_candidates", [])
    if not candidates:
        return {"interview_questions": []}
    return {"interview_questions": run_questions(candidates[0], state.get("requirements", {}))}


def feedback_handler(state: AgentState) -> AgentState:
    """Update the query with recruiter feedback for another pass."""
    iteration = state.get("iteration", 0) + 1
    feedback = state.get("feedback", "")
    if feedback:
        jd_text = f"{state.get('jd_text', '')}\nAdditional recruiter feedback: {feedback}"
    else:
        jd_text = state.get("jd_text", "")
    return {"jd_text": jd_text, "iteration": iteration}
