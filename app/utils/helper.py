"""Small shared helper functions."""

from __future__ import annotations

import json
import re
from typing import Any


def safe_json_loads(text: str, default: Any) -> Any:
    """Parse JSON from an LLM response, tolerating fenced code blocks."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return default
        return default


def normalize_skill(skill: str) -> str:
    """Normalize a skill for lightweight matching."""
    return re.sub(r"[^a-z0-9+#.]", "", skill.lower())


def extract_years(text: str) -> int:
    """Extract a rough years-of-experience value from free text."""
    matches = re.findall(r"(\d+)\+?\s*(?:years|yrs|year)", text.lower())
    return max([int(value) for value in matches], default=0)


def unique_preserve_order(values: list[str]) -> list[str]:
    """Return unique non-empty strings while preserving order."""
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        cleaned = value.strip()
        key = cleaned.lower()
        if cleaned and key not in seen:
            output.append(cleaned)
            seen.add(key)
    return output
