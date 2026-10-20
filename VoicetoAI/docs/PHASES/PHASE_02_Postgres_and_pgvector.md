# Phase 2: PostgreSQL with pgvector Schema & Database Migrations

---

### Navigation
- **Current Phase:** Phase 2 of 20
- **Previous Phase:** [Phase 1: Repository Foundation, Monorepo Setup & Shared Contracts](file:///d:/VoicetoAI/docs/PHASES/PHASE_01_Repo_Setup_and_Contracts.md)
- **Next Phase:** [Phase 3: S3 Object Storage & Audio Validation Pipeline](file:///d:/VoicetoAI/docs/PHASES/PHASE_03_S3_Storage_and_Audio_Validation.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [TDD.md](file:///d:/VoicetoAI/docs/TDD.md), [RAG_ManifestSearch.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/RAG_ManifestSearch.md)

---

### Objective
Deploy PostgreSQL 16 with the `vector` extension and configure Alembic migrations to establish the normalized data model.

### Business Goal
Provide persistent, transactional storage for users, projects, messages, file manifests, versions, and the platform financial ledger.

### Technical Goal
Execute fully reversible database migrations with foreign key constraints, indexes, and pgvector HNSW index structures.

### Features Included
- Docker Compose configuration for PostgreSQL 16 + pgvector.
- SQLAlchemy 2.0 async models for all 16 relational tables.
- Alembic migration pipeline (`alembic upgrade head`).
- Database seed script with standard subscription plans (`free_tier`, `pro_tier`).

### Features NOT Included
- Direct agent integration, S3 storage, WebSocket endpoints.

### Dependencies
- Phase 1 (Repository Foundation & Contracts).

### Deliverables
- `docker-compose.yml` with pgvector service.
- `backend/app/models/` containing all relational models.
- Reversible Alembic migration scripts in `backend/alembic/versions/`.

### Architecture Changes
- Persistence layer established; FastAPI backend connects to PostgreSQL via `asyncpg` connection pool.

### Database Changes
- Complete DDL execution: `users`, `plans`, `subscriptions`, `usage_counters`, `projects`, `messages`, `requirements`, `decisions`, `versions`, `files`, `runs`, `deployment_requests`, `quotes`, `payments`, `ledger_entries`, `payout_periods`, `payouts`.
- HNSW index created on `files.embedding` (cosine distance).

### API Changes
- Internal database session dependency `get_db` available for FastAPI routers.

### Frontend Changes
- None.

### Backend Changes
- Asynchronous database engine setup using SQLAlchemy `create_async_engine`.
- CRUD repository modules for `projects`, `messages`, and `users`.

### ML Changes
- None.

### Infrastructure Changes
- Local containerized Postgres service exposed on port 5432 with volume persistence.

### Configuration Required
- Postgres credentials and connection string configuration.

### Environment Variables
- `DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/voicetoai_db`
- `POSTGRES_DB=voicetoai_db`
- `POSTGRES_USER=postgres`
- `POSTGRES_PASSWORD=postgres`

### Third-party Services
- None (local Docker).

### Tasks
- [x] Task 2.1: Add `pgvector/pgvector:pg16` service to `docker-compose.yml`.
- [x] Task 2.2: Implement SQLAlchemy 2.0 declarative models.
- [x] Task 2.3: Initialize Alembic and create initial migration.
- [x] Task 2.4: Implement vector column definition and HNSW index in migration script.
- [x] Task 2.5: Write seed script for subscription tiers and test users.

### Subtasks
- Subtask 2.2.1: Implement core project and message models.
- Subtask 2.2.2: Implement file manifest model with Vector(1536).
- Subtask 2.2.3: Implement double-entry ledger models.

### Acceptance Criteria
- `alembic upgrade head` runs cleanly on a fresh Postgres container.
- `alembic downgrade base` cleanly drops all tables and types without orphan locks.
- `SELECT * FROM pg_extension WHERE extname = 'vector';` returns 1 row.

### Definition of Done
- Automated integration test runs migration up, inserts a row into all tables, queries vector similarity, and migrates down successfully.

### Unit Tests
- `test_user_model_creation()`
- `test_project_model_relationships()`
- `test_ledger_entry_debit_credit_validation()`

### Integration Tests
- `test_alembic_upgrade_downgrade_cycle()`
- `test_pgvector_insertion_and_cosine_query()`

### End-to-End Tests
- None for this phase.

### Manual Testing Checklist
- [ ] Run `docker-compose up -d postgres`.
- [ ] Run `alembic upgrade head`.
- [ ] Connect with `psql` and inspect `\d files`. Verify vector index exists.
- [ ] Run seed script; verify plans table contains Free and Pro rows.

### Regression Tests
- Re-run Phase 1 contract unit tests; assert zero breakage.

### Rollback Strategy
- Execute `alembic downgrade -1` or destroy docker volume.

### Estimated Complexity
- Medium (2/5).

### Estimated Time
- 3 days.

### Risks
- PostgreSQL vector extension incompatibility on certain Windows native environments.
- *Mitigation:* Enforce Dockerized Postgres container across all developer machines.

### Future Improvements
- Read-replica connection pooling with PgBouncer.
