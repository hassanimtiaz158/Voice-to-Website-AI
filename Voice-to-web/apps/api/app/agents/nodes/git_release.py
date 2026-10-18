from ..state import State
from ._stub import ev


def git_release(s: State):
    """Apply patches to the workspace, branch, commit, push, open PR.
    Also handles pure pull/push requests (intent == "git")."""
    return {"branch": "ai/stub", "events": ev("git_release", "pushed")}
