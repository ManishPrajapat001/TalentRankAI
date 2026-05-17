"""Sentence-transformers embedding wrapper."""

from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.utils.config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load the embedding model once per process."""
    return SentenceTransformer(EMBEDDING_MODEL)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts."""
    if not texts:
        return []
    vectors = get_embedding_model().encode(texts, normalize_embeddings=True)
    return vectors.tolist()
