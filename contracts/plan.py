from typing import List, Literal
from pydantic import BaseModel, Field


class FileAction(BaseModel):
    path: str = Field(description="Relative file path, e.g. src/components/Hero.tsx")
    role: Literal["component", "content", "page", "style", "config", "api"] = Field(
        description="Architectural role of the file"
    )
    action: Literal["create", "modify", "delete"] = Field(
        description="Action to perform on this file"
    )
    description: str = Field(min_length=1, description="Exact purpose of this file")
    imports: List[str] = Field(default_factory=list, description="List of import paths")
    exports: List[str] = Field(default_factory=list, description="List of exported symbol names")


class PlanContract(BaseModel):
    project_id: str = Field(min_length=1)
    stack_profile: Literal["vite-react-tailwind", "static-html"] = Field(
        default="vite-react-tailwind", description="Pinned technology stack"
    )
    files: List[FileAction] = Field(min_length=1, description="Dependency-ordered list of file actions")
    estimated_tokens: int = Field(default=0, ge=0, description="Estimated token budget for this generation")
