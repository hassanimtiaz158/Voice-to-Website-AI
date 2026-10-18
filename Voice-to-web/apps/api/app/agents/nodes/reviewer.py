from ..state import State
from ._stub import STUB, ev


def reviewer(s: State):
    """Correctness, security, style, unrelated changes."""
    if STUB["reject_reviews"] > 0:
        STUB["reject_reviews"] -= 1
        review = {"approved": False, "issues": ["naming"]}
    else:
        review = {"approved": True, "issues": []}
    return {"review": review, "review_rounds": s.get("review_rounds", 0) + 1,
            "feedback": review["issues"], "events": ev("reviewer", f"approved={review['approved']}")}
