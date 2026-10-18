from ..state import State
from ._stub import ev


def coder(s: State):
    """Implement pending/rework tasks -> patches (diffs). If `tasks` is empty (bugfix path),
    derive one task from the request. Consumes `feedback`."""
    return {"patches": {"app.py": "--- stub diff ---"}, "events": ev("coder", "patches written")}
