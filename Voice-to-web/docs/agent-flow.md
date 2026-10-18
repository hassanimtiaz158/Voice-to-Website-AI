# Agent flow

orchestrator -> (ask_user | architect | context | git_release)
context      -> (respond | architect | coder)
architect    -> coder -> tester
tester       -> reviewer | debugger (<=3) | ask_user (escalate)
debugger     -> tester
reviewer     -> approval_gate | coder (<=2 rounds)
approval_gate-> git_release | coder | respond
git_release  -> respond -> END

Source of truth: apps/api/app/agents/graph.py
