"""Knowledge-facing tools -- LOW risk, read-only (TRD section 10)."""
from typing import Callable

from tools.registry import Tool, ToolResult
from agent.state import RiskLevel

CHECKLIST_TEMPLATE = [
    "Venue",
    "Registration",
    "Technical setup",
    "Speaker coordination",
    "Feedback collection",
]


def build_search_knowledge_tool(retrieve_fn: Callable[[str, int], list[str]]) -> Tool:
    """Factory so the tool can be wired to whichever retriever instance the
    app constructed, without tools/ importing rag/ at module scope."""

    def _search(query: str, top_k: int = 3) -> ToolResult:
        chunks = retrieve_fn(query, top_k)
        if not chunks:
            return ToolResult(False, [], f"No relevant knowledge found for: {query!r}")
        return ToolResult(True, chunks, f"Retrieved {len(chunks)} relevant chunk(s)")

    return Tool(
        name="search_knowledge",
        description="Retrieve relevant chunks from the local knowledge base for a query.",
        risk_level=RiskLevel.LOW,
        run=_search,
    )


def _generate_checklist(**_ignored) -> ToolResult:
    return ToolResult(True, list(CHECKLIST_TEMPLATE), "Generated standard event checklist")


generate_checklist_tool = Tool(
    name="generate_checklist",
    description="Produce the standard event-preparation checklist.",
    risk_level=RiskLevel.LOW,
    run=_generate_checklist,
)
