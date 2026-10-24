"""Retriever facade (TRD section 9): loads the knowledge base once and
exposes a single retrieve(query, top_k) -> list[str] function, which is
what tools.knowledge_lookup wires into the search_knowledge tool."""
from pathlib import Path

from rag.loader import load_and_chunk
from rag.vectorstore import VectorStore

DEFAULT_TOP_K = 3


class Retriever:
    def __init__(self, knowledge_dir: str | Path):
        self.chunks = load_and_chunk(knowledge_dir)
        self.store = VectorStore(self.chunks)

    def retrieve(self, query: str, top_k: int = DEFAULT_TOP_K) -> list[str]:
        hits = self.store.search(query, top_k=top_k)
        return [f"[{h['source']}] {h['text']}" for h in hits]

    def retrieve_detailed(self, query: str, top_k: int = DEFAULT_TOP_K) -> list[dict]:
        return self.store.search(query, top_k=top_k)
