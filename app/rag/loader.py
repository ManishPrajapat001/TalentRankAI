"""Resume PDF loading utilities."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


def load_pdf(path: Path) -> str:
    """Load text from one PDF file."""
    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def load_resumes(resume_dir: Path) -> list[dict]:
    """Load all PDF resumes from a directory."""
    resumes: list[dict] = []
    for path in sorted(resume_dir.glob("*.pdf")):
        text = load_pdf(path)
        if text:
            resumes.append({"candidate_id": path.stem, "source": str(path), "text": text})
    return resumes
