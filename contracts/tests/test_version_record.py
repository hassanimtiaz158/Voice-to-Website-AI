from datetime import datetime, timezone
import pytest
from pydantic import ValidationError

from contracts.version_record import VersionRecordContract


def test_version_record_contract_valid():
    record = VersionRecordContract(
        project_id="proj-999",
        version_n=1,
        requirements_n=1,
        commit_sha="a1b2c3d4e5f67890123456789abcdef012345678",
        summary="Initial greenfield generation",
        status="verified",
        created_at=datetime.now(timezone.utc),
    )
    assert record.project_id == "proj-999"
    assert record.version_n == 1
    assert record.parent_n is None
    assert record.status == "verified"

    serialized = record.model_dump_json()
    reconstructed = VersionRecordContract.model_validate_json(serialized)
    assert reconstructed.commit_sha == record.commit_sha


def test_version_record_invalid_sha_rejected():
    with pytest.raises(ValidationError):
        VersionRecordContract(
            project_id="proj-999",
            version_n=1,
            requirements_n=1,
            commit_sha="short",  # Must be min 7 chars
            summary="Invalid sha test",
        )
