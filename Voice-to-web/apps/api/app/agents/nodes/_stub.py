"""Test hooks for the stub agents. Delete when real agents land."""
STUB = {"fail_tests": 0, "reject_reviews": 0}


def ev(agent: str, text: str = "") -> list:
    return [{"agent": agent, "text": text}]
