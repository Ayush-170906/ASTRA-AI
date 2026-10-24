"""Provider-agnostic LLM interface (TRD section 5).

Deliberately minimal: one method, `generate(prompt) -> str`. Every other
module (agent/decomposer.py, agent/planner.py) talks only to this
interface and parses whatever text comes back -- it never knows or cares
whether the text came from a local model, an API, or the deterministic
fallback in rule_based.py. This is what makes the controller provider-
independent, per the TRD's locked decision.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    name: str = "base"

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Return raw text completion for the given prompt."""
        raise NotImplementedError

    def is_available(self) -> bool:
        """Cheap reachability/config check used by the factory in
        __init__.py to decide whether this provider can be used at all,
        before the app commits to it for the whole session."""
        return True
