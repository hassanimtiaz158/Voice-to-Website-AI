# Phase 1: Repository Foundation, Monorepo Setup & Shared Contracts

---

### Navigation
- **Current Phase:** Phase 1 of 20
- **Previous Phase:** None (Kickoff)
- **Next Phase:** [Phase 2: PostgreSQL with pgvector Schema & Database Migrations](file:///d:/VoicetoAI/docs/PHASES/PHASE_02_Postgres_and_pgvector.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [FOLDER_STRUCTURE.md](file:///d:/VoicetoAI/docs/FOLDER_STRUCTURE.md), [REPOSITORY_STRATEGY.md](file:///d:/VoicetoAI/docs/REPOSITORY_STRATEGY.md)

---

### Objective
Establish the project repository structure, tooling, CI linting gates, and immutable Pydantic V2 data contracts that define all inter-agent and inter-service boundaries.

### Business Goal
Ensure zero integration drift between the four engineering team members from day one by establishing clear API boundaries.

### Technical Goal
Deploy a monorepo with strict TypeScript and Python linting, pre-commit hooks, and compile-time contract validation.

### Features Included
- Directory scaffolding for `frontend/`, `backend/`, `contracts/`, `scaffolds/`, and `evals/`.
- Pydantic V2 inter-agent contracts: `RequirementsContract`, `PlanContract`, `BuildResultContract`, `FileEditContract`, `VersionRecordContract`, `DeploymentRequestContract`.
- Pre-commit hooks for Black, Flake8, MyPy, Prettier, and ESLint.

### Features NOT Included
- Database connections, UI components, LLM calls, audio processing.

### Dependencies
- None (First Phase).

### Deliverables
- Fully initialized Git repository with monorepo directory tree.
- Tested and exported Python package in `contracts/`.
- Passing GitHub Actions base linting workflow (`.github/workflows/lint.yml`).

### Architecture Changes
- Establishment of the clean architecture boundary where contracts sit independent of backend business logic.

### Database Changes
- None.

### API Changes
- None.

### Frontend Changes
- Initial Next.js 15 app shell setup in `frontend/` with Tailwind CSS v3/v4 configured.

### Backend Changes
- Minimal FastAPI application entry point in `backend/app/main.py` exposing health check `/healthz`.

### ML Changes
- None.

### Infrastructure Changes
- Root-level configuration files: `.gitignore`, `.pre-commit-config.yaml`, `pyproject.toml`, `package.json`.

### Configuration Required
- Python 3.12+ virtual environment, Node.js 20+ LTS runtime.

### Environment Variables
- `ENVIRONMENT=development`
- `LOG_LEVEL=DEBUG`

### Third-party Services
- GitHub for source control.

### Tasks
- [x] Task 1.1: Initialize Git repo and enforce branch protection on `main`.
- [x] Task 1.2: Author all Pydantic V2 schemas in `contracts/`.
- [x] Task 1.3: Configure poetry / uv for Python dependency management.
- [x] Task 1.4: Configure pnpm workspace for frontend and scaffolds.
- [x] Task 1.5: Set up pre-commit hook runner.

### Subtasks
- Subtask 1.2.1: Write `RequirementsContract` with validation rules for color codes and navigation items.
- Subtask 1.2.2: Write `PlanContract` with file role validations.
- Subtask 1.2.3: Write `BuildResultContract` with exit code and boolean flags.

### Acceptance Criteria
- Running `pre-commit run --all-files` passes without errors.
- Running `pytest contracts/tests/` passes 100% of schema serialization/deserialization tests.
- FastAPI `/healthz` returns `{"status": "ok"}`.

### Definition of Done
- Code merged to `main` via PR reviewed by at least one team member; CI workflow green.

### Unit Tests
- `test_requirements_contract_valid_json()`
- `test_requirements_contract_invalid_color_hex()`
- `test_plan_contract_file_roles_enum()`
- `test_build_result_contract_defaults()`

### Integration Tests
- `test_fastapi_healthz_endpoint()`

### End-to-End Tests
- None for this phase.

### Manual Testing Checklist
- [ ] Clone fresh repository onto a separate machine.
- [ ] Run `poetry install` and `pnpm install`.
- [ ] Execute `pytest` and verify 0 failures.
- [ ] Run `git commit` with improperly formatted code; assert pre-commit blocks the commit.

### Regression Tests
- None (baseline phase).

### Rollback Strategy
- Revert commit on `main`; reset to empty initial commit.

### Estimated Complexity
- Low (1/5).

### Estimated Time
- 3 days.

### Risks
- Team members using disparate Python or Node version managers causing lockfile discrepancies.
- *Mitigation:* Pin exact versions in `.tool-versions` and `pyproject.toml`.

### Future Improvements
- Automated type generation from Pydantic schemas to TypeScript interfaces via `json-schema-to-typescript`.
