from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict




class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "dev"  # dev | staging | production | test
    database_url: str = "postgresql+asyncpg://codepilot:codepilot@localhost:5432/codepilot"
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 15
    refresh_token_days: int = 7
    # "lax" works when frontend and API share a registrable domain (app.x.com + api.x.com, or localhost).
    # Use "none" only if they are on different domains (needs HTTPS).
    cookie_samesite: Literal["lax", "strict", "none"] = "lax"
    cors_origins: list[str] = ["http://localhost:5173"]

    @model_validator(mode="after")
    def _require_real_secret(self):
        if self.env in ("staging", "production") and (
            self.jwt_secret == "" or len(self.jwt_secret) < 32
        ):
            raise ValueError("JWT_SECRET must be a random value of 32+ chars in staging/production")
        return self


settings = Settings()