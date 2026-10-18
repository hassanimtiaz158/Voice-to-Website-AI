import operator
from typing import Annotated, Literal, Optional, TypedDict

Intent = Literal["new_project", "change", "bugfix", "explain", "git", "clarify"]


class Task(TypedDict):
    id: str
    title: str
    files: list[str]
    depends_on: list[str]
    status: Literal["pending", "done", "rework"]


class TestReport(TypedDict):
    passed: bool
    failures: list[str]
    logs: str


class Review(TypedDict):
    approved: bool
    issues: list[str]


def merge(a: dict, b: dict) -> dict:  # dict reducer: later writes win per key
    return {**(a or {}), **(b or {})}


class State(TypedDict, total=False):
    # input
    project_id: str
    request: str
    repo: Optional[str]
    # orchestrator
    intent: Intent
    questions: list[str]
    answers: str
    # context agent
    repo_map: str
    relevant_files: Annotated[dict, merge]   # path -> content
    # architect
    spec: str
    tasks: list[Task]
    # coder
    patches: Annotated[dict, merge]          # path -> unified diff (not on disk yet)
    feedback: list[str]
    # tester / debugger
    test_report: TestReport
    debug_attempts: int
    # reviewer
    review: Review
    review_rounds: int
    # human gate
    approval: Literal["approved", "rejected", "cancelled"]
    # git agent
    branch: str
    pr_url: str
    # output + bookkeeping
    summary: str
    events: Annotated[list, operator.add]    # append-only trace streamed to the UI
    tokens_used: int
