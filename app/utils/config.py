"""Configuration helpers for TalentRankAI."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
RESUME_DIR = DATA_DIR / "resumes"
JD_DIR = DATA_DIR / "jds"
CHROMA_DIR = DATA_DIR / "chroma_db"


load_dotenv(ROOT_DIR / ".env")


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "resumes")


def ensure_data_dirs() -> None:
    """Create expected local data directories."""
    for path in (RESUME_DIR, JD_DIR, CHROMA_DIR):
        path.mkdir(parents=True, exist_ok=True)
