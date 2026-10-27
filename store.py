import hashlib

import chromadb
from sentence_transformers import SentenceTransformer

from config import CHROMA_DIR, EMBED_MODEL
from models import Chunk, Hit


class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer(EMBED_MODEL)
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.col = client.get_or_create_collection(
            "documind", metadata={"hnsw:space": "cosine"}
        )

    def _embed(self, texts):
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def add(self, chunks: list[Chunk]) -> int:
        if not chunks:
            return 0
        ids = [
            hashlib.sha1(f"{c.source}|{c.page}|{c.text}".encode()).hexdigest()
            for c in chunks
        ]  # content-hash ids make re-uploads idempotent
        self.col.upsert(
            ids=ids,
            embeddings=self._embed([c.text for c in chunks]),
            documents=[c.text for c in chunks],
            metadatas=[{"source": c.source, "page": c.page} for c in chunks],
        )
        return len(chunks)

    def search(self, query: str, k: int) -> list[Hit]:
        if self.col.count() == 0:
            return []
        r = self.col.query(query_embeddings=self._embed([query]), n_results=k)
        return [
            Hit(text=d, source=m["source"], page=m["page"], score=1 - dist)
            for d, m, dist in zip(
                r["documents"][0], r["metadatas"][0], r["distances"][0]
            )
        ]

    def sources(self) -> list[str]:
        metas = self.col.get(include=["metadatas"])["metadatas"]
        return sorted({m["source"] for m in metas})

    def delete_source(self, name: str) -> None:
        self.col.delete(where={"source": name})
