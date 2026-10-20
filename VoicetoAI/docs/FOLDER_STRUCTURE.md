# Folder Structure Plan: Voice-to-Website AI
## Enterprise Monorepo Directory Layout & Module Responsibilities

---

### Document Metadata
- **Document Version:** 2.0.0
- **Status:** APPROVED & LOCKED
- **Standard:** Clean architecture separation, isolated contracts, and strict dependency boundaries.

---

## 1. Complete Monorepo Directory Tree

```
d:/VoicetoAI/
├── .github/                               # CI/CD Workflows & GitHub Automation
│   ├── workflows/
│   │   ├── ci.yml                         # Lint, contract check, unit & integration tests
│   │   ├── cd.yml                         # Build production containers & deploy to VPS
│   │   └── evals.yml                      # Weekly automated benchmark evaluation run
│   └── pull_request_template.md           # Ring review checklist & DOD verification
│
├── contracts/                             # Shared Pydantic V2 Data Schemas (Zero DB Dependencies)
│   ├── __init__.py
│   ├── requirements.py                    # RequirementsContract schema
│   ├── plan.py                            # PlanContract schema
│   ├── build_result.py                    # BuildResultContract schema
│   ├── file_edit.py                       # FileEditContract & SingleFileDiff schemas
│   ├── version_record.py                  # VersionRecordContract schema
│   ├── deployment_request.py              # DeploymentRequestContract schema
│   └── tests/                             # Contract validation & serialization tests
│       ├── test_requirements.py
│       └── test_plan.py
│
├── backend/                               # Core FastAPI & Python Agentic Platform
│   ├── alembic/                           # Database Migrations
│   │   ├── env.py
│   │   └── versions/                      # Reversible migration scripts
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                        # FastAPI entry point & CORS configuration
│   │   ├── config.py                      # Pydantic Settings (Environment variables)
│   │   ├── api/                           # REST & WebSocket API Routers
│   │   │   ├── v1/
│   │   │   │   ├── auth.py                # Registration, login, token refresh
│   │   │   │   ├── projects.py            # Project creation, listing, metadata
│   │   │   │   ├── voice.py               # Audio upload, normalization, transcribe
│   │   │   │   ├── edit.py                # Incremental surgical edit endpoints
│   │   │   │   ├── rollback.py            # Historical tag rollback endpoint
│   │   │   │   ├── marketplace.py         # Deployment tickets, quotes, escrow payment
│   │   │   │   └── admin.py               # Developer assignment, payouts, ledger view
│   │   │   └── websockets/
│   │   │       ├── ws_chat.py             # Streaming chat & agent status events
│   │   │       ├── ws_voice.py            # Real-time audio streaming & VAD
│   │   │       └── ws_workroom.py         # Client-developer marketplace chat
│   │   ├── models/                        # SQLAlchemy 2.0 Relational & Vector Models
│   │   │   ├── base.py
│   │   │   ├── user.py                    # users, subscriptions, usage_counters
│   │   │   ├── project.py                 # projects, messages, requirements, decisions
│   │   │   ├── version.py                 # versions, files (with pgvector embedding)
│   │   │   ├── execution.py               # runs (observability & cost tracking)
│   │   │   └── ledger.py                  # deployment_requests, quotes, payments, ledger_entries
│   │   ├── agents/                        # Autonomous AI Agent Implementations
│   │   │   ├── router.py                  # Claude 3.5 Haiku Tri-Modal Classifier
│   │   │   ├── clarifier.py               # Claude 3.5 Haiku 3-Turn Diagnostic Interviewer
│   │   │   ├── planner.py                 # Claude 3.5 Sonnet Stack-Aware Architect
│   │   │   ├── coder.py                   # Claude 3.5 Sonnet File-by-File Generator
│   │   │   ├── locator.py                 # pgvector 3-Signal Hybrid Manifest Search
│   │   │   ├── editor.py                  # Claude 3.5 Sonnet Unified Diff Synthesizer
│   │   │   ├── fixer.py                   # Claude 3.5 Sonnet Self-Healing Agent
│   │   │   └── verifier.py                # Playwright DOM & Vision Judge Node
│   │   ├── orchestrator/                  # LangGraph Deterministic State Machine
│   │   │   ├── state.py                   # ProjectGraphState TypedDict
│   │   │   ├── graph.py                   # StateGraph assembly, conditional edges
│   │   │   └── checkpointer.py            # AsyncPostgresSaver configuration
│   │   ├── sandbox/                       # Isolated MicroVM Execution Engine
│   │   │   ├── runner.py                  # SandboxRunner abstract base interface
│   │   │   ├── e2b_runner.py              # E2B Firecracker MicroVM implementation
│   │   │   ├── docker_runner.py           # Local Docker unprivileged runner fallback
│   │   │   └── error_parser.py            # TypeScript & ESLint regex trace extractor
│   │   ├── mcp/                           # Model Context Protocol Integrations
│   │   │   └── github_client.py           # GitHub MCP client (commit, tag, branch, repo)
│   │   ├── services/                      # Core Business & Infrastructure Logic
│   │   │   ├── asr.py                     # Whisper ASR with retail domain priming
│   │   │   ├── vad.py                     # Silero VAD silence boundary detection
│   │   │   ├── storage.py                 # Asynchronous S3 / MinIO client
│   │   │   ├── audio_validator.py         # Format, duration, and loudness energy checker
│   │   │   ├── manifest_indexer.py        # File summary & 1536d embedding generation
│   │   │   ├── ledger.py                  # Double-entry accounting transaction engine
│   │   │   └── github_token.py            # Scoped temporary installation token dispenser
│   │   ├── middleware/                    # HTTP Middleware
│   │   │   ├── auth.py                    # JWT Bearer token validator & RBAC guard
│   │   │   ├── quota.py                   # Monthly token & edit quota enforcer
│   │   │   └── logging.py                 # Structured JSON request logger & trace_id
│   │   └── observability/                 # Telemetry & Monitoring
│   │       ├── langfuse.py                # Langfuse LLM trace wrapper
│   │       └── metrics.py                 # Prometheus latency histograms & counters
│   ├── pyproject.toml                     # Poetry Python dependencies
│   └── tests/                             # Backend Test Suite
│       ├── unit/                          # Isolated function & model tests
│       └── integration/                   # Database, S3, Sandbox & Graph tests
│
├── frontend/                              # Next.js 15 App Router Frontend (React 19)
│   ├── src/
│   │   ├── app/                           # App Router Pages
│   │   │   ├── layout.tsx                 # Root layout with providers
│   │   │   ├── page.tsx                   # Landing page & feature overview
│   │   │   ├── dashboard/                 # User project management portal
│   │   │   ├── project/[id]/              # Main workspace (Chat, Preview, Versions)
│   │   │   ├── marketplace/               # Client deployment workroom portal
│   │   │   ├── developer/                 # Freelancer deployment ticket portal
│   │   │   └── admin/                     # Admin ledger, users, and payout reports
│   │   ├── components/                    # Reusable React UI Components
│   │   │   ├── voice/                     # VoiceRecorder, Waveform, TranscriptModal
│   │   │   ├── chat/                      # ChatStream, ClarifierCards, SummaryCard
│   │   │   ├── preview/                   # PreviewFrame, ScreenshotView, DeviceToggle
│   │   │   ├── versions/                  # VersionTimeline, DiffViewer, RollbackButton
│   │   │   ├── marketplace/               # QuoteCard, EscrowModal, WorkroomChat
│   │   │   └── ui/                        # Buttons, Modals, Badges, Tabs (Tailwind)
│   │   ├── hooks/                         # Custom React Hooks
│   │   │   ├── useVoiceRecorder.ts        # Browser MediaRecorder & VAD integration
│   │   │   ├── useProjectWebSocket.ts     # Real-time build logs & chat streaming
│   │   │   └── useAuth.ts                 # JWT session & RBAC role state
│   │   ├── lib/                           # Utility Functions
│   │   │   ├── api_client.ts              # Fetch wrapper with auto-refresh token
│   │   │   └── constants.ts               # Stack profiles, default colors
│   │   └── styles/
│   │       └── globals.css                # Tailwind CSS v4 directives & design tokens
│   ├── package.json
│   └── tailwind.config.ts
│
├── scaffolds/                             # Pinned Stack Templates for Greenfield Builds
│   └── vite-react-tailwind/               # Pinned Primary Stack Profile
│       ├── package.json                   # Pinned dependency versions (React 19, Vite, Tailwind)
│       ├── tsconfig.json                  # TypeScript strict: true
│       ├── vite.config.ts                 # Vite build & preview configuration
│       ├── tailwind.config.js             # Pre-configured color tokens & utility classes
│       ├── index.html                     # HTML5 entry with mobile viewport tags
│       ├── src/
│       │   ├── main.tsx
│       │   ├── App.tsx                    # Root component rendering from data/site.json
│       │   ├── components/                # Base modular UI primitives
│       │   └── index.css
│       └── data/
│           └── site.json                  # Mandatory Central Copy & Configuration Source
│
├── evals/                                 # Automated FYP Evaluation Harness
│   ├── audio_clips/                       # 30 Bilingual Urdu/English audio clips (.wav)
│   ├── personas/                          # 20 Scripted shop owner persona prompts (.json)
│   ├── build_scenarios/                   # 30 Greenfield retail business prompts (.json)
│   ├── edit_tasks/                        # 30 Surgical modification tasks (.json)
│   ├── asr_eval.py                        # JiWER Word Error Rate benchmark runner
│   ├── clarifier_eval.py                  # Turns-to-ready evaluation script
│   ├── build_benchmark.py                 # Greenfield headless sandbox compilation runner
│   ├── locator_eval.py                    # Recall@K and Precision@K retrieval runner
│   └── run_all_benchmarks.py              # Master evaluation script compiling Markdown report
│
├── deploy/                                # Production Infrastructure & Container Configs
│   ├── Dockerfile.backend                 # Multi-stage Python 3.12 production image
│   ├── Dockerfile.frontend                # Multi-stage Next.js 15 standalone image
│   ├── docker-compose.yml                 # Local development stack (Postgres, MinIO)
│   ├── docker-compose.prod.yml            # Production stack with Traefik reverse proxy
│   ├── traefik/                           # Traefik v3 configuration & Let's Encrypt SSL
│   │   └── traefik.yml
│   └── sandbox-base/                      # Base image for E2B/Docker sandbox runner
│       └── Dockerfile.sandbox
│
├── scripts/                               # Maintenance & Operational Automation
│   ├── seed_db.py                         # Seeds plans, test users, and mock projects
│   ├── backup_db.sh                       # PostgreSQL encrypted dump to S3
│   └── restore_db.sh                      # Automated disaster recovery restore script
│
└── docs/                                  # Project Documentation (Single Source of Truth)
    ├── PRD.md
    ├── TDD.md
    ├── IMPLEMENTATION_ROADMAP.md
    ├── MILESTONES.md
    ├── ARCHITECTURE.md
    ├── FOLDER_STRUCTURE.md
    ├── REPOSITORY_STRATEGY.md
    ├── TESTING.md
    ├── DEVOPS.md
    ├── CICD.md
    ├── MLOPS.md
    ├── DEPLOYMENT.md
    ├── RISK_ASSESSMENT.md
    ├── FUTURE_ROADMAP.md
    ├── PROJECT_MANAGEMENT.md
    └── FEATURE_SPECS/
        ├── VoicePipeline.md
        ├── Agents_Orchestration.md
        ├── RAG_ManifestSearch.md
        ├── Sandboxing_Execution.md
        ├── Authentication_RBAC.md
        ├── Marketplace_Deployment_Ledger.md
        └── Monitoring_Logging_Evaluation.md
```
