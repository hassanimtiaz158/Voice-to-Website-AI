from ..state import State
from ._stub import STUB, ev


def tester(s: State):
    """Apply patches in a Docker sandbox copy, run tests / lint / types."""
    if STUB["fail_tests"] > 0:
        STUB["fail_tests"] -= 1
        report = {"passed": False, "failures": ["test_x"], "logs": "boom"}
    else:
        report = {"passed": True, "failures": [], "logs": ""}
    return {"test_report": report, "events": ev("tester", f"passed={report['passed']}")}
