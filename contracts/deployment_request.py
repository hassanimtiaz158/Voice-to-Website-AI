from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class DeploymentRequestContract(BaseModel):
    request_id: str = Field(min_length=1, description="Unique deployment request ID")
    project_id: str = Field(min_length=1, description="Associated project ID")
    version_id: str = Field(min_length=1, description="Version ID being deployed")
    status: Literal[
        "pending_assignment",
        "assigned",
        "quoted",
        "in_progress",
        "live_confirmed",
        "canceled",
    ] = Field(default="pending_assignment", description="Marketplace ticket status")
    assigned_developer_id: Optional[str] = Field(default=None, description="Assigned developer user ID")
    chat_room_id: Optional[str] = Field(default=None, description="Marketplace chat room UUID")
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")
