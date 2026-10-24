import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from agent.controller import Dependencies
from llm.rule_based import RuleBasedProvider
from rag.retriever import Retriever
from tools.registry import ToolRegistry
from tools.calculator import calculate_capacity_tool
from tools.knowledge_lookup import build_search_knowledge_tool, generate_checklist_tool
from tools.mock_notification import mock_send_announcement_tool

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"


@pytest.fixture
def deps() -> Dependencies:
    retriever = Retriever(KNOWLEDGE_DIR)
    registry = ToolRegistry()
    registry.register(calculate_capacity_tool)
    registry.register(generate_checklist_tool)
    registry.register(build_search_knowledge_tool(retriever.retrieve))
    registry.register(mock_send_announcement_tool)
    return Dependencies(llm=RuleBasedProvider(), retriever=retriever, registry=registry)
