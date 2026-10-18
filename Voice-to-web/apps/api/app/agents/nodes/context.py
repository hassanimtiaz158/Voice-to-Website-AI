from ..state import State
from ._stub import ev


def context(s: State):
    """AST + embedding search -> relevant_files, repo_map."""
    return {"events": ev("context", "found relevant files")}
