"""Local vector store for RAG retrieval (TRD section 8).

DEVIATION FROM THE TRD, DOCUMENTED HERE AND IN README.md:
The TRD's locked decision names FAISS + neural embeddings. This prototype
instead uses scikit-learn's TF-IDF vectorizer with brute-force numpy cosine
similarity. Reasoning: the knowledge base is four short text files (a few
dozen chunks); FAISS's approximate-nearest-neighbor indexing exists to make
million-vector search fast, which is not a problem this prototype has, and
it adds a native-build dependency that is a common source of install
failures on Windows. TF-IDF + brute-force cosine similarity retrieves the
same "top-k relevant chunks for a query" result at this scale, with zero
model download and a pure-Python/numpy dependency chain. The retriever
interface below is the seam where a FAISS + embedding-model backend could
be swapped in later without touching any calling code, if the knowledge
base grows enough to need it.
"""
from __future__ import annotations

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class VectorStore:
    def __init__(self, chunks: list[dict]):
        self.chunks = chunks
        self._texts = [c["text"] for c in chunks]
        self._vectorizer = TfidfVectorizer(stop_words="english")
        self._matrix = self._vectorizer.fit_transform(self._texts) if self._texts else None

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if self._matrix is None or not query.strip():
            return []
        query_vec = self._vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self._matrix)[0]
        ranked_idx = np.argsort(-sims)[:top_k]
        results = []
        for i in ranked_idx:
            if sims[i] <= 0:
                continue
            results.append({**self.chunks[i], "score": float(sims[i])})
        return results
