"""Prompts for candidate ranking."""


DEEP_ANALYSIS_PROMPT = """
You are screening a candidate for a role.
Assess the fit using the requirements and candidate profile.
Return strict JSON:
analysis: short paragraph
recommendation: one of Strong Hire, Hire, Borderline, Reject
risks: list of notable risks

Requirements:
{requirements}

Candidate:
{candidate}
"""
