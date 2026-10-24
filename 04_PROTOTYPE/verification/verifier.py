"""Verification engine (FR-12, TRD sections 14 & 23). Compares the task's
declared expected_outcome against the actual tool observation and returns
a structured PASS/FAIL with a human-readable reason -- never a bare
boolean, so the execution trace can always explain *why* a step passed or
failed (seminar Principle 3: never claim success without verification).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from agent.state import SubTask
from tools.registry import ToolResult


@dataclass
class VerificationOutcome:
    verified: bool
    reason: str


def _first_number(text: str) -> Optional[float]:
    m = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(m.group()) if m else None


def verify(task: SubTask, observation: ToolResult,
           force_fail: bool = False, force_fail_reason: str = "") -> VerificationOutcome:
    if force_fail:
        return VerificationOutcome(
            verified=False,
            reason=force_fail_reason or "Demo-forced failure (verification override for retry demonstration)",
        )

    if not observation.success:
        return VerificationOutcome(False, f"Tool reported failure: {observation.message}")

    expected = task.expected_outcome or ""
    observed_text = f"{observation.result} {observation.message}"

    expected_num = _first_number(expected)
    observed_num = _first_number(observed_text)
    if expected_num is not None and observed_num is not None:
        if abs(expected_num - observed_num) < 1e-6:
            return VerificationOutcome(True, f"Observed value {observed_num} matches expected {expected_num}")
        return VerificationOutcome(False, f"Observed value {observed_num} does not match expected {expected_num}")

    # No numeric expectation to check (e.g. retrieval/checklist tasks) --
    # tool-level success plus a non-empty result is the available evidence.
    if observation.result:
        return VerificationOutcome(True, "Tool succeeded and returned a non-empty result")
    return VerificationOutcome(False, "Tool succeeded but returned an empty result")
