from ..state import State
from ._stub import ev


def orchestrator(s: State):
    """Classify intent, decide if clarification is needed, reset loop counters,
    merge `answers` back into the request."""
    intent = s.get("intent", "change")
    return {"intent": intent, "debug_attempts": 0, "review_rounds": 0,
            "events": ev("orchestrator", f"intent={intent}")}


def respond(s: State):
    """Final step (orchestrator): explanation, change summary, PR link."""
    return {"summary": "done", "events": ev("respond", "reply sent")}
