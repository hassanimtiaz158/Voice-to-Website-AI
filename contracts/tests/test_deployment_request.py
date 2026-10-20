from contracts.deployment_request import DeploymentRequestContract


def test_deployment_request_contract_valid():
    req = DeploymentRequestContract(
        request_id="req-123",
        project_id="proj-123",
        version_id="ver-123",
        status="pending_assignment",
    )
    assert req.request_id == "req-123"
    assert req.status == "pending_assignment"
    assert req.assigned_developer_id is None

    serialized = req.model_dump_json()
    reconstructed = DeploymentRequestContract.model_validate_json(serialized)
    assert reconstructed == req
