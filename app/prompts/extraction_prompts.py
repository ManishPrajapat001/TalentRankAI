"""Prompts for job description and resume extraction."""


REQUIREMENT_EXTRACTION_PROMPT = """
Extract hiring requirements from this job description.
Return strict JSON with these keys:
must_have: list of required skills
nice_to_have: list of optional skills
experience: concise experience requirement
education: concise education requirement

Job description:
{jd}
"""


RESUME_EXTRACTION_PROMPT = """
Extract candidate information from this resume text.
Return strict JSON with these keys:
candidate_id: candidate name if present, otherwise filename stem
skills: list of skills
experience: integer estimated years of professional experience
summary: two sentence professional summary

Filename fallback:
{filename}

Resume:
{resume_text}
"""
