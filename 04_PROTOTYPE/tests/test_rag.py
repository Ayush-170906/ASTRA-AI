def test_retriever_finds_capacity_information(deps):
    chunks = deps.retriever.retrieve("registration capacity maximum seating", top_k=3)
    assert chunks
    assert any("500" in c for c in chunks)


def test_retriever_returns_nothing_for_irrelevant_query(deps):
    chunks = deps.retriever.retrieve("zzz nonexistent unrelated qwerty topic", top_k=3)
    # TF-IDF cosine similarity should score this near zero against our
    # small, topic-specific knowledge base.
    assert len(chunks) <= 1
