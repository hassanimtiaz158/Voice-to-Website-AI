# Architecture

Browser (React) -> FastAPI (HTTP + SSE) -> Redis queue -> Worker -> LangGraph agents -> Docker sandbox.
Postgres: users, projects, runs, events, LangGraph checkpoints. Vector index: per-project code embeddings.
One graph run per user request (thread_id = run id). Project files live in the workspace volume / object storage, not in graph state.
