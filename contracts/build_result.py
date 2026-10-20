from typing import List, Optional
from pydantic import BaseModel, Field


class BuildResultContract(BaseModel):
    success: bool = Field(description="Whether the entire verification pipeline passed")
    exit_code: int = Field(default=0, description="Process exit code of sandbox run")
    tsc_passed: bool = Field(default=False, description="Whether TypeScript compilation succeeded")
    lint_passed: bool = Field(default=False, description="Whether ESLint checks succeeded")
    build_passed: bool = Field(default=False, description="Whether Vite production build succeeded")
    playwright_passed: bool = Field(default=False, description="Whether Playwright smoke tests passed")
    failing_files: List[str] = Field(default_factory=list, description="List of files that caused compilation or test failures")
    raw_error_log: Optional[str] = Field(default=None, description="Captured stderr/stdout from failing build stage")
    preview_url: Optional[str] = Field(default=None, description="Ephemeral preview URL if preview server booted")
    screenshot_s3_key: Optional[str] = Field(default=None, description="S3 storage key of full-page verification screenshot")
