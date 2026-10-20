from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class VersionRecordContract(BaseModel):
    project_id: str = Field(min_length=1)
    version_n: int = Field(ge=1, description="Version sequence number (1, 2, ... N)")
    parent_n: Optional[int] = Field(default=None, description="Previous version sequence number, if any")
    requirements_n: int = Field(ge=1, description="Associated requirements version sequence")
    trigger_message_id: Optional[str] = Field(default=None, description="Message ID triggering this version")
    commit_sha: str = Field(min_length=7, max_length=40, description="Git commit SHA-1")
    summary: str = Field(min_length=1, description="Summary of changes included in this version")
    status: Literal["draft", "verified", "failed", "rolled_back"] = Field(
        default="draft", description="Operational status of this version"
    )
    created_at: Optional[datetime] = Field(default=None, description="Timestamp when version was created")
