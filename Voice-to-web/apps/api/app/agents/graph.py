"""Graph wiring + routers. Agent logic lives in nodes/."""
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from .nodes import (
    approval_gate,
    architect,
    ask_user,
    coder,
    context,
    debugger,
    git_release,
    orchestrator,
    respond,
    reviewer,
    tester,
)
from .state import State

MAX_DEBUG = 3    # tester <-> debugger loops
MAX_REVIEW = 2   # reviewer -> coder loops


def after_orchestrator(s: State) -> str:
    return {"clarify": "ask_user", "new_project": "architect", "git": "git_release",
            "explain": "context", "change": "context", "bugfix": "context"}[s["intent"]]


def after_context(s: State) -> str:
    return {"explain": "respond", "change": "architect", "bugfix": "coder"}[s["intent"]]


def after_tester(s: State) -> str:
    if s["test_report"]["passed"]:
        return "reviewer"
    if s.get("debug_attempts", 0) < MAX_DEBUG:
        return "debugger"
    return "ask_user"  # retries exhausted: escalate to the user


def after_reviewer(s: State) -> str:
    if s["review"]["approved"] or s.get("review_rounds", 0) >= MAX_REVIEW:
        return "approval_gate"
    return "coder"


def after_approval(s: State) -> str:
    return {"approved": "git_release", "rejected": "coder", "cancelled": "respond"}[s["approval"]]


def build(checkpointer=None):
    """Pass a PostgresSaver in production so runs survive restarts and interrupts resume."""
    g = StateGraph(State)
    for name, fn in [("orchestrator", orchestrator), ("ask_user", ask_user), ("context", context),
                     ("architect", architect), ("coder", coder), ("tester", tester),
                     ("debugger", debugger), ("reviewer", reviewer),
                     ("approval_gate", approval_gate), ("git_release", git_release),
                     ("respond", respond)]:
        g.add_node(name, fn)

    g.add_edge(START, "orchestrator")
    g.add_conditional_edges("orchestrator", after_orchestrator,
                            ["ask_user", "architect", "git_release", "context"])
    g.add_edge("ask_user", "orchestrator")
    g.add_conditional_edges("context", after_context, ["respond", "architect", "coder"])
    g.add_edge("architect", "coder")
    g.add_edge("coder", "tester")
    g.add_conditional_edges("tester", after_tester, ["reviewer", "debugger", "ask_user"])
    g.add_edge("debugger", "tester")
    g.add_conditional_edges("reviewer", after_reviewer, ["approval_gate", "coder"])
    g.add_conditional_edges("approval_gate", after_approval, ["git_release", "coder", "respond"])
    g.add_edge("git_release", "respond")
    g.add_edge("respond", END)
    return g.compile(checkpointer=checkpointer or MemorySaver())
