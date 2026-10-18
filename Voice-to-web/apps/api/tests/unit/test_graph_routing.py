from langgraph.types import Command

from app.agents.graph import build
from app.agents.nodes._stub import STUB

APPROVE = {"action": "approved"}


def run(intent, resumes=(), fail=0, reject=0, tid="t"):
    STUB.update(fail_tests=fail, reject_reviews=reject)
    g, cfg = build(), {"configurable": {"thread_id": tid}}
    out = g.invoke({"request": "x", "intent": intent}, cfg)
    for r in resumes:
        out = g.invoke(Command(resume=r), cfg)
    return [e["agent"] for e in out["events"]]


def test_change_happy_path():
    assert run("change", [APPROVE]) == ["orchestrator", "context", "architect", "coder", "tester",
                                        "reviewer", "approval_gate", "git_release", "respond"]


def test_bugfix_skips_architect():
    assert "architect" not in run("bugfix", [APPROVE])


def test_explain_only_reads():
    assert run("explain") == ["orchestrator", "context", "respond"]


def test_debug_loop():
    path = run("change", [APPROVE], fail=2)
    assert path.count("debugger") == 2


def test_review_loop():
    assert run("change", [APPROVE], reject=1).count("coder") == 2


def test_user_cancel():
    assert run("change", [{"action": "cancelled"}])[-1] == "respond"
