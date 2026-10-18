# CodePilot: multi-agent coding assistant

Monorepo: FastAPI + LangGraph backend, React (Vite, TypeScript) frontend.

```
apps/api       FastAPI, agents (LangGraph), sandbox, workers, evals
apps/web       React UI
packages/      shared code (generated API client)
infra/         sandbox image, deploy manifests, nginx
docs/          architecture, agent flow, ADRs
```

## Run
```
cp .env.example .env      # add ANTHROPIC_API_KEY (+ GITHUB_TOKEN)
make dev                  # api :8000, web :5173, postgres, redis, worker
```
Health check: http://localhost:8000/api/v1/health

## Status
Agents are stubs that wire the full graph (see `apps/api/app/agents/`).
Implement them one by one; routing and state are already in place.
Suggested order: context + coder (patches) -> sandbox + tester/debugger -> orchestrator -> auth/GitHub App -> evals.
