from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "dev"
    database_url: str = "postgresql+asyncpg://codepilot:codepilot@localhost:5432/codepilot"
    redis_url: str = "redis://localhost:6379/0"
    anthropic_api_key: str = ""
    model: str = "claude-sonnet-5-5"
    github_token: str = ""
    workspace_root: str = "/data/workspaces"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:8080"]


settings = Settings()
