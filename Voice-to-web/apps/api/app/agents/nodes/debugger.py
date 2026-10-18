from ..state import State
from ._stub import ev


def debugger(s: State):
    """Read failures / logs, fix patches."""
    return {"debug_attempts": s.get("debug_attempts", 0) + 1,
            "events": ev("debugger", "fix attempt")}
