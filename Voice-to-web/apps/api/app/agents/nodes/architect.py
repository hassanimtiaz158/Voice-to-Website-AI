from ..state import State
from ._stub import ev


def architect(s: State):
    """Spec + task list with dependencies."""
    task = {"id": "t1", "title": "stub", "files": [], "depends_on": [], "status": "pending"}
    return {"tasks": [task], "events": ev("architect", "plan ready")}
