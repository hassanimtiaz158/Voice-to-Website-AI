# Voice-to-Website AI: Complete Engineering Documentation
## Enterprise Master Documentation Index & Single Source of Truth

---

### Project Overview
**Voice-to-Website AI** is an enterprise-grade autonomous software engineering SaaS platform. A non-technical shop owner describes their dream website in natural spoken voice (Urdu, English, or Roman Urdu) or text. An orchestrated multi-agent system conducts a diagnostic interview, extracts verified specifications, plans a bespoke architecture, generates real component-based code (`vite-react-tailwind`), compiles and executes the code inside a hardened, isolated sandbox, and runs automated visual and functional verification checks.

Every verified version is version-controlled via GitHub commits (`v1`, `v2`, ... `vN`). Subsequent modification requests use semantic file-manifest retrieval with pgvector to surgically locate and edit only the affected 1 to 3 files. When the business owner is ready to go live, the platform bridges the digital divide with a **Human-in-the-Loop (HITL) Marketplace**, connecting the client to verified developers via a dedicated escrow-backed workroom with an automated double-entry ledger.

---

## Master Documentation Catalog

| Document | File Link | Description & Key Contents |
|---|---|---|
| **Product Requirements Document (PRD)** | [PRD.md](file:///d:/VoicetoAI/docs/PRD.md) | Personas (Tariq Khan, Zainab Ahmed, Admin), core user journeys, functional and non-functional requirements, acceptance criteria. |
| **Technical Design Document (TDD)** | [TDD.md](file:///d:/VoicetoAI/docs/TDD.md) | Detailed technical architecture, LangGraph state machine specs, inter-agent Pydantic contracts, complete PostgreSQL 16 + pgvector DDL, double-entry financial math. |
| **Architecture Plan** | [ARCHITECTURE.md](file:///d:/VoicetoAI/docs/ARCHITECTURE.md) | C4 Model (Context, Container, Component diagrams), sequence diagrams for Greenfield, Edit, Sandbox, and Marketplace flows, STRIDE threat model. |
| **Complete Implementation Roadmap** | [IMPLEMENTATION_ROADMAP.md](file:///d:/VoicetoAI/docs/IMPLEMENTATION_ROADMAP.md) | 20 independent, small-scoped, fully testable phases with all 33 mandatory technical sections per phase. |
| **Milestone Plan** | [MILESTONES.md](file:///d:/VoicetoAI/docs/MILESTONES.md) | 16-week milestone breakdown (M0 to M5), 4-member vertical slice ownership, team review ring rules, prioritized scope cut lines. |
| **Folder Structure Plan** | [FOLDER_STRUCTURE.md](file:///d:/VoicetoAI/docs/FOLDER_STRUCTURE.md) | Monorepo layout for `contracts/`, `backend/`, `frontend/`, `scaffolds/`, `evals/`, `deploy/`, and `docs/`. |
| **Repository Strategy** | [REPOSITORY_STRATEGY.md](file:///d:/VoicetoAI/docs/REPOSITORY_STRATEGY.md) | Trunk-based development, branch naming, Ring Review peer review protocol, conventional commits, GitHub MCP integration. |
| **Testing Strategy** | [TESTING.md](file:///d:/VoicetoAI/docs/TESTING.md) | Test pyramid (Unit, Contract, Integration, Playwright Smoke, Performance), double-entry ledger invariant tests, quantitative benchmark harness. |
| **DevOps Strategy** | [DEVOPS.md](file:///d:/VoicetoAI/docs/DEVOPS.md) | Production Dockerfiles, Traefik v3 reverse proxy, automated Let's Encrypt SSL, secrets management, AES-256 automated backup/restore scripts. |
| **CI/CD Strategy** | [CICD.md](file:///d:/VoicetoAI/docs/CICD.md) | Multi-stage GitHub Actions workflows for continuous integration (lint, typecheck, contracts, tests, security) and continuous deployment. |
| **MLOps Strategy** | [MLOPS.md](file:///d:/VoicetoAI/docs/MLOPS.md) | Prompt versioning, evaluation datasets, model tiering (Haiku vs Sonnet), prompt caching cost reduction, drift detection alerts. |
| **Deployment Strategy** | [DEPLOYMENT.md](file:///d:/VoicetoAI/docs/DEPLOYMENT.md) | Cloud VPS deployment topology, instant preview URL architecture (screenshots + sandboxed iframes), zero-downtime rolling updates. |
| **Risk Assessment** | [RISK_ASSESSMENT.md](file:///d:/VoicetoAI/docs/RISK_ASSESSMENT.md) | Complete risk register: build failure mitigations, token runaway circuit breakers, sandbox memory caps, live demo backup rehearsals. |
| **Future Roadmap** | [FUTURE_ROADMAP.md](file:///d:/VoicetoAI/docs/FUTURE_ROADMAP.md) | Post-FYP commercialization: Next.js full-stack apps, automated custom domains with Caddy, Safepay Pakistani gateway, Urdu voice bot. |
| **Project Management Plan** | [PROJECT_MANAGEMENT.md](file:///d:/VoicetoAI/docs/PROJECT_MANAGEMENT.md) | Epics, INVEST user stories, 8 two-week sprint schedule, Trello/Jira board layout, Definition of Done (DoD). |

---

## Feature Specifications Catalog (`docs/FEATURE_SPECS/`)

| Feature Specification | File Link | Focus & Invariants |
|---|---|---|
| **Voice Processing & Streaming** | [VoicePipeline.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/VoicePipeline.md) | Audio normalization, Silero VAD, Whisper bilingual ASR with Pakistani retail lexicon priming, transcript confirmation modal. |
| **Multi-Agent Orchestration** | [Agents_Orchestration.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Agents_Orchestration.md) | LangGraph state graph, Router, Clarifier, Planner, Coder, Fixer, prompt templates, 300k token run ceiling. |
| **Semantic Manifest Search (RAG)** | [RAG_ManifestSearch.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/RAG_ManifestSearch.md) | File-level manifest in PostgreSQL, pgvector HNSW indexing, 3-signal retrieval, conventional routing (`data/site.json`). |
| **Sandboxed Execution Engine** | [Sandboxing_Execution.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Sandboxing_Execution.md) | E2B microVM / Docker isolation, 2GB RAM cap, pre-cached npm dependencies, 5-stage build, Playwright smoke checks. |
| **Authentication & RBAC** | [Authentication_RBAC.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Authentication_RBAC.md) | Multi-tenant isolation, JWT sessions, User/Developer/Admin roles, scoped 4-hour GitHub App tokens, subscription quotas. |
| **Marketplace & Double-Entry Ledger** | [Marketplace_Deployment_Ledger.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Marketplace_Deployment_Ledger.md) | Human-in-the-loop deployment tickets, workroom chat, mock escrow, immutable double-entry ledger ($\sum \text{Debits} = \sum \text{Credits}$). |
| **Observability & Evaluation** | [Monitoring_Logging_Evaluation.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Monitoring_Logging_Evaluation.md) | Langfuse tracing, Prometheus telemetry, structured JSON logs, 4 automated quantitative evaluation benchmarks. |

---

## 3 Core Inviolable Laws
1. **Code Controls the Flow:** A deterministic LangGraph state machine governs execution routing. LLMs never decide the next state freely.
2. **Verify with Tools, Not Opinions:** A version is NEVER marked complete until sandbox TypeScript compilation, linting, production build, and Playwright smoke tests exit with code 0.
3. **Clarify Before Generating:** No code is written until the user explicitly confirms a structured requirements summary.
