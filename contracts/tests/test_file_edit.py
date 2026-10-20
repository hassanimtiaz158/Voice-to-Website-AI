import pytest
from pydantic import ValidationError

from contracts.file_edit import FileEditContract, SingleFileDiff


def test_file_edit_contract_valid():
    diff = SingleFileDiff(
        path="data/site.json",
        original_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        unified_diff="--- data/site.json\n+++ data/site.json\n@@ -5,1 +5,1 @@\n-  \"hero_title\": \"Old Title\"\n+  \"hero_title\": \"New Title\"",
        summary_of_change="Updated hero title copy",
    )

    edit = FileEditContract(
        project_id="proj-789",
        version_n=2,
        trigger_message_id="msg-abc",
        diffs=[diff],
    )

    assert edit.project_id == "proj-789"
    assert edit.version_n == 2
    assert len(edit.diffs) == 1
    assert edit.diffs[0].path == "data/site.json"

    serialized = edit.model_dump_json()
    reconstructed = FileEditContract.model_validate_json(serialized)
    assert reconstructed == edit


def test_file_edit_contract_empty_diffs_rejected():
    with pytest.raises(ValidationError):
        FileEditContract(
            project_id="proj-789",
            version_n=2,
            trigger_message_id="msg-abc",
            diffs=[],
        )
