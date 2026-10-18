from arq.connections import RedisSettings

from app.agents.graph import build
from app.core.config import settings


async def run_graph(ctx, run_id: str, state: dict):
    """Execute one agent run. Resume paused runs with Command(resume=...) on the same thread_id."""
    graph = ctx["graph"]
    await graph.ainvoke(state, {"configurable": {"thread_id": run_id}})


async def startup(ctx):
    ctx["graph"] = build()  # TODO: PostgresSaver


class WorkerSettings:
    functions = [run_graph]
    on_startup = startup
    redis_settings = RedisSettings.from_dsn(settings.redis_url)
