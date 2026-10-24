"""Load and chunk the local knowledge base (TRD section 7)."""
from pathlib import Path


def load_and_chunk(knowledge_dir: str | Path, chunk_size: int = 400, overlap: int = 50) -> list[dict]:
    """Split each .txt file into overlapping word-window chunks. Simple by
    design -- the knowledge base is a handful of short files, so paragraph-
    aware chunking would add complexity with no benefit at this scale."""
    knowledge_dir = Path(knowledge_dir)
    chunks: list[dict] = []
    for path in sorted(knowledge_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        words = text.split()
        start = 0
        idx = 0
        while start < len(words):
            window = words[start:start + chunk_size]
            if not window:
                break
            chunk_text = " ".join(window)
            chunks.append({
                "id": f"{path.stem}::chunk{idx}",
                "source": path.name,
                "text": chunk_text,
            })
            idx += 1
            start += chunk_size - overlap
    return chunks
