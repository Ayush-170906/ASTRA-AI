"""Risk classification (TRD sections 11-12). Risk is a static property of
the TOOL being invoked, declared on the tool itself in the registry -- this
module just looks it up and exposes the one rule that matters for the whole
prototype: HIGH risk always requires human approval before execution, no
tool-level override, no bypass path.
"""
from agent.state import RiskLevel


def requires_approval(risk: RiskLevel) -> bool:
    """The single safety rule of this prototype (seminar Principle 1):
    never execute a HIGH-risk action before approval. There is no other
    function anywhere in this codebase that is allowed to send a HIGH-risk
    action to the executor -- every call path goes through here first."""
    return risk == RiskLevel.HIGH
