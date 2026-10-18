from pydantic import BaseModel


class RunCreate(BaseModel):
    project_id: str
    request: str


class RunResume(BaseModel):
    action: str  # approved | rejected | cancelled, or free text for clarifications
    feedback: str = ""
