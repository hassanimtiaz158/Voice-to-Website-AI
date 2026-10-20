# Voice-to-Website AI: Complete Engineering Documentation
## Enterprise Master Documentation Index & Single Source of Truth

---

### Project Overview
**Voice-to-Website AI** is an enterprise-grade autonomous software engineering SaaS platform. A non-technical shop owner describes their dream website in natural spoken voice (Urdu, English, or Roman Urdu) or text. An orchestrated multi-agent system conducts a diagnostic interview, extracts verified specifications, plans a bespoke architecture, generates real component-based code (`vite-react-tailwind`), compiles and executes the code inside a hardened, isolated sandbox, and runs automated visual and functional verification checks.

Every verified version is version-controlled via GitHub commits (`v1`, `v2`, ... `vN`). Subsequent modification requests use semantic file-manifest retrieval with pgvector to surgically locate and edit only the affected 1 to 3 files. When the business owner is ready to go live, the platform bridges the digital divide with a **Human-in-the-Loop (HITL) Marketplace**, connecting the client to verified developers via a dedicated escrow-backed workroom with an automated double-entry ledger.

---

## 🚀 START HERE: Phase-by-Phase Implementation Guide

If you are looking for which phase to work on first and what comes next:
👉 **Open [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)**

All 20 individual phase documents are located in the [docs/PHASES/](file:///d:/VoicetoAI/docs/PHASES) folder:
- **Phase 1:** [PHASE_01_Repo_Setup_and_Contracts.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_01_Repo_Setup_and_Contracts.md)
- **Phase 2:** [PHASE_02_Postgres_and_pgvector.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_02_Postgres_and_pgvector.md)
- **Phase 3:** [PHASE_03_S3_Storage_and_Audio_Validation.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_03_S3_Storage_and_Audio_Validation.md)
- **Phase 4:** [PHASE_04_Whisper_ASR_and_Transcript.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_04_Whisper_ASR_and_Transcript.md)
- **Phase 5:** [PHASE_05_VAD_and_Audio_Streaming.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_05_VAD_and_Audio_Streaming.md)
- **Phase 6:** [PHASE_06_Scaffold_and_Sandbox_Runner.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_06_Scaffold_and_Sandbox_Runner.md)
- **Phase 7:** [PHASE_07_LangGraph_and_Checkpointer.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_07_LangGraph_and_Checkpointer.md)
- **Phase 8:** [PHASE_08_Router_and_Clarifier_Agent.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_08_Router_and_Clarifier_Agent.md)
- **Phase 9:** [PHASE_09_Architectural_Planner_Agent.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_09_Architectural_Planner_Agent.md)
- **Phase 10:** [PHASE_10_Sequential_Coder_Agent.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_10_Sequential_Coder_Agent.md)
- **Phase 11:** [PHASE_11_Playwright_Verifier_Node.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_11_Playwright_Verifier_Node.md)
- **Phase 12:** [PHASE_12_Fixer_Agent_Self_Healing.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_12_Fixer_Agent_Self_Healing.md)
- **Phase 13:** [PHASE_13_GitHub_MCP_Committer.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_13_GitHub_MCP_Committer.md)
- **Phase 14:** [PHASE_14_File_Manifest_pgvector_Locator.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_14_File_Manifest_pgvector_Locator.md)
- **Phase 15:** [PHASE_15_Surgical_Editor_and_Rollback.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_15_Surgical_Editor_and_Rollback.md)
- **Phase 16:** [PHASE_16_Auth_RBAC_and_Quotas.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_16_Auth_RBAC_and_Quotas.md)
- **Phase 17:** [PHASE_17_Marketplace_and_Escrow_Ledger.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_17_Marketplace_and_Escrow_Ledger.md)
- **Phase 18:** [PHASE_18_Observability_and_Eval_Suite.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_18_Observability_and_Eval_Suite.md)
- **Phase 19:** [PHASE_19_Docker_Traefik_SSL_and_CICD.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_19_Docker_Traefik_SSL_and_CICD.md)
- **Phase 20:** [PHASE_20_Hardening_Recovery_and_Ship.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_20_Hardening_Recovery_and_Ship.md)

---

## Master Architecture Documentation Catalog

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
