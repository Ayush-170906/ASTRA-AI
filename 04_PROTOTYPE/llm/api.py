"""API-based LLM adapter (TRD section 6, "API fallback"). Targets the
Anthropic Messages API by default since no provider was specified in the
seminar's open items. Reads the key ONLY from the environment (SR-01/02/03:
never hardcoded, never logged, never committed) -- if ANTHROPIC_API_KEY is
not set, is_available() returns False and the factory in llm/__init__.py
falls through to the next provider.
"""
from __future__ import annotations

import json
import os
import urllib.request
import urllib.error

from llm.base import LLMProvider

DEFAULT_MODEL = "claude-3-5-haiku-20241022"
API_URL = "https://api.anthropic.com/v1/messages"


class APIProvider(LLMProvider):
    name = "api-anthropic"

    def __init__(self, model: str = DEFAULT_MODEL, timeout: float = 30.0):
        self.model = model
        self.timeout = timeout
        self.api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set; APIProvider is unavailable.")
        payload = json.dumps({
            "model": self.model,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }).encode("utf-8")
        req = urllib.request.Request(
            API_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        parts = body.get("content", [])
        return "".join(p.get("text", "") for p in parts)
