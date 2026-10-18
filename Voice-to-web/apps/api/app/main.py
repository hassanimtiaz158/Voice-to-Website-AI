from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, github, health, projects, runs
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title="CodePilot API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware, allow_origins=settings.cors_origins,
        allow_methods=["*"], allow_headers=["*"],
    )
    for r in (health, auth, projects, runs, github):
        app.include_router(r.router, prefix="/api/v1")
    return app


app = create_app()
