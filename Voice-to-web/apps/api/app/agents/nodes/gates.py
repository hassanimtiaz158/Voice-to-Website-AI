from langgraph.types import interrupt

from ..state import State
from ._stub import ev


def ask_user(s: State):
    answers = interrupt({"type": "clarify", "questions": s.get("questions", []),
                         "test_report": s.get("test_report")})
    return {"answers": answers, "events": ev("ask_user", "user answered")}


def approval_gate(s: State):
    decision = interrupt({"type": "approve_diff", "patches": s.get("patches", {}),
                          "review": s.get("review"), "tests": s.get("test_report")})
    out = {"approval": decision["action"], "events": ev("approval_gate", decision["action"])}
    if decision["action"] == "rejected":
        out["feedback"] = [decision.get("feedback", "")]
        out["review_rounds"] = 0
        out["debug_attempts"] = 0
    return out
