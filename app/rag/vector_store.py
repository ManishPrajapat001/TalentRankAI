"""ChromaDB vector store integration."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import chromadb

from app.rag.chunker import chunk_text
from app.rag.embedder import embed_texts
from app.rag.loader import load_resumes
from app.utils import config


class ResumeVectorStore:
    """Persistent Chroma collection for resume chunks."""

    def __init__(self, persist_dir: Path | None = None, collection_name: str | None = None) -> None:
        config.ensure_data_dirs()
        self.client = chromadb.PersistentClient(path=str(persist_dir or config.CHROMA_DIR))
        self.collection = self.client.get_or_create_collection(
            name=collection_name or config.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    def index_resumes(self, resume_dir: Path | None = None) -> int:
        """Load and index PDF resumes. Returns number of chunks indexed."""
        resumes = load_resumes(resume_dir or config.RESUME_DIR)
        return self.index_documents(resumes)

    def index_documents(self, resumes: list[dict]) -> int:
        """Index preloaded resume documents. Returns number of chunks indexed."""
        documents: list[str] = []
        metadatas: list[dict] = []
        ids: list[str] = []

        for resume in resumes:
            candidate_id = resume.get("candidate_id") or resume.get("id") or "unknown"
            for index, chunk in enumerate(chunk_text(resume["text"])):
                documents.append(chunk)
                metadatas.append(
                    {
                        "candidate_id": candidate_id,
                        "source": resume.get("source", ""),
                        "chunk_index": index,
                    }
                )
                ids.append(f"{candidate_id}-{index}-{uuid4().hex[:8]}")

        if not documents:
            return 0

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embed_texts(documents),
            metadatas=metadatas,
        )
        return len(documents)

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        """Run semantic search over resume chunks."""
        embeddings = embed_texts([query])
        if not embeddings:
            return []
        results = self.collection.query(
            query_embeddings=embeddings,
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        output: list[dict] = []
        for doc, metadata, distance in zip(
            results.get("documents", [[]])[0],
            results.get("metadatas", [[]])[0],
            results.get("distances", [[]])[0],
        ):
            output.append(
                {
                    "candidate_id": metadata.get("candidate_id", "unknown"),
                    "source": metadata.get("source", ""),
                    "text": doc,
                    "semantic_score": round(max(0.0, 1.0 - float(distance)), 4),
                }
            )
        return output
