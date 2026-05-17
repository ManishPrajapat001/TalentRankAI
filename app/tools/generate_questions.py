"""Interview question generation."""

from __future__ import annotations

from app.utils.llm import llm


def generate_interview_questions(candidate: dict, requirements: dict, count: int = 6) -> list[str]:
    """Generate role-specific interview questions for a candidate."""
    prompt = f"""
Generate {count} interview questions for this candidate and role.
Focus on required skills, experience gaps, and practical scenario questions.
Return one question per line.

Requirements:
{requirements}

Candidate:
{candidate}
"""
    response = llm.complete(prompt)
    questions = [line.lstrip("-0123456789. ").strip() for line in response.splitlines() if line.strip()]
    if questions:
        return questions[:count]
    skills = ", ".join(requirements.get("must_have", [])[:3]) or "the role requirements"
    return [
        f"Walk me through a project where you used {skills}.",
        "What tradeoffs did you make in your most relevant recent project?",
        "Which part of this role would require the most ramp-up for you?",
        "How do you validate the quality of your work before release?",
        "Describe a difficult technical decision and how you handled it.",
        "What would you want to learn in the first 30 days in this role?",
    ][:count]
