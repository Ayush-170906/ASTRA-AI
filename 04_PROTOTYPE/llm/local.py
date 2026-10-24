"""Local LLM adapter targeting an Ollama-compatible server (TRD section 6).
Uses plain HTTP so no `ollama` package is required. Not used by default in
this environment because no Ollama server is running here -- see
llm/__init__.py's provider-selection factory and README.md for how to
switch this on when Ollama is available."""
from __future__ import annotations

import json
import urllib.request
import urllib.error

from llm.base import LLMProvider

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1"


class LocalLLM(LLMProvider):
    name = "local-ollama"

    def __init__(self, host: str = DEFAULT_HOST, model: str = DEFAULT_MODEL, timeout: float = 30.0):
        self.host = host.rstrip("/")
        self.model = model
        self.timeout = timeout

    def is_available(self) -> bool:
        try:
            req = urllib.request.Request(f"{self.host}/api/tags")
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                return resp.status == 200
        except (urllib.error.URLError, OSError, TimeoutError):
            return False

    def generate(self, prompt: str) -> str:
        payload = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.host}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return body.get("response", "")
