"""LLM-backed extraction tools."""

from __future__ import annotations

import re

from app.prompts.extraction_prompts import REQUIREMENT_EXTRACTION_PROMPT, RESUME_EXTRACTION_PROMPT
from app.utils.helper import extract_years, safe_json_loads, unique_preserve_order
from app.utils.llm import llm


COMMON_SKILLS = [
    "Python", "Java", "JavaScript", "TypeScript", "React", "Node.js", "AWS",
    "Azure", "GCP", "Docker", "Kubernetes", "SQL", "PostgreSQL", "MongoDB",
    "LangChain", "LangGraph", "Machine Learning", "NLP", "FastAPI", "Django",
]


def extract_requirements(jd: str) -> dict:
    """Extract structured hiring requirements from a job description."""
    response = llm.complete(REQUIREMENT_EXTRACTION_PROMPT.format(jd=jd))
    parsed = safe_json_loads(response, {})
    if parsed:
        return {
            "must_have": parsed.get("must_have", []),
            "nice_to_have": parsed.get("nice_to_have", []),
            "experience": parsed.get("experience", ""),
            "education": parsed.get("education", ""),
        }
    return _fallback_requirements(jd)


def extract_resume_profile(resume_text: str, filename: str) -> dict:
    """Extract structured candidate data from resume text."""
    prompt = RESUME_EXTRACTION_PROMPT.format(filename=filename, resume_text=resume_text[:6000])
    response = llm.complete(prompt)
    parsed = safe_json_loads(response, {})
    if parsed:
        return {
            "candidate_id": parsed.get("candidate_id") or filename,
            "skills": parsed.get("skills", []),
            "experience": int(parsed.get("experience") or 0),
            "summary": parsed.get("summary", ""),
        }
    return _fallback_resume_profile(resume_text, filename)


def _fallback_requirements(text: str) -> dict:
    found = [skill for skill in COMMON_SKILLS if re.search(rf"\b{re.escape(skill)}\b", text, re.I)]
    return {
        "must_have": unique_preserve_order(found[:6]),
        "nice_to_have": unique_preserve_order(found[6:10]),
        "experience": f"{extract_years(text)}+ years" if extract_years(text) else "",
        "education": "Not specified",
    }


def _fallback_resume_profile(text: str, filename: str) -> dict:
    skills = [skill for skill in COMMON_SKILLS if re.search(rf"\b{re.escape(skill)}\b", text, re.I)]
    summary = " ".join(text.split()[:45])
    return {
        "candidate_id": filename,
        "skills": unique_preserve_order(skills),
        "experience": extract_years(text),
        "summary": summary,
    }
