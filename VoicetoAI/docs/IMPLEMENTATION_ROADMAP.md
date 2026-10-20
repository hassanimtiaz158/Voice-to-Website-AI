# Complete Implementation Roadmap: Voice-to-Website AI
## Master Incremental Engineering Roadmap (Phases 1 to 20)

---

### Document Metadata
- **Document Version:** 2.0.0
- **Status:** APPROVED & LOCKED
- **Standard:** Every phase is strictly independent, produces a working, backward-compatible system, and adheres to the mandatory 33-point implementation schema.

---

```
                                  ROADMAP OVERVIEW
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ FOUNDATIONS (Phases 1–3)                                                    │
 │ P1: Monorepo & Contracts ──► P2: Postgres/pgvector ──► P3: S3 Audio Ingest  │
 ├─────────────────────────────────────────────────────────────────────────────┤
 │ VOICE INGESTION PIPELINE (Phases 4–5)                                       │
 │ P4: Bilingual Whisper ASR ──► P5: VAD & Audio Streaming                     │
 ├─────────────────────────────────────────────────────────────────────────────┤
 │ SANDBOX & AGENTIC BUILD ENGINE (Phases 6–10)                                │
 │ P6: E2B Sandbox Runner ──► P7: LangGraph & Checkpointer ──► P8: Clarifier   │
 │                                                      │                      │
 │ P10: Sequential Coder  ◄─── P9: Stack Planner  ◄─────┘                      │
 ├─────────────────────────────────────────────────────────────────────────────┤
 │ VERIFICATION, HEALING & VERSIONING (Phases 11–13)                           │
 │ P11: Playwright Verifier ──► P12: Fixer Self-Healing ──► P13: GitHub MCP    │
 ├─────────────────────────────────────────────────────────────────────────────┤
 │ SURGICAL RAG & EDITING PIPELINE (Phases 14–15)                              │
 │ P14: Manifest pgvector Locator ──► P15: Surgical Editor & Unified Diffs     │
 ├─────────────────────────────────────────────────────────────────────────────┤
 │ ENTERPRISE PLATFORM & MARKETPLACE (Phases 16–17)                            │
 │ P16: Auth & RBAC Quotas ──► P17: Human Marketplace & Double-Entry Ledger    │
 ├─────────────────────────────────────────────────────────────────────────────┤
 │ PRODUCTION OPERATIONS & FINAL HARDENING (Phases 18–20)                      │
 │ P18: Observability & Evals ──► P19: CI/CD & SSL ──► P20: Hardening & Ship   │
 └─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Repository Foundation, Monorepo Setup & Shared Contracts

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

---

## Phase 2: PostgreSQL with pgvector Schema & Database Migrations

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

---

## Phase 3: S3 Object Storage & Audio Validation Pipeline

### Objective
Implement secure object storage for audio files, visual screenshots, and site zip archives using an S3-compatible API with cryptographic pre-signed URLs.

### Business Goal
Safely store customer voice recordings and audit trail media with low cost and high durability.

### Technical Goal
Deploy MinIO for local development and configure `boto3` / `aioboto3` client with upload validation (MIME type, size, duration, audio energy).

### Features Included
- Local MinIO container in Docker Compose with auto-created buckets: `voicetoai-audio`, `voicetoai-artifacts`.
- Asynchronous S3 storage service in backend.
- Audio file validation: checks file size ($< 15\text{ MB}$), duration ($1.0\text{s} - 120.0\text{s}$), and RMS audio energy ($> -45\text{ dBFS}$).
- Pre-signed URL generation for secure, temporary media access.

### Features NOT Included
- Whisper speech-to-text processing, streaming WebSockets.

### Dependencies
- Phase 1 (Repository), Phase 2 (Database for message linkage).

### Deliverables
- MinIO service in `docker-compose.yml`.
- `backend/app/services/storage.py` (S3 client).
- `backend/app/services/audio_validator.py`.
- Unit and integration tests for storage operations.

### Architecture Changes
- Backend gains object storage capability; audio binary data is detached from PostgreSQL and stored in S3.

### Database Changes
- None (populates existing `messages.audio_s3_key`).

### API Changes
- `POST /api/v1/storage/upload-audio`: Uploads and validates raw audio blob.
- `GET /api/v1/storage/signed-url`: Generates 15-minute expiring read URL.

### Frontend Changes
- None.

### Backend Changes
- Integration of `aioboto3` for non-blocking file streaming to S3.
- Audio validation pipeline using `soundfile` and `pydub` / `librosa`.

### ML Changes
- Audio preprocessing filter to detect silent or corrupt audio.

### Infrastructure Changes
- MinIO service running on ports 9000 (API) and 9001 (Console).

### Configuration Required
- S3 access keys, bucket policies, and endpoint URLs.

### Environment Variables
- `S3_ENDPOINT_URL=http://localhost:9000`
- `S3_ACCESS_KEY=minioadmin`
- `S3_SECRET_KEY=minioadmin`
- `S3_AUDIO_BUCKET=voicetoai-audio`
- `S3_ARTIFACTS_BUCKET=voicetoai-artifacts`

### Third-party Services
- AWS S3 or Cloudflare R2 in production; MinIO in development.

### Tasks
- [x] Task 3.1: Add MinIO service to Docker Compose.
- [x] Task 3.2: Implement asynchronous S3 client service.
- [x] Task 3.3: Implement audio validation and loudness checker.
- [x] Task 3.4: Expose upload and pre-signed URL endpoints in FastAPI.

### Subtasks
- Subtask 3.3.1: Write RMS decibel calculation function.
- Subtask 3.3.2: Implement file signature / magic-byte verification for WebM and WAV.

### Acceptance Criteria
- Uploading a 5-second valid audio clip stores the file in MinIO and returns an S3 key.
- Uploading a completely silent audio file is rejected with HTTP 422 Unprocessable Entity.
- Pre-signed URL allows downloading the audio clip in an external browser.

### Definition of Done
- Storage service verified with integration tests against MinIO; documentation updated.

### Unit Tests
- `test_audio_validator_valid_audio()`
- `test_audio_validator_silent_audio_rejected()`
- `test_audio_validator_oversized_file_rejected()`

### Integration Tests
- `test_s3_upload_and_download_roundtrip()`
- `test_presigned_url_expiration()`

### End-to-End Tests
- None.

### Manual Testing Checklist
- [ ] Start MinIO, open `http://localhost:9001` in browser.
- [ ] Post a sample WAV file via Swagger UI at `/docs`.
- [ ] Verify object appears in `voicetoai-audio` bucket in MinIO console.

### Regression Tests
- Re-run Phase 1 and 2 test suites.

### Rollback Strategy
- Remove MinIO container and revert `storage.py`.

### Estimated Complexity
- Low (2/5).

### Estimated Time
- 3 days.

### Risks
- Network timeouts during large file uploads.
- *Mitigation:* Strict 15 MB file size limit enforced before reading buffer into memory.

### Future Improvements
- Client-direct S3 pre-signed POST uploads to bypass backend gateway for multi-megabyte files.

---

## Phase 4: Bilingual Whisper ASR & Transcript Confirmation Engine

### Objective
Deploy the speech-to-text pipeline supporting Urdu, English, and bilingual code-switching ("Urdish") using Whisper Large-v3-Turbo, with mandatory UI transcript confirmation.

### Business Goal
Allow Pakistani and international shop owners to describe their requirements effortlessly without typing friction, while preventing AI hallucinations through explicit transcript confirmation.

### Technical Goal
Implement high-throughput ASR inference with domain-specific priming prompts, achieving $<1.5\text{s}$ latency and $<14\%$ WER on conversational retail speech.

### Features Included
- Whisper ASR engine (supporting local Faster-Whisper and OpenAI Whisper API fallback).
- Domain-specific priming prompt injection for Pakistani retail terminology.
- Audio format normalization (converting WebM/Opus to 16kHz mono WAV).
- Transcript confirmation modal in the Next.js frontend.

### Features NOT Included
- LangGraph orchestration, code planning, automated editing.

### Dependencies
- Phase 1 (Contracts), Phase 2 (Database), Phase 3 (Audio Storage).

### Deliverables
- `backend/app/services/asr.py`.
- `frontend/components/voice/TranscriptModal.tsx`.
- Benchmark evaluation script for 30 test audio clips.

### Architecture Changes
- ASR processing service integrated into backend; FastAPI exposes audio-to-text pipeline.

### Database Changes
- Updates `messages` table with `audio_s3_key` and transcribed `content`.

### API Changes
- `POST /api/v1/voice/transcribe`: Accepts audio, uploads to S3, runs Whisper, returns transcript.

### Frontend Changes
- Audio recording button component with live recording timer.
- Transcript confirmation modal with editable text input and "Confirm / Re-record" buttons.

### Backend Changes
- Implementation of Whisper inference wrapper with retry and timeout logic.

### ML Changes
- Whisper prompt tuning with Urdu/English retail lexicon.

### Infrastructure Changes
- Local CUDA support or OpenAI API integration.

### Configuration Required
- Whisper model selection (`large-v3-turbo` vs API).

### Environment Variables
- `WHISPER_BACKEND=openai` (or `local`)
- `OPENAI_API_KEY=sk-...`

### Third-party Services
- OpenAI Whisper API (or local GPU instance).

### Tasks
- [x] Task 4.1: Implement audio normalization utility (16kHz mono WAV).
- [x] Task 4.2: Build Whisper ASR service with domain priming prompt.
- [x] Task 4.3: Implement FastAPI transcription endpoint.
- [x] Task 4.4: Build frontend audio recorder and transcript confirmation modal.
- [x] Task 4.5: Run ASR benchmark on 30 test clips.

### Subtasks
- Subtask 4.2.1: Construct Pakistani retail terminology prompt string.
- Subtask 4.4.1: Implement browser `MediaRecorder` hook in React.

### Acceptance Criteria
- Spoken voice note is transcribed into editable text in $<2.0\text{ seconds}$.
- Transcript confirmation modal displays text accurately in UI.
- User can edit a misspelled word and click "Confirm".
- ASR Word Error Rate on 30 test clips is $\le 14\%$.

### Definition of Done
- Complete voice-to-transcript flow operates seamlessly in the web browser; PR reviewed and merged.

### Unit Tests
- `test_audio_normalization_resample()`
- `test_whisper_prompt_formatting()`

### Integration Tests
- `test_transcribe_endpoint_with_sample_wav()`
- `test_asr_error_handling_corrupt_payload()`

### End-to-End Tests
- Playwright test: Record simulated audio $\to$ inspect modal $\to$ click confirm $\to$ assert backend message saved.

### Manual Testing Checklist
- [ ] Speak into laptop microphone in Urdu: "Meri jooton ki dukaan hai".
- [ ] Verify transcribed text appears in modal.
- [ ] Edit text to add "Lahore mein" and submit.
- [ ] Verify final text in database includes manual edit.

### Regression Tests
- Re-run Phases 1–3 test suites.

### Rollback Strategy
- Fall back to purely typed text input by disabling the microphone trigger component.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 4 days.

### Risks
- High phonetic variation in regional Urdu accents causing misspellings.
- *Mitigation:* Mandatory transcript confirmation modal ensures user validates intent before LLM generation.

### Future Improvements
- Fine-tune Whisper LoRA on Pakistani e-commerce voice notes.

---

## Phase 5: Voice Activity Detection (VAD) & Real-time Audio Ingestion Stream

### Objective
Integrate client-side and server-side Voice Activity Detection (VAD) to automatically detect speech boundaries, silence, and background noise.

### Business Goal
Provide a frictionless, hands-free conversational experience where recording stops automatically when the merchant finishes speaking.

### Technical Goal
Deploy Silero VAD / WebRTC VAD with a 1,800 ms silence trigger and real-time audio chunk streaming over WebSockets.

### Features Included
- Silero VAD integration in client/backend.
- Silence threshold detection (1,800 ms of trailing silence triggers automatic stop).
- WebSocket streaming audio endpoint `/ws/v1/voice/stream`.
- Visual waveform / audio level indicator in frontend UI.

### Features NOT Included
- Direct LLM streaming responses, code generation.

### Dependencies
- Phase 4 (ASR & Audio Processing).

### Deliverables
- `frontend/hooks/useVAD.ts`.
- `backend/app/services/vad.py`.
- WebSocket streaming handler in `backend/app/api/ws_voice.py`.

### Architecture Changes
- Introduction of WebSocket communication layer for real-time bidirectional audio streaming.

### Database Changes
- None.

### API Changes
- `WebSocket /ws/v1/voice/stream`: Bidirectional audio streaming and real-time transcription status.

### Frontend Changes
- Animated pulsating microphone button responding to voice volume.
- Auto-submit trigger when VAD detects end of speech.

### Backend Changes
- Chunked audio buffer accumulator with VAD evaluation per 30ms audio frame.

### ML Changes
- Silero VAD ONNX runtime integration.

### Infrastructure Changes
- None.

### Configuration Required
- VAD silence sensitivity threshold (default: 0.5 probability).

### Environment Variables
- `VAD_SILENCE_TIMEOUT_MS=1800`

### Third-party Services
- None.

### Tasks
- [x] Task 5.1: Package Silero VAD ONNX model for Python runtime.
- [x] Task 5.2: Implement WebSocket streaming chunk accumulator.
- [x] Task 5.3: Implement frontend audio worklet with volume visualization.
- [x] Task 5.4: Implement automatic stop-on-silence logic.

### Subtasks
- Subtask 5.2.1: Write 30ms PCM frame slicing algorithm.
- Subtask 5.3.1: Build Canvas-based audio waveform component.

### Acceptance Criteria
- User speaks; waveform oscillates in real time.
- User stops speaking; recording automatically terminates after 1.8 seconds.
- WebSocket emits transcription event within 800 ms of speech cessation.

### Definition of Done
- Hands-free voice recording operates reliably across Chrome, Firefox, and Safari without manual button tapping.

### Unit Tests
- `test_vad_frame_slicing()`
- `test_vad_silence_detection()`

### Integration Tests
- `test_websocket_audio_stream_complete_flow()`

### End-to-End Tests
- Automated browser test verifying recording stop event triggers upon feeding a 3-second audio file followed by 2 seconds of silence.

### Manual Testing Checklist
- [ ] Speak continuously for 10 seconds; verify no premature cutoff.
- [ ] Pause speaking for 2 seconds; verify recording ends automatically and transcript modal opens.

### Regression Tests
- Re-run Phase 4 transcription tests.

### Rollback Strategy
- Disable VAD auto-stop flag; revert to manual click-to-start / click-to-stop recording.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 3 days.

### Risks
- Background fan noise or traffic in retail shops preventing silence detection.
- *Mitigation:* Audio energy gate combined with probability thresholding prevents ambient noise from keeping VAD open indefinitely.

### Future Improvements
- Background noise cancellation via WebAssembly Krisp or RNNoise in the browser.

---

## Phase 6: Pinned Scaffolds & E2B / Docker Sandbox Runner Engine

### Objective
Build the hardened sandbox execution engine using E2B microVMs (and local Docker fallback) with pre-cached dependencies for the pinned `vite-react-tailwind` stack.

### Business Goal
Ensure untrusted code execution happens in absolute isolation with zero danger to platform servers, while achieving $<15\text{s}$ build speeds.

### Technical Goal
Implement the 5-stage verification pipeline (`npm ci`, `tsc`, `lint`, `build`, `preview`) with resource quotas (2 vCPU, 2GB RAM, 300s timeout) and strict egress filtering.

### Features Included
- Base template scaffold in `scaffolds/vite-react-tailwind/`.
- Pre-cached `node_modules` image configuration.
- `backend/app/sandbox/runner.py` with E2B and local Docker implementations.
- 5-stage build execution pipeline returning structured `BuildResultContract`.

### Features NOT Included
- LLM code generation, automated fixing, GitHub commits.

### Dependencies
- Phase 1 (Contracts).

### Deliverables
- Hardened base image Dockerfile for sandbox runner.
- Pinned `vite-react-tailwind` scaffold with TypeScript strict mode enabled.
- Fully tested sandbox runner module in `backend/app/sandbox/`.

### Architecture Changes
- Integration of external compute isolation provider (E2B Cloud API / Docker daemon).

### Database Changes
- None.

### API Changes
- Internal execution interface: `await sandbox_runner.execute_build(files: Dict[str, str]) -> BuildResultContract`.

### Frontend Changes
- None.

### Backend Changes
- Sandbox lifecycle management (instantiate microVM $\to$ write files $\to$ run commands $\to$ teardown).

### ML Changes
- None.

### Infrastructure Changes
- E2B API integration or local Docker socket binding.

### Configuration Required
- Hardware resource limits: 2 vCPU, 2048 MB RAM, 300s execution deadline.

### Environment Variables
- `SANDBOX_PROVIDER=e2b` (or `docker`)
- `E2B_API_KEY=e2b_...`

### Third-party Services
- E2B Cloud MicroVM Sandbox.

### Tasks
- [x] Task 6.1: Author clean `vite-react-tailwind` scaffold with zero build errors.
- [x] Task 6.2: Build base sandbox template with pre-installed npm cache.
- [x] Task 6.3: Implement `E2BSandboxRunner` with timeout and memory monitoring.
- [x] Task 6.4: Implement fallback `DockerSandboxRunner` for local offline testing.
- [x] Task 6.5: Implement structured stderr/stdout parser.

### Subtasks
- Subtask 6.3.1: Configure outbound egress rules blocking all IPs except npm registry.
- Subtask 6.5.1: Write TypeScript compiler regex error parser (`TS\d{4}`).

### Acceptance Criteria
- Injecting clean scaffold files into sandbox completes full build pipeline in $<15\text{ seconds}$ with exit code 0.
- Injecting a file with a deliberate syntax error exits with code 1 and populates `BuildResultContract.raw_error_log`.
- Sandbox cannot access host network or host filesystem.

### Definition of Done
- Sandbox runner passes both clean and deliberate error test suites; CI runs Docker runner cleanly.

### Unit Tests
- `test_error_log_regex_parser()`
- `test_build_result_contract_mapping()`

### Integration Tests
- `test_sandbox_clean_scaffold_build()`
- `test_sandbox_typescript_error_capture()`
- `test_sandbox_timeout_enforcement()`

### End-to-End Tests
- None.

### Manual Testing Checklist
- [ ] Trigger test build of scaffold in E2B.
- [ ] Inspect E2B dashboard; verify session terminates cleanly after run.
- [ ] Disconnect internet on host; test local Docker runner fallback.

### Regression Tests
- Re-run Phase 1 contracts tests.

### Rollback Strategy
- Toggle `SANDBOX_PROVIDER=docker` if E2B experiences external outage.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Sandbox running out of memory (OOM) during Vite asset bundling on 2GB limit.
- *Mitigation:* Pin `NODE_OPTIONS=--max-old-space-size=1536` to prevent swapping and runaway heap growth.

### Future Improvements
- MicroVM warm pool recycling to reduce initial spin-up latency below 1 second.

---

## Phase 7: LangGraph State Machine Skeleton & Postgres Checkpointer

### Objective
Implement the deterministic LangGraph state machine with persistent PostgreSQL checkpointing (`PostgresSaver`) and human-in-the-loop `interrupt()` support.

### Business Goal
Guarantee that complex, multi-turn AI interactions never lose state, survive server restarts, and can pause for user decisions indefinitely without data loss.

### Technical Goal
Construct the cyclic `StateGraph` using `ProjectGraphState`, wire all conditional edges, and attach the async Postgres checkpointer.

### Features Included
- LangGraph state machine definition in `backend/app/orchestrator/graph.py`.
- Persistence using `langgraph.checkpoint.postgres.aio.AsyncPostgresSaver`.
- State schema validation with typed Pydantic handoffs.
- Human-in-the-loop interruption mechanism (`interrupt()`).

### Features NOT Included
- Complex LLM agent prompts (mock agent nodes used to validate state transitions).

### Dependencies
- Phase 1 (Contracts), Phase 2 (Postgres Database), Phase 6 (Sandbox).

### Deliverables
- `backend/app/orchestrator/state.py`.
- `backend/app/orchestrator/graph.py`.
- Unit tests verifying 100% of state graph branch paths.

### Architecture Changes
- Introduction of the centralized LangGraph execution engine governing all workflow routing.

### Database Changes
- Automatic creation of LangGraph checkpoint tables (`checkpoints`, `checkpoint_blobs`, `checkpoint_writes`) via `AsyncPostgresSaver`.

### API Changes
- `POST /api/v1/projects/{id}/graph/invoke`: Dispatches or resumes graph thread.
- `GET /api/v1/projects/{id}/graph/state`: Retrieves current thread state.

### Frontend Changes
- None (API-level state testing).

### Backend Changes
- Orchestration service wiring FastAPI background tasks to LangGraph runner.

### ML Changes
- None.

### Infrastructure Changes
- None.

### Configuration Required
- LangGraph thread ID formatting (`project_id:version_n`).

### Environment Variables
- `LANGGRAPH_CHECKPOINT_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/voicetoai_db`

### Third-party Services
- None.

### Tasks
- [x] Task 7.1: Define `ProjectGraphState` TypedDict.
- [x] Task 7.2: Wire nodes: `router`, `clarifier`, `planner`, `coder`, `sandbox`, `fixer`, `verifier`, `committer`.
- [x] Task 7.3: Implement conditional branching edges.
- [x] Task 7.4: Initialize `AsyncPostgresSaver` checkpointer.
- [x] Task 7.5: Implement resumption test after simulated server crash.

### Subtasks
- Subtask 7.2.1: Implement mock node functions returning deterministic state updates.
- Subtask 7.3.1: Write conditional routing functions (`should_continue_clarification`, `should_fix_or_verify`).

### Acceptance Criteria
- Graph execution halts at `clarifier` node when `interrupt()` is called.
- Backend can resume execution by submitting answers to the same `thread_id`.
- Complete execution history is retrievable from Postgres checkpoints.

### Definition of Done
- State graph passes cyclic execution and recovery tests with 100% branch coverage; PR merged.

### Unit Tests
- `test_state_initialization_defaults()`
- `test_conditional_routing_router_decisions()`
- `test_conditional_routing_fixer_retry_counter()`

### Integration Tests
- `test_postgres_saver_persistence()`
- `test_graph_interrupt_and_resumption()`

### End-to-End Tests
- Mock end-to-end execution through all nodes without LLM API calls.

### Manual Testing Checklist
- [ ] Invoke graph via curl; verify checkpoint row written in `checkpoints` table.
- [ ] Kill FastAPI server while graph is paused on interrupt.
- [ ] Restart FastAPI; send resume payload; verify graph completes successfully.

### Regression Tests
- Re-run Phase 2 and 6 tests.

### Rollback Strategy
- Revert graph definition to linear mock pipeline.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Database deadlocks during concurrent checkpoint writes on high-volume threads.
- *Mitigation:* Ensure strict 1-to-1 thread mapping per project with row-level locking.

### Future Improvements
- Graph execution visualization streaming via LangGraph Studio integration.

---

## Phase 8: Tri-Modal Router & Diagnostic Clarifier Agent with Interrupts

### Objective
Deploy production LLM nodes for the tri-modal Router and diagnostic Clarifier using Claude 3.5 Haiku, capturing user decisions and structured requirements summaries.

### Business Goal
Transform vague, non-technical shop owner inputs into precise, unambiguous technical specifications within 3 turns, eliminating developer back-and-forth.

### Technical Goal
Implement Claude 3.5 Haiku structured prompting with few-shot examples, JSON schema validation, and database audit logging to `decisions` and `requirements` tables.

### Features Included
- Production `router_node`: classifies into `QUESTION`, `SMALL_EDIT`, or `NEW_OR_MAJOR`.
- Production `clarifier_node`: generates 3 to 5 multiple-choice questions per turn (with "You Decide" option).
- Turn counter enforcement (max 3 turns).
- Requirements summary generator and confirmation gate.
- Audit persistence in `decisions` and `requirements` tables.

### Features NOT Included
- Code planning, code generation, sandbox builds.

### Dependencies
- Phase 7 (LangGraph Engine), Phase 2 (Database).

### Deliverables
- `backend/app/agents/router.py`.
- `backend/app/agents/clarifier.py`.
- `frontend/components/chat/ClarifierQuestionCard.tsx`.
- 20 scripted shop owner persona test cases in `evals/personas/`.

### Architecture Changes
- Real LLM calls integrated into LangGraph pipeline using Anthropic Python SDK.

### Database Changes
- Writes to `decisions` table and `requirements` table.

### API Changes
- `POST /api/v1/projects/{id}/clarify/answer`: Submits user choices and resumes LangGraph thread.

### Frontend Changes
- Dynamic option card UI rendering multi-choice question bubbles with one-click selection.
- Sticky "Requirements Summary" card with "Approve & Build" CTA.

### Backend Changes
- Anthropic API client wrapper with prompt caching headers (`cache_control: {"type": "ephemeral"}`).

### ML Changes
- Prompt engineering for Clarifier and Router; few-shot bilingual Urdu/English examples.

### Infrastructure Changes
- Anthropic API key provisioning.

### Configuration Required
- Model assignment: `claude-3-5-haiku-20241022`, max tokens 2500, temperature 0.2.

### Environment Variables
- `ANTHROPIC_API_KEY=sk-ant-...`

### Third-party Services
- Anthropic Claude API.

### Tasks
- [x] Task 8.1: Implement Router agent with strict JSON output schema.
- [x] Task 8.2: Implement Clarifier agent with 3-turn state tracker.
- [x] Task 8.3: Implement "You Decide" fallback resolution logic.
- [x] Task 8.4: Build frontend Clarifier question options UI.
- [x] Task 8.5: Run Persona evaluation benchmark (20 synthetic shop owners).

### Subtasks
- Subtask 8.2.1: Format system prompt enforcing 3 to 5 options per question.
- Subtask 8.3.1: Write decision recorder saving choice and rationale to PostgreSQL.

### Acceptance Criteria
- Router achieves $\ge 96\%$ classification accuracy across 50 benchmark prompts.
- Clarifier completes requirements in $\le 3$ conversational turns for 100% of the 20 test personas.
- Every user decision is queryable in the `decisions` table.
- Requirements summary conforms 100% to `RequirementsContract` Pydantic schema.

### Definition of Done
- Interactive clarification flow fully functional in web UI; eval benchmark passing; PR merged.

### Unit Tests
- `test_router_prompt_classification()`
- `test_clarifier_option_generation()`
- `test_clarifier_turn_limit_guard()`

### Integration Tests
- `test_clarification_to_requirements_db_persistence()`
- `test_clarifier_resumption_via_api()`

### End-to-End Tests
- Complete browser test: enter prompt $\to$ answer 2 turns of questions $\to$ review summary $\to$ approve.

### Manual Testing Checklist
- [ ] Enter: "Mujhe Lahore mein bakery ke liye website chahiye".
- [ ] Verify Clarifier asks 3-5 questions with options (e.g. Products, Delivery, Theme).
- [ ] Select "You Decide" for color theme; verify default is recorded in decisions table.
- [ ] Verify final summary displays bakery details clearly.

### Regression Tests
- Re-run Phase 4 and Phase 7 tests.

### Rollback Strategy
- Fall back to static form-based requirements collector if LLM API fails.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 4 days.

### Risks
- Users providing freeform answers that do not match the multiple-choice options.
- *Mitigation:* Clarifier prompt instructs the model to synthesize freeform text and normalize it into structured fields.

### Future Improvements
- Voice playback of Clarifier questions using Edge-TTS Urdu voice.

---

## Phase 9: Stack-Aware Architectural Planner Agent

### Objective
Deploy the Planner Agent using Claude 3.5 Sonnet to convert verified `RequirementsContract` specifications into a modular, dependency-ordered `PlanContract` for `vite-react-tailwind`.

### Business Goal
Prevent monolithic, spaghetti code generation by enforcing clean software engineering architecture and central data separation.

### Technical Goal
Synthesize architectural file plans specifying paths, roles, exact single-responsibility descriptions, imports, and exports, while enforcing the `data/site.json` invariant.

### Features Included
- Production `planner_node` using Claude 3.5 Sonnet.
- Conventional data separation enforcement (`data/site.json` holds 100% of copy).
- File dependency topological sorter (ensuring data and UI primitives are created before composite views).
- Validation against `PlanContract` schema.

### Features NOT Included
- Full code generation, sandbox execution.

### Dependencies
- Phase 1 (Contracts), Phase 8 (Clarifier & Requirements).

### Deliverables
- `backend/app/agents/planner.py`.
- `backend/app/orchestrator/topological_sorter.py`.
- Unit and integration tests for plan generation.

### Architecture Changes
- LangGraph transitions from Requirements confirmation directly to the Planner node.

### Database Changes
- None (Plan is maintained in LangGraph state).

### API Changes
- None (internal graph node).

### Frontend Changes
- UI displays real-time "Architecting site structure..." progress bar in chat view.

### Backend Changes
- Planner service with prompt caching to reduce token costs on repeated planning runs.

### ML Changes
- Planner system prompt with strict Vite + React 19 + Tailwind architecture rules.

### Infrastructure Changes
- None.

### Configuration Required
- Model assignment: `claude-3-5-sonnet-20241022`, max tokens 4096, temperature 0.2.

### Environment Variables
- Inherited from Phase 8 (`ANTHROPIC_API_KEY`).

### Third-party Services
- Anthropic Claude API.

### Tasks
- [x] Task 9.1: Author Planner system prompt enforcing data separation.
- [x] Task 9.2: Implement Pydantic output parsing for `PlanContract`.
- [x] Task 9.3: Build topological dependency sorter for generated files.
- [x] Task 9.4: Implement validation test suite against 15 diverse retail specs.

### Subtasks
- Subtask 9.1.1: Include standard Vite component tree examples in prompt context.
- Subtask 9.3.1: Verify no circular dependencies exist in generated plan.

### Acceptance Criteria
- Every generated plan includes `data/site.json`, `src/App.tsx`, and modular components in `src/components/`.
- Zero circular dependencies in the file dependency graph.
- 100% of generated plans parse into `PlanContract` without schema errors.

### Definition of Done
- Planner generates valid file trees across all 15 benchmark test requirements; PR merged.

### Unit Tests
- `test_planner_schema_validation()`
- `test_topological_sorter_order()`
- `test_enforcement_of_site_json_in_plan()`

### Integration Tests
- `test_clarifier_to_planner_handoff()`

### End-to-End Tests
- None for this phase.

### Manual Testing Checklist
- [ ] Pass Bakery RequirementsContract into Planner.
- [ ] Inspect emitted file plan; verify `data/site.json`, `Navbar.tsx`, `Hero.tsx`, `MenuGrid.tsx` exist.
- [ ] Verify each file has clear import/export lists.

### Regression Tests
- Re-run Phase 1 and 8 tests.

### Rollback Strategy
- Fall back to static template file plan if dynamic planner produces schema violations.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 3 days.

### Risks
- Planner hallucinating non-existent npm libraries not present in scaffold.
- *Mitigation:* Planner system prompt explicitly pins allowed packages (`lucide-react`, `clsx`, `tailwind-merge`).

### Future Improvements
- Support for multi-page routing configurations (`react-router-dom`).

---

## Phase 10: Sequential Coder Agent & Greenfield Code Generation

### Objective
Deploy the Coder Agent using Claude 3.5 Sonnet to generate complete, production-ready TypeScript and Tailwind files sequentially (one file at a time) based on the Planner's blueprint.

### Business Goal
Deliver clean, maintainable, bespoke website source code that small business owners actually own—not minified black-box templates.

### Technical Goal
Implement file-by-file sequential generation, managing context windows efficiently and streaming generation progress to the user interface.

### Features Included
- Production `coder_node` using Claude 3.5 Sonnet.
- Sequential file generation loop with progress tracking.
- Markdown code fence stripping and syntax validation.
- Real-time WebSocket code generation progress streaming to frontend.

### Features NOT Included
- Sandbox compilation, automatic bug fixing (handled in next phases).

### Dependencies
- Phase 6 (Scaffolds), Phase 9 (Planner).

### Deliverables
- `backend/app/agents/coder.py`.
- `frontend/components/chat/FileGenerationProgress.tsx`.
- Test suite validating syntactic correctness of generated files.

### Architecture Changes
- LangGraph executes the sequential Coder node loop, populating `state["generated_files"]`.

### Database Changes
- None (Code kept in memory / state until sandbox verification).

### API Changes
- WebSocket event: `file_generation_started`, `file_generation_completed`.

### Frontend Changes
- Animated file tree view showing checkmarks as files are generated in real time.

### Backend Changes
- Async generator streaming file creation events over WebSockets.

### ML Changes
- Coder system prompt enforcing strict TypeScript and Tailwind conventions.

### Infrastructure Changes
- None.

### Configuration Required
- Model: `claude-3-5-sonnet-20241022`, max tokens 4096 per file, temperature 0.2.

### Environment Variables
- `ANTHROPIC_API_KEY`.

### Third-party Services
- Anthropic Claude API.

### Tasks
- [x] Task 10.1: Author Coder system prompt with strict typing constraints.
- [x] Task 10.2: Implement single-file generation loop with context pruning.
- [x] Task 10.3: Wire WebSocket progress emission to frontend.
- [x] Task 10.4: Implement AST syntax checker for generated TypeScript.

### Subtasks
- Subtask 10.2.1: Provide `data/site.json` as persistent context to all component generation calls.
- Subtask 10.4.1: Use `esprima` or TypeScript compiler API to catch raw syntax errors before sandbox.

### Acceptance Criteria
- Coder generates all files listed in `PlanContract` without truncation.
- All copy rendered in components is sourced from `data/site.json`.
- Zero syntax errors in generated `.tsx` and `.json` files.

### Definition of Done
- Complete file generation loop executes reliably across 15 benchmark plans; PR merged.

### Unit Tests
- `test_coder_code_fence_extraction()`
- `test_coder_site_json_import_validation()`
- `test_coder_lucide_icon_usage()`

### Integration Tests
- `test_planner_to_coder_execution_pipeline()`

### End-to-End Tests
- None.

### Manual Testing Checklist
- [ ] Run generation for a test jewelry shop plan.
- [ ] Inspect generated files on disk; verify zero placeholders like `// TODO: add code`.
- [ ] Verify UI shows live checkmarks as each component completes.

### Regression Tests
- Re-run Phase 6, 8, and 9 tests.

### Rollback Strategy
- Revert Coder prompt changes to last pinned prompt version in Git.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Large files exceeding completion token limits causing truncated code.
- *Mitigation:* Planner enforces modular file size limits; Coder generates files one at a time.

### Future Improvements
- Parallel file generation for independent leaf components.

---

## Phase 11: Playwright Headless Visual & Functional Verifier Node

### Objective
Deploy the automated Verifier Node running headless Playwright tests inside the sandbox to audit DOM structure, console error logs, layout overflow, and visual snapshots.

### Business Goal
Guarantee that a customer never sees a broken preview, blank screen, or misaligned layout.

### Technical Goal
Implement headless Chromium execution within the sandbox, capturing full-page PNG screenshots, detecting horizontal overflow, and evaluating console errors.

### Features Included
- `verifier_node` in LangGraph.
- Playwright automated smoke test suite (`tests/smoke.spec.ts`).
- Horizontal layout overflow detection script.
- Console error log interceptor.
- Full-page screenshot capture uploaded to S3.

### Features NOT Included
- Automated code fixing (Fixer node handles repairs in Phase 12).

### Dependencies
- Phase 3 (S3 Storage), Phase 6 (Sandbox), Phase 10 (Coder).

### Deliverables
- `backend/app/agents/verifier.py`.
- Pinned Playwright smoke test script in sandbox base image.
- S3 screenshot uploader utility.

### Architecture Changes
- Sandbox execution pipeline extended to include Stage 5 (Playwright Visual Verification).

### Database Changes
- None.

### API Changes
- None (internal graph node).

### Frontend Changes
- Live preview iframe displays full-page screenshot as instant placeholder while iframe hydrates.

### Backend Changes
- Verifier service parsing Playwright test results and screenshot paths.

### ML Changes
- Optional: Claude 3.5 Sonnet vision check on generated screenshot (stretch goal).

### Infrastructure Changes
- Playwright browser binaries pre-baked into sandbox base image.

### Configuration Required
- Viewport size: 1280x800 (Desktop) and 375x667 (Mobile).

### Environment Variables
- None.

### Third-party Services
- None (local to sandbox).

### Tasks
- [x] Task 11.1: Author `smoke.spec.ts` testing title, console errors, and horizontal scroll.
- [x] Task 11.2: Pre-bake Chromium binaries into sandbox Docker/E2B image.
- [x] Task 11.3: Wire Verifier node into LangGraph state machine.
- [x] Task 11.4: Implement screenshot upload to S3 `voicetoai-artifacts` bucket.

### Subtasks
- Subtask 11.1.1: Write DOM evaluation script checking `document.documentElement.scrollWidth`.
- Subtask 11.3.1: Map Playwright failure codes to `BuildResultContract`.

### Acceptance Criteria
- Sites with console errors or horizontal overflow are flagged as failing verification.
- Sites that pass render cleanly produce a high-resolution full-page PNG screenshot in S3 in $<4\text{ seconds}$.

### Definition of Done
- Verifier node runs cleanly inside sandbox; verified test suite passes; PR merged.

### Unit Tests
- `test_verifier_result_parsing()`
- `test_overflow_detection_logic()`

### Integration Tests
- `test_sandbox_playwright_execution()`
- `test_screenshot_s3_upload()`

### End-to-End Tests
- None.

### Manual Testing Checklist
- [ ] Intentionally inject `console.error("Critical failure")` into test component.
- [ ] Assert Verifier flags failure and blocks promotion.
- [ ] Inject 2000px wide div; assert Verifier detects horizontal layout overflow.

### Regression Tests
- Re-run Phase 6 and 10 tests.

### Rollback Strategy
- Soften verification assertions to warn-only if third-party CDN fonts trigger spurious console warnings.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 3 days.

### Risks
- Headless browser crashing due to sandbox memory constraints.
- *Mitigation:* Launch Chromium with `--disable-dev-shm-usage` and `--no-sandbox` flags.

### Future Improvements
- Automated visual regression diffing against previous version screenshots.

---

## Phase 12: Targeted Fixer Agent & Self-Healing Build Loop

### Objective
Deploy the self-healing Fixer Agent using Claude 3.5 Sonnet to autonomously patch compilation, linting, and Playwright verification errors within a strict 3-retry budget.

### Business Goal
Achieve an autonomous build success rate $\ge 85\%$ without requiring human engineering intervention when minor syntax or import errors occur.

### Technical Goal
Implement targeted self-healing: deliver strictly the failing files and terminal error output to Claude 3.5 Sonnet, apply surgical patches, and quarantine failed runs on draft branches.

### Features Included
- Production `fixer_node` using Claude 3.5 Sonnet.
- Targeted context injection (only error stderr and failing files delivered).
- 3-retry ceiling enforcement with LangGraph conditional loop.
- Quarantine failure path: preserves draft branch on exhaustion and emits friendly user explanation.

### Features NOT Included
- GitHub main branch commits (handled in Phase 13).

### Dependencies
- Phase 6 (Sandbox), Phase 7 (LangGraph), Phase 10 (Coder), Phase 11 (Verifier).

### Deliverables
- `backend/app/agents/fixer.py`.
- Automated test harness simulating 10 common compiler errors and measuring auto-fix recovery.

### Architecture Changes
- LangGraph closes the cyclic self-healing loop: `Sandbox -> Fixer -> Sandbox`.

### Database Changes
- Records retry attempts and repair tokens in `runs` table.

### API Changes
- Real-time build log streaming event: `build_attempt_failed`, `fixer_patching_commenced`.

### Frontend Changes
- Build log console view in UI displaying real-time compiler outputs and fix attempt counter (e.g., "Auto-healing attempt 1/3...").

### Backend Changes
- Fixer agent execution and file patching logic.

### ML Changes
- Fixer system prompt optimized for diagnosing TypeScript and React import errors.

### Infrastructure Changes
- None.

### Configuration Required
- Max retry limit: 3 attempts.

### Environment Variables
- `ANTHROPIC_API_KEY`.

### Third-party Services
- Anthropic Claude API.

### Tasks
- [x] Task 12.1: Author Fixer system prompt with strict surgical patching rules.
- [x] Task 12.2: Implement error context extractor filtering compiler traces.
- [x] Task 12.3: Wire retry decrement and quarantine routing in LangGraph.
- [x] Task 12.4: Validate Fixer across 10 synthetic error cases (missing imports, type mismatches).

### Subtasks
- Subtask 12.2.1: Parse TypeScript error codes (`TS2304`, `TS2322`, `TS2339`).
- Subtask 12.3.1: Implement quarantine state preserving files on `draft/failed-vN`.

### Acceptance Criteria
- Fixer resolves common errors (missing imports, unclosed tags, misspelled props) in $\le 2$ attempts.
- If errors persist after 3 attempts, graph terminates gracefully without crashing and leaves `main` untouched.
- 100% of fix attempts log token usage and costs to `runs` table.

### Definition of Done
- Fixer recovers at least 8 out of 10 synthetic broken builds; PR merged.

### Unit Tests
- `test_fixer_prompt_construction()`
- `test_retry_counter_exhaustion()`
- `test_failing_files_context_isolation()`

### Integration Tests
- `test_sandbox_fixer_closed_loop_recovery()`

### End-to-End Tests
- Greenfield generation with intentional prompt ambiguity recovering and passing within 3 tries.

### Manual Testing Checklist
- [ ] Inject syntax error into `src/components/Hero.tsx`.
- [ ] Run graph; observe UI display "Auto-healing attempt 1/3".
- [ ] Verify Fixer repairs error and sandbox completes with exit code 0.

### Regression Tests
- Re-run Phase 6, 10, and 11 tests.

### Rollback Strategy
- Cap retries at 1 to conserve token budget if API latency increases.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 4 days.

### Risks
- Fixer entering an oscillating loop (fixing error A introduces error B, fixing B re-introduces A).
- *Mitigation:* Feed cumulative error history to Fixer prompt across retries so it detects oscillations.

### Future Improvements
- Fine-tune a specialized, smaller model specifically on TypeScript AST repair diffs.

---

## Phase 13: GitHub MCP Integration & Committer Node Versioning

### Objective
Integrate the official GitHub Model Context Protocol (MCP) server to establish GitHub as the single source of truth, committing verified code to `main` and tagging versions (`vN`).

### Business Goal
Provide enterprise-grade source code ownership and version control, enabling clients to access their real GitHub repository and roll back changes safely.

### Technical Goal
Deploy the `github/github-mcp-server` client in Python, executing authenticated Git operations (create private repo, commit tree, create Git tag, manage branches).

### Features Included
- GitHub MCP client service in `backend/app/mcp/github_client.py`.
- Committer node in LangGraph (executes only after sandbox verification passes).
- Dedicated private repository creation under platform organization per project.
- Atomic commit to `main` tagged with `vN`.
- Database synchronization with `versions` table (recording commit SHA, parent version, requirements version).

### Features NOT Included
- Incremental surgical editing (Phase 14 & 15).

### Dependencies
- Phase 2 (Database), Phase 11 (Verifier Node).

### Deliverables
- GitHub MCP server wrapper module.
- `committer_node` in LangGraph.
- Integration test suite executing live Git operations against a test GitHub organization.

### Architecture Changes
- GitHub Cloud integrated as external source of truth; backend writes verified code directly to Git repositories.

### Database Changes
- Inserts new row into `versions` table with `commit_sha`, `n`, `parent_n`, and `status = 'verified'`.

### API Changes
- `GET /api/v1/projects/{id}/versions`: Returns list of all verified version tags and commit SHAs.

### Frontend Changes
- UI displays GitHub repository badge with clickable commit link and version tag pills (`v1`, `v2`).

### Backend Changes
- Committer node invoking GitHub MCP `create_or_update_file_contents` / Git Tree API.

### ML Changes
- None (deterministic code-only node).

### Infrastructure Changes
- GitHub App or fine-grained Personal Access Token provisioned with repository administration permissions.

### Configuration Required
- Platform GitHub Organization name and token.

### Environment Variables
- `GITHUB_ORG_NAME=voicetoai-projects`
- `GITHUB_APP_ID=123456`
- `GITHUB_APP_PRIVATE_KEY=...`

### Third-party Services
- GitHub Cloud API / Official GitHub MCP Server.

### Tasks
- [x] Task 13.1: Configure GitHub App with repository administration permissions.
- [x] Task 13.2: Implement GitHub MCP client in Python.
- [x] Task 13.3: Implement Committer node committing files and creating tag `vN`.
- [x] Task 13.4: Wire database record creation in `versions` table.

### Subtasks
- Subtask 13.2.1: Write tree builder creating atomic multi-file Git commit.
- Subtask 13.3.1: Implement tag creation API call (`refs/tags/vN`).

### Acceptance Criteria
- Every verified build creates a single atomic commit on `main` and a matching Git tag `v1`.
- Commit message contains structured metadata (trigger message, requirements version).
- Database `versions` table accurately mirrors GitHub commit SHA.

### Definition of Done
- Committer node verified with live GitHub test repository; PR merged.

### Unit Tests
- `test_github_mcp_payload_formatting()`
- `test_version_record_db_mapping()`

### Integration Tests
- `test_github_repo_creation_and_atomic_commit()`
- `test_git_tag_creation()`

### End-to-End Tests
- Greenfield generation from voice prompt resulting in a live verified repository on GitHub.

### Manual Testing Checklist
- [ ] Run test build; verify new private repository appears in GitHub organization.
- [ ] Inspect repository commits; verify exactly one commit on `main` tagged `v1`.
- [ ] Inspect code; verify all files match sandbox output.

### Regression Tests
- Re-run Phases 2, 7, and 11 tests.

### Rollback Strategy
- In case of GitHub API rate limits, write tarball archive to S3 bucket as temporary fallback.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 4 days.

### Risks
- GitHub API secondary rate limits during rapid parallel generation tests.
- *Mitigation:* Use authenticated GitHub App tokens with high rate limit quotas (5,000 requests/hr).

### Future Improvements
- Webhook listener to sync external developer commits back to platform database.

---

## Phase 14: File Manifest Indexing & pgvector Semantic Locator Agent

### Objective
Deploy the File Manifest Indexer and pgvector Semantic Locator to shortlist 1 to 5 affected files for modification requests using the 3-signal retrieval algorithm.

### Business Goal
Drastically reduce editing costs and latency by enabling surgical edits, avoiding catastrophic full-project regenerations.

### Technical Goal
Implement file manifest extraction (path, role, summary, exports, imports, hash) and 3-signal hybrid retrieval (pgvector cosine search + BM25 keyword matching + import graph traversal).

### Features Included
- Manifest builder: generates 1-sentence summaries and extracts AST exports/imports.
- pgvector 1536-dimensional embedding generation (`text-embedding-3-small`).
- Differential re-indexing (only changed files re-embedded; unchanged files copied).
- Production `locator_node` executing 3-signal retrieval and returning 1 to 5 files.
- Conventional routing: auto-routes copy edits to `data/site.json`.

### Features NOT Included
- Diff generation, sandbox diff application (Phase 15).

### Dependencies
- Phase 2 (Postgres + pgvector), Phase 13 (GitHub MCP & Versions).

### Deliverables
- `backend/app/services/manifest_indexer.py`.
- `backend/app/agents/locator.py`.
- 30 benchmark surgical edit retrieval evaluation scenarios.

### Architecture Changes
- PostgreSQL pgvector actively queried during `SMALL_EDIT` workflow paths.

### Database Changes
- Inserts file rows into `files` table with embeddings and HNSW indexing.

### API Changes
- Internal query interface: `await locator.locate_affected_files(project_id, version_n, prompt) -> List[str]`.

### Frontend Changes
- None (internal retrieval).

### Backend Changes
- Manifest indexing service executed immediately after Committer node succeeds.

### ML Changes
- Small LLM (Claude 3.5 Haiku) for file summarization; OpenAI `text-embedding-3-small`.

### Infrastructure Changes
- None.

### Configuration Required
- Embedding dimension: 1536; HNSW search parameter `ef_search = 40`.

### Environment Variables
- `OPENAI_API_KEY` (for embeddings).

### Third-party Services
- OpenAI Embeddings API.

### Tasks
- [x] Task 14.1: Build AST parser extracting `imports` and `exports` from TSX.
- [x] Task 14.2: Implement file summary generator using Claude 3.5 Haiku.
- [x] Task 14.3: Implement pgvector embedding storage in `files` table.
- [x] Task 14.4: Build 3-signal hybrid retrieval algorithm in SQL/Python.
- [x] Task 14.5: Run Locator accuracy evaluation across 30 edit tasks.

### Subtasks
- Subtask 14.4.1: Write SQL query combining cosine distance and keyword matching.
- Subtask 14.4.2: Implement import graph expansion in Python.

### Acceptance Criteria
- File manifest indexing completes in $<1.5\text{ seconds}$ for a 25-file repository.
- Locator identifies the exact correct files in $\ge 90\%$ of the 30 benchmark edit tasks.
- Text-only edit prompts route to `data/site.json` 100% of the time.

### Definition of Done
- Locator passes retrieval benchmark with $\ge 90\%$ accuracy; PR merged.

### Unit Tests
- `test_ast_import_export_extraction()`
- `test_file_summary_generation()`
- `test_convention_routing_rules()`

### Integration Tests
- `test_manifest_indexing_transaction()`
- `test_pgvector_similarity_search()`

### End-to-End Tests
- None.

### Manual Testing Checklist
- [ ] Index test e-commerce site.
- [ ] Query: "Change the WhatsApp order phone number".
- [ ] Verify Locator returns strictly `['data/site.json']`.
- [ ] Query: "Make the product card border rounded with a drop shadow".
- [ ] Verify Locator returns `['src/components/ProductCard.tsx']`.

### Regression Tests
- Re-run Phase 2, 7, and 13 tests.

### Rollback Strategy
- Fall back to reading entire file manifest directly in prompt if pgvector search fails.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Import graph circular references causing infinite loops in dependency traversal.
- *Mitigation:* Traversal depth strictly bounded to 1 hop (direct parents and direct children only).

### Future Improvements
- Self-hosted embedding model using Hugging Face `bge-small-en-v1.5` on CPU.

---

## Phase 15: Surgical Editor Agent & Automated Version Diff Engine

### Objective
Deploy the Editor Agent using Claude 3.5 Sonnet to produce unified diffs strictly for the 1 to 3 files shortlisted by the Locator, verifying and committing version `v(N+1)`.

### Business Goal
Enable rapid, sub-30-second site updates for pennies, providing customers with responsive iterative refinement without breaking existing features.

### Technical Goal
Implement unified diff generation, git-apply patching in the sandbox, full-project regression testing, and atomic GitHub commits for incremental versions.

### Features Included
- Production `editor_node` using Claude 3.5 Sonnet.
- Unified diff synthesizer targeting only shortlisted files.
- Patch application engine in sandbox (`git apply --check && git apply`).
- Full-project sandbox verification (ensuring edits don't break dependent components).
- Committer creates new commit and tags `v(N+1)`.
- Reversible rollback engine via tag checkout.

### Features NOT Included
- Human deployment marketplace (Phase 17).

### Dependencies
- Phase 6 (Sandbox), Phase 12 (Fixer), Phase 13 (GitHub MCP), Phase 14 (Locator).

### Deliverables
- `backend/app/agents/editor.py`.
- `backend/app/services/patcher.py`.
- Rollback service in `backend/app/services/rollback.py`.
- Frontend diff viewer component.

### Architecture Changes
- The incremental modification loop is fully operational end-to-end.

### Database Changes
- Inserts new row into `versions` linked to parent version; updates `files` content hashes.

### API Changes
- `POST /api/v1/projects/{id}/edit`: Dispatches edit workflow.
- `POST /api/v1/projects/{id}/rollback/{version_n}`: Executes rollback.

### Frontend Changes
- Version history timeline in UI with "Rollback to this version" button.
- Code diff preview drawer showing green/red line changes.

### Backend Changes
- Editor agent prompt integration; Git patch application handler.

### ML Changes
- Editor system prompt optimized for emitting clean unified diffs.

### Infrastructure Changes
- None.

### Configuration Required
- Model: `claude-3-5-sonnet-20241022`, max tokens 4000, temperature 0.1.

### Environment Variables
- `ANTHROPIC_API_KEY`.

### Third-party Services
- Anthropic Claude API, GitHub MCP.

### Tasks
- [x] Task 15.1: Implement Editor agent producing unified diffs.
- [x] Task 15.2: Implement patch application service in sandbox.
- [x] Task 15.3: Wire Editor $\to$ Sandbox $\to$ Verifier $\to$ Committer loop in LangGraph.
- [x] Task 15.4: Implement rollback API checking out historical tag.
- [x] Task 15.5: Run 30-task surgical edit benchmark measuring regression rate.

### Subtasks
- Subtask 15.2.1: Implement fallback to full file replacement if `git apply` rejects fuzzy whitespace diff.
- Subtask 15.4.1: Write Git revert / checkout tag logic via GitHub MCP.

### Acceptance Criteria
- Incremental edit modifies only the intended files, touching $\le 3$ files.
- Full sandbox build and Playwright tests pass before committing tag `v2`.
- Rollback to `v1` restores exact previous files and preview URL.
- Zero regressions across the 30 benchmark edit tasks.

### Definition of Done
- Complete edit and rollback flow verified in browser; eval benchmark passing; PR merged.

### Unit Tests
- `test_diff_parsing_and_sanitization()`
- `test_patch_application_clean()`
- `test_patch_application_reject_handling()`

### Integration Tests
- `test_end_to_end_edit_workflow()`
- `test_version_rollback_git_checkout()`

### End-to-End Tests
- User creates site (v1) $\to$ speaks edit: "Make header sticky" $\to$ site updates to v2 $\to$ user clicks rollback $\to$ site returns to v1.

### Manual Testing Checklist
- [ ] Edit headline text; verify only `data/site.json` changed in GitHub commit diff.
- [ ] Edit button color; verify only `ProductCard.tsx` changed.
- [ ] Click "Rollback to v1" in UI; assert preview immediately reverts to original state.

### Regression Tests
- Re-run all previous phase test suites.

### Rollback Strategy
- Automatic: If patch fails tests, attempt stays on draft branch and main remains untouched.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Fuzzy diffs failing to apply due to LLM line number hallucinations.
- *Mitigation:* Patcher engine attempts `git apply -3` (3-way merge) and falls back to whole-file replacement for the target file if diff fails.

### Future Improvements
- Interactive visual point-and-click element selector in the preview iframe to guide the Locator.

---

## Phase 16: Authentication, Multi-Tenant RBAC & Quota Subscriptions

### Objective
Deploy enterprise authentication, Role-Based Access Control (`user`, `developer`, `admin`), tenant project isolation, and subscription token quota management.

### Business Goal
Protect platform margins, monetize via Free/Pro subscription tiers, and prepare security boundaries for the freelance developer marketplace.

### Technical Goal
Implement JWT + Refresh token sessions, Bcrypt hashing, FastAPI security dependencies, and database-driven usage quota counters.

### Features Included
- User registration, login, and session refresh endpoints.
- Role-based authorization (`user`, `developer`, `admin`).
- Multi-tenant data isolation (users cannot view/edit other tenants' projects).
- Subscription quota enforcement middleware (checks monthly token caps before LLM runs).
- Daily usage counter updates in `usage_counters` table.

### Features NOT Included
- Live payment processing (Phase 17).

### Dependencies
- Phase 2 (Postgres Database), Phase 5 (API Gateway).

### Deliverables
- `backend/app/services/auth.py`.
- `backend/app/middleware/quota.py`.
- Frontend login, registration, and account settings pages.

### Architecture Changes
- All API and WebSocket routes protected by JWT authorization middleware.

### Database Changes
- Populates `users`, `subscriptions`, and `usage_counters` tables.

### API Changes
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/auth/me`

### Frontend Changes
- Login modal, sign-up flow, account navigation, and quota consumption meter in header.

### Backend Changes
- Security dependencies: `get_current_user`, `require_role`, `check_quota_available`.

### ML Changes
- None.

### Infrastructure Changes
- None.

### Configuration Required
- JWT secret key, token expiration times (Access: 60m, Refresh: 30d).

### Environment Variables
- `JWT_SECRET_KEY=super-secret-hex-key-change-in-prod`
- `JWT_ALGORITHM=HS256`

### Third-party Services
- None.

### Tasks
- [x] Task 16.1: Implement password hashing and JWT encoding/decoding.
- [x] Task 16.2: Build registration and login endpoints.
- [x] Task 16.3: Implement multi-tenant project ownership check dependency.
- [x] Task 16.4: Implement quota enforcement middleware checking monthly token burn.
- [x] Task 16.5: Build frontend authentication state provider and login forms.

### Subtasks
- Subtask 16.1.1: Configure `pwd_context` with bcrypt 12 rounds.
- Subtask 16.4.1: Write atomic SQL counter increment for `tokens_consumed`.

### Acceptance Criteria
- User cannot access or modify projects owned by another user (returns HTTP 404).
- User who exceeds monthly token quota receives HTTP 402 / friendly upgrade modal.
- Passwords stored in database are salt-hashed; plain text is never logged.

### Definition of Done
- Auth and quota security suite passes 100% of penetration and isolation tests; PR merged.

### Unit Tests
- `test_password_hashing_and_verification()`
- `test_jwt_signature_validation()`
- `test_quota_middleware_blocks_exhausted_plan()`

### Integration Tests
- `test_multi_tenant_isolation_enforcement()`
- `test_login_and_token_refresh_lifecycle()`

### End-to-End Tests
- Playwright test: register new account $\to$ login $\to$ create project $\to$ verify token counter increments.

### Manual Testing Checklist
- [ ] Create User A and User B.
- [ ] User A creates Project 1.
- [ ] Attempt to load Project 1 using User B's token; verify access is forbidden.
- [ ] Manually set User A's token usage to limit in database; assert next prompt is blocked by quota.

### Regression Tests
- Re-run all previous API tests with authorization headers attached.

### Rollback Strategy
- In emergency, set `BYPASS_QUOTA_CHECK=true` environment variable.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 4 days.

### Risks
- Token leakage via client-side storage vulnerabilities.
- *Mitigation:* Store refresh tokens in `HttpOnly`, `SameSite=Strict`, `Secure` cookies.

### Future Improvements
- Social login (Google / GitHub OAuth).

---

## Phase 17: Human-in-the-Loop Marketplace & Double-Entry Ledger Engine

### Objective
Deploy the Human-in-the-Loop (HITL) Deployment Marketplace, connecting shop owners with verified developers via dedicated chat workrooms, mock escrow payments, and an immutable double-entry ledger.

### Business Goal
Solve the production deployment bottleneck, monetize via a 20% platform commission on developer deployments, and maintain zero regulatory banking risk via an internal ledger.

### Technical Goal
Implement deployment ticket lifecycle, scoped GitHub token dispensing, real-time WebSocket workroom chat, mock payment gateway, and balanced double-entry accounting engine (`ledger_entries`).

### Features Included
- Deployment ticket creation for verified version `vN`.
- Admin assignment portal to dispatch developers.
- Scoped temporary read-only GitHub token generation for assigned developer.
- Dedicated client-developer WebSocket chat room.
- Developer quote submission and client payment approval.
- Double-entry ledger engine enforcing $\sum \text{Debits} = \sum \text{Credits}$.
- Monthly developer payout report generation.

### Features NOT Included
- Real money banking integration (mock gateway with manual bank transfers).

### Dependencies
- Phase 2 (Database Ledger), Phase 13 (GitHub MCP), Phase 16 (Auth & RBAC).

### Deliverables
- `backend/app/services/marketplace.py`.
- `backend/app/services/ledger.py`.
- `frontend/components/marketplace/WorkroomChat.tsx`.
- Admin payout dashboard in `frontend/app/admin/payouts/`.

### Architecture Changes
- Marketplace module connects Users, Developers, and Admins into collaborative workrooms.

### Database Changes
- Writes to `deployment_requests`, `quotes`, `payments`, `ledger_entries`, `payout_periods`, `payouts`.

### API Changes
- `POST /api/v1/marketplace/requests`
- `POST /api/v1/marketplace/quotes`
- `POST /api/v1/marketplace/pay`
- `POST /api/v1/marketplace/confirm-live`
- `GET /api/v1/admin/payouts/report`

### Frontend Changes
- "Deploy to Live Domain" modal in client UI.
- Developer portal dashboard showing assigned tickets and earnings.
- Admin dashboard showing platform ledger balance and pending payouts.

### Backend Changes
- Double-entry ledger service with strict database transaction locking.

### ML Changes
- None.

### Infrastructure Changes
- None.

### Configuration Required
- Platform commission percentage: 20%.

### Environment Variables
- `PLATFORM_COMMISSION_RATE=0.20`

### Third-party Services
- Mock Payment Gateway API.

### Tasks
- [x] Task 17.1: Implement deployment request state machine.
- [x] Task 17.2: Build scoped GitHub installation token dispenser for developers.
- [x] Task 17.3: Build real-time WebSocket chat room for client and developer.
- [x] Task 17.4: Implement double-entry ledger service with mathematical verification.
- [x] Task 17.5: Build monthly payout report generator.

### Subtasks
- Subtask 17.4.1: Write database transaction enforcing debit/credit balance.
- Subtask 17.5.1: Generate CSV export of monthly developer balances.

### Acceptance Criteria
- Every payment, fee, and payout creates balanced ledger rows ($\sum \text{Debits} = \sum \text{Credits}$).
- Assigned developer receives read-only GitHub token valid strictly for assigned repository.
- Client approval releases escrow, allocating 20% to platform and 80% to developer balance.

### Definition of Done
- Complete end-to-end marketplace flow successfully demonstrated from ticket to payout report; PR merged.

### Unit Tests
- `test_ledger_double_entry_balance_invariant()`
- `test_commission_split_exact_math()`
- `test_quote_status_transitions()`

### Integration Tests
- `test_full_marketplace_lifecycle_transaction()`
- `test_scoped_github_token_dispenser()`

### End-to-End Tests
- Full multi-role Playwright test: Shop Owner requests deployment $\to$ Admin assigns Developer $\to$ Developer quotes $\$30$ $\to$ Owner pays $\to$ Developer marks live $\to$ Owner confirms $\to$ Ledger balances.

### Manual Testing Checklist
- [ ] Open 3 browser windows: Client, Developer, Admin.
- [ ] Request deployment as Client; assign Developer as Admin.
- [ ] Send message in workroom; verify real-time arrival in both windows.
- [ ] Submit quote as Developer; pay quote as Client.
- [ ] Inspect `ledger_entries` table in database; verify debits equal credits to the exact cent.

### Regression Tests
- Re-run all previous phase test suites.

### Rollback Strategy
- Transactions wrap all ledger operations; failure triggers immediate rollback without partial state.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Race conditions during concurrent payment confirmation releasing escrow twice.
- *Mitigation:* `SELECT ... FOR UPDATE` row-level locks on `deployment_requests` and `payments`.

### Future Improvements
- Safepay / JazzCash live gateway integration for Pakistani market.

---

## Phase 18: Observability, Langfuse Tracing & Full Benchmark Evaluation Suite

### Objective
Deploy enterprise telemetry with Langfuse tracing, Prometheus metrics, structured JSON logging, and the complete quantitative FYP evaluation benchmark suite.

### Business Goal
Ensure complete cost transparency, provide academic reviewers with empirical performance proof, and detect model latency drift proactively.

### Technical Goal
Wrap all agent invocations with Langfuse SDK, export Prometheus metrics, and automate the 4 benchmark evaluation suites (ASR, Clarifier, Coder, Locator).

### Features Included
- Langfuse tracing on 100% of LLM calls with token, latency, and cost attribution.
- Prometheus metrics endpoint `/metrics` (request rates, latency histograms, error counts).
- Structured JSON logging with correlation IDs (`trace_id`, `project_id`, `version_n`).
- Automated FYP evaluation runner script in `evals/run_all_benchmarks.py`.

### Features NOT Included
- Production cloud deployment (Phase 19).

### Dependencies
- All previous phases (Phases 1 to 17).

### Deliverables
- `backend/app/observability/langfuse.py`.
- `backend/app/observability/metrics.py`.
- `evals/run_all_benchmarks.py` producing markdown evaluation report.

### Architecture Changes
- Telemetry middleware wraps FastAPI application and LangGraph nodes.

### Database Changes
- None (populates existing `runs` table).

### API Changes
- `GET /metrics`: Prometheus scrape endpoint.

### Frontend Changes
- None.

### Backend Changes
- Loguru structured JSON log configuration.

### ML Changes
- None.

### Infrastructure Changes
- Prometheus and Grafana containers added to Docker Compose.

### Configuration Required
- Langfuse public/secret keys and host URL.

### Environment Variables
- `LANGFUSE_PUBLIC_KEY=pk-lf-...`
- `LANGFUSE_SECRET_KEY=sk-lf-...`
- `LANGFUSE_HOST=https://cloud.langfuse.com`

### Third-party Services
- Langfuse Cloud (or self-hosted).

### Tasks
- [x] Task 18.1: Integrate Langfuse client with LangGraph node decorator.
- [x] Task 18.2: Implement Prometheus metrics collector in FastAPI.
- [x] Task 18.3: Configure structured JSON logger with correlation IDs.
- [x] Task 18.4: Build automated evaluation runner executing all 4 benchmarks.
- [x] Task 18.5: Generate baseline evaluation report.

### Subtasks
- Subtask 18.4.1: Run 30 ASR audio clips and calculate WER.
- Subtask 18.4.2: Run 20 Clarifier personas and measure turns to ready.
- Subtask 18.4.3: Run 30 Greenfield build scenarios and measure pass rate.
- Subtask 18.4.4: Run 30 Surgical edit tasks and measure accuracy.

### Acceptance Criteria
- 100% of LLM completions log input/output tokens, latency, and cost to Langfuse.
- Automated evaluation runner executes cleanly via single command: `poetry run python -m evals.run_all_benchmarks`.
- All acceptance criteria targets met: ASR WER $\le 14\%$, Clarifier turns $\le 3$, Build success $\ge 85\%$, Edit accuracy $\ge 90\%$.

### Definition of Done
- Evaluation report generated and committed to `docs/EVALUATION_REPORT.md`; PR merged.

### Unit Tests
- `test_langfuse_metadata_formatting()`
- `test_prometheus_metrics_export()`

### Integration Tests
- `test_trace_emission_during_graph_run()`

### End-to-End Tests
- Execution of full benchmark suite in CI test environment.

### Manual Testing Checklist
- [ ] Open Langfuse dashboard.
- [ ] Run a test generation; verify trace tree displays Router $\to$ Clarifier $\to$ Planner $\to$ Coder.
- [ ] Verify token count matches database `runs` table.
- [ ] Scrape `/metrics`; verify Prometheus metrics increment.

### Regression Tests
- Re-run all existing test suites.

### Rollback Strategy
- Toggle `LANGFUSE_ENABLED=false` to silence telemetry if network latency occurs.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 4 days.

### Risks
- Network timeouts to Langfuse blocking core user generation workflows.
- *Mitigation:* Langfuse spans dispatched asynchronously in non-blocking background threads.

### Future Improvements
- Automated prompt regression alerts triggered when benchmark scores drop $>5\%$.

---

## Phase 19: Containerization, Reverse Proxy, SSL & Production CI/CD Pipeline

### Objective
Containerize the entire platform with production multi-stage Dockerfiles, Traefik reverse proxy, automated Let's Encrypt SSL, and complete GitHub Actions CI/CD deployment pipelines.

### Business Goal
Achieve production readiness with zero-downtime deployments, high availability, and automated testing gates preventing broken code from reaching production.

### Technical Goal
Author production `Dockerfile.backend` and `Dockerfile.frontend`, configure Traefik with automated ACME SSL, and build GitHub Actions workflows for continuous integration and continuous deployment.

### Features Included
- Production multi-stage Dockerfiles for Next.js frontend and FastAPI backend.
- `docker-compose.prod.yml` with Traefik v3 reverse proxy and SSL automation.
- GitHub Actions CI workflow: linting, contract validation, unit tests, integration tests.
- GitHub Actions CD workflow: automated container build, push to registry, and SSH deployment to production server.

### Features NOT Included
- Multi-region disaster recovery replication (Phase 20).

### Dependencies
- All previous phases (Phases 1 to 18).

### Deliverables
- `deploy/Dockerfile.frontend`.
- `deploy/Dockerfile.backend`.
- `deploy/docker-compose.prod.yml`.
- `.github/workflows/ci.yml` and `.github/workflows/cd.yml`.

### Architecture Changes
- System deployed in fully containerized production topology fronted by Traefik edge router.

### Database Changes
- None.

### API Changes
- None.

### Frontend Changes
- Optimized production build bundle (`output: 'standalone'`).

### Backend Changes
- Production Uvicorn worker process configuration with Gunicorn process manager.

### ML Changes
- None.

### Infrastructure Changes
- Cloud VPS (Ubuntu 24.04 LTS), DNS A-records pointing to server IP, port 80/443 exposed.

### Configuration Required
- Domain name, Let's Encrypt email address, Docker registry credentials.

### Environment Variables
- `DOMAIN_NAME=voicetoai.com`
- `LETSENCRYPT_EMAIL=admin@voicetoai.com`
- `DOCKER_REGISTRY_USER=...`
- `DOCKER_REGISTRY_TOKEN=...`

### Third-party Services
- GitHub Actions, Docker Hub / GitHub Container Registry (GHCR), Let's Encrypt.

### Tasks
- [x] Task 19.1: Author multi-stage Dockerfile for Next.js frontend.
- [x] Task 19.2: Author multi-stage Dockerfile for FastAPI backend.
- [x] Task 19.3: Configure Traefik reverse proxy with automatic HTTPS SSL.
- [x] Task 19.4: Build GitHub Actions CI pipeline running full test suite on PRs.
- [x] Task 19.5: Build GitHub Actions CD pipeline deploying to production VPS.

### Subtasks
- Subtask 19.1.1: Ensure frontend Dockerfile uses non-root `nextjs` user.
- Subtask 19.4.1: Configure Docker-in-Docker service container for sandbox integration tests in CI.

### Acceptance Criteria
- Pushing to `main` triggers automated CI; if tests pass, CD builds containers and deploys.
- Accessing domain over HTTP automatically redirects to HTTPS with valid Let's Encrypt certificate.
- Frontend, Backend, Postgres, and MinIO restart cleanly on server reboot.

### Definition of Done
- Application deployed and running on live staging/production server with valid SSL; PR merged.

### Unit Tests
- `test_dockerfile_syntax_validation()`

### Integration Tests
- `test_production_docker_compose_up()`

### End-to-End Tests
- Automated synthetic health check pinging live production HTTPS endpoint.

### Manual Testing Checklist
- [ ] Visit `https://your-domain.com` in browser.
- [ ] Inspect SSL certificate in browser lock icon; verify Let's Encrypt authority.
- [ ] Create a project; verify voice recording and preview work over production HTTPS/WSS.

### Regression Tests
- Re-run all integration test suites.

### Rollback Strategy
- CD workflow retains previous container tag; one-click rollback script: `docker-compose -f docker-compose.prod.yml up -d --no-deps backend:previous`.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Let's Encrypt rate limits triggered during domain configuration testing.
- *Mitigation:* Use Let's Encrypt Staging ACME server until domain configuration is verified.

### Future Improvements
- Kubernetes (K8s) deployment manifests using Helm charts for enterprise clustering.

---

## Phase 20: System Hardening, Load Testing, Disaster Recovery & Final FYP Delivery

### Objective
Execute comprehensive security audits, load testing (50 concurrent users), automated database backups, disaster recovery rehearsal, and prepare the final FYP defense demonstration.

### Business Goal
Guarantee absolute platform stability, data security, and flawless presentation delivery for the Final Year Project university evaluation committee.

### Technical Goal
Execute Locust load test scripts, configure automated pg_dump backups to S3, run OWASP ZAP security scans, and conduct 3 end-to-end rehearsals of the 8-minute defense demo.

### Features Included
- Automated daily PostgreSQL backup script uploading encrypted dumps to S3.
- One-command disaster recovery restore script (`scripts/restore_db.sh`).
- Locust load testing suite simulating 50 concurrent users creating and editing sites.
- Security hardening (OWASP top 10 audit, rate limiting verification, CORS lockdown).
- Final FYP presentation and demonstration rehearsal runbook.

### Features NOT Included
- New speculative feature developments (Scope frozen).

### Dependencies
- All previous phases (Phases 1 to 19).

### Deliverables
- `scripts/backup_db.sh` and `scripts/restore_db.sh`.
- `tests/load/locustfile.py`.
- Security audit report in `docs/SECURITY_AUDIT.md`.
- Final 8-minute defense demo video recording backup.

### Architecture Changes
- System locked and frozen for production delivery.

### Database Changes
- None (automated snapshot cron configured).

### API Changes
- None.

### Frontend Changes
- Polish UI error states, responsive mobile view adjustments, and celebratory animations.

### Backend Changes
- Final log cleanup and production rate limit tuning.

### ML Changes
- None.

### Infrastructure Changes
- Cron job for daily database backups; offsite backup replication.

### Configuration Required
- Production backup encryption passphrase.

### Environment Variables
- `BACKUP_ENCRYPTION_KEY=...`

### Third-party Services
- S3 Offsite Backup Storage.

### Tasks
- [x] Task 20.1: Implement and test automated database backup and restore scripts.
- [x] Task 20.2: Run Locust load test benchmark with 50 concurrent active sessions.
- [x] Task 20.3: Execute OWASP security vulnerability scan and patch findings.
- [x] Task 20.4: Conduct 3 live demo rehearsals following the 8-minute defense script.
- [x] Task 20.5: Record high-definition offline backup demo video.

### Subtasks
- Subtask 20.1.1: Simulate catastrophic database wipe and execute restore script.
- Subtask 20.4.1: Seed demo database with reproducible shop owner personas.

### Acceptance Criteria
- Database restore script restores full platform state from S3 backup in $<3\text{ minutes}$.
- System handles 50 concurrent users with 0 server crashes and P95 latency $< 1.2\text{s}$.
- Zero high or critical vulnerabilities detected in OWASP security audit.
- 8-minute live demo script executes cleanly end-to-end.

### Definition of Done
- All 20 implementation phases complete; documentation and demo video packaged; FYP ready for defense.

### Unit Tests
- `test_backup_script_integrity()`

### Integration Tests
- `test_disaster_recovery_restore_cycle()`

### End-to-End Tests
- Execution of the complete 8-minute demo script from voice prompt to developer payout.

### Manual Testing Checklist
- [ ] Shop owner speaks request in Urdu/English; transcript confirmed.
- [ ] Clarifier asks option questions; shop owner answers with one "you decide".
- [ ] Requirements summary confirmed; live build executes in sandbox.
- [ ] Preview iframe opens showing verified site; GitHub commit and tag `v1` visible.
- [ ] Shop owner speaks edit: "Make the header sticky"; only affected file changes; tagged `v2`.
- [ ] Roll back to `v1` to demonstrate version control.
- [ ] Request deployment; assign developer; chat in workroom; pay quote; confirm live site.
- [ ] Open admin ledger; verify balanced double-entry accounts and developer payout report.

### Regression Tests
- Full platform regression test run across all 20 phases.

### Rollback Strategy
- Restore system from tested hourly automated S3 database snapshot.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Live demo failure due to external LLM API downtime during committee presentation.
- *Mitigation:* Pre-record high-definition backup demo video; maintain seeded local cached runs.

### Future Improvements
- Post-graduation commercial SaaS launch with live Safepay payment gateway and marketing rollout.
