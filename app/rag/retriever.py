"""Structured candidate retrieval."""

from __future__ import annotations

from collections import defaultdict

from app.rag.vector_store import ResumeVectorStore
from app.tools.extract_requirements import extract_resume_profile


class CandidateRetriever:
    """Retrieve and summarize candidates from the vector store."""

    def __init__(self, store: ResumeVectorStore | None = None) -> None:
        self.store = store or ResumeVectorStore()

    def retrieve(self, query: str, top_k: int = 10) -> list[dict]:
        """Return structured candidate data grouped from matching chunks."""
        hits = self.store.search(query, top_k=top_k)
        grouped: dict[str, list[dict]] = defaultdict(list)
        for hit in hits:
            grouped[hit["candidate_id"]].append(hit)

        candidates: list[dict] = []
        for candidate_id, candidate_hits in grouped.items():
            combined_text = "\n".join(hit["text"] for hit in candidate_hits)
            profile = extract_resume_profile(combined_text, candidate_id)
            profile["candidate_id"] = profile.get("candidate_id") or candidate_id
            profile["source"] = candidate_hits[0].get("source", "")
            profile["semantic_score"] = round(
                max(hit["semantic_score"] for hit in candidate_hits), 4
            )
            profile["evidence"] = combined_text[:1500]
            candidates.append(profile)

        candidates.sort(key=lambda item: item.get("semantic_score", 0), reverse=True)
        return candidates
