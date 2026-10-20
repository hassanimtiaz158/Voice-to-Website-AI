from typing import List
from pydantic import BaseModel, Field


class SingleFileDiff(BaseModel):
    path: str = Field(min_length=1, description="Relative path to file being edited")
    original_hash: str = Field(min_length=1, description="SHA256 hex hash of file before modification")
    unified_diff: str = Field(min_length=1, description="Unified diff patch text")
    summary_of_change: str = Field(min_length=1, description="Concise human-readable explanation of change")


class FileEditContract(BaseModel):
    project_id: str = Field(min_length=1)
    version_n: int = Field(ge=1, description="Resulting target version number")
    trigger_message_id: str = Field(min_length=1, description="ID of user message triggering this edit")
    diffs: List[SingleFileDiff] = Field(min_length=1, description="List of single-file diffs to apply")
