"""Prompts for report generation."""


REPORT_PROMPT = """
Write a concise recruiter report for the ranked candidates.
Include ranking, score, strengths, gaps, and recommendation.

Requirements:
{requirements}

Ranked candidates:
{ranked_candidates}
"""
