"""Provider-selection factory (TRD section 6: "local-first + API fallback").

Order of preference:
1. Local Ollama server, if reachable.
2. Anthropic API, if ANTHROPIC_API_KEY is set.
3. Deterministic rule-based fallback (always available).

Call get_llm_provider() once at app startup; the returned object satisfies
llm.base.LLMProvider for every downstream caller.
"""
from llm.base import LLMProvider
from llm.local import LocalLLM
from llm.api import APIProvider
from llm.rule_based import RuleBasedProvider


def get_llm_provider() -> LLMProvider:
    local = LocalLLM()
    if local.is_available():
        return local

    api = APIProvider()
    if api.is_available():
        return api

    return RuleBasedProvider()


__all__ = ["LLMProvider", "LocalLLM", "APIProvider", "RuleBasedProvider", "get_llm_provider"]
