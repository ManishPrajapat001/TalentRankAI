"""LangGraph workflow definition."""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.agent import nodes
from app.agent.state import AgentState


def should_refine(state: AgentState) -> str:
    """Loop once when explicit feedback is present."""
    if state.get("feedback") and state.get("iteration", 0) < 1:
        return "feedback_handler"
    return END


def build_graph():
    """Build and compile the hiring workflow graph."""
    graph = StateGraph(AgentState)
    graph.add_node("parse_jd", nodes.parse_jd)
    graph.add_node("extract_requirements", nodes.extract_requirements)
    graph.add_node("retrieve_candidates", nodes.retrieve_candidates)
    graph.add_node("rank_candidates", nodes.rank_candidates)
    graph.add_node("generate_report", nodes.generate_report)
    graph.add_node("feedback_handler", nodes.feedback_handler)

    graph.add_edge(START, "parse_jd")
    graph.add_edge("parse_jd", "extract_requirements")
    graph.add_edge("extract_requirements", "retrieve_candidates")
    graph.add_edge("retrieve_candidates", "rank_candidates")
    graph.add_edge("rank_candidates", "generate_report")
    graph.add_conditional_edges("generate_report", should_refine)
    graph.add_edge("feedback_handler", "extract_requirements")
    return graph.compile()
