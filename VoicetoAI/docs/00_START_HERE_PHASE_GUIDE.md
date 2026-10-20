# 00 START HERE: Master Phase Navigation & Execution Guide
## How to Identify Which Phase is Which, Which to Start With, and What Comes Next

---

### Why This Guide Exists
If you open the `docs/` folder and don't know where to start, which document is Phase 1, or which phase comes next, **this document is your single source of truth**.

Every single phase has its own dedicated specification file inside the [docs/PHASES/](file:///d:/VoicetoAI/docs/PHASES) directory, numbered from **`PHASE_01`** to **`PHASE_20`**.

---

## 1. Quick Answer: Which Phase is Phase 1 and Where Do I Start?

👉 **Start here:** Open [PHASE_01_Repo_Setup_and_Contracts.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_01_Repo_Setup_and_Contracts.md)

At the top of every phase document, you will find a **Navigation Header** that tells you:
- Current Phase
- Previous Phase
- Next Phase
- Master Guide Link
- Related Architecture Specs

---

## 2. Master Chronological Phase Roadmap (Phases 1 to 20)

Follow these phases sequentially. **Do not skip ahead.** Every phase must pass its tests before moving to the next.

| Phase # | Phase File Link | Phase Name | What It Builds | Related Spec |
|:---:|:---|:---|:---|:---|
| **01** | [PHASE_01_Repo_Setup_and_Contracts.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_01_Repo_Setup_and_Contracts.md) | **Repository & Contracts** | Scaffolding, pre-commit hooks, Pydantic V2 data contracts | [FOLDER_STRUCTURE.md](file:///d:/VoicetoAI/docs/FOLDER_STRUCTURE.md) |
| **02** | [PHASE_02_Postgres_and_pgvector.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_02_Postgres_and_pgvector.md) | **PostgreSQL & pgvector** | 16 relational tables, Alembic migrations, HNSW vector index | [TDD.md](file:///d:/VoicetoAI/docs/TDD.md) |
| **03** | [PHASE_03_S3_Storage_and_Audio_Validation.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_03_S3_Storage_and_Audio_Validation.md) | **S3 Storage & Audio Gate** | MinIO/S3 async client, audio format & loudness energy check | [VoicePipeline.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/VoicePipeline.md) |
| **04** | [PHASE_04_Whisper_ASR_and_Transcript.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_04_Whisper_ASR_and_Transcript.md) | **Bilingual Whisper ASR** | Speech-to-text with Pakistani retail lexicon priming, modal | [VoicePipeline.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/VoicePipeline.md) |
| **05** | [PHASE_05_VAD_and_Audio_Streaming.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_05_VAD_and_Audio_Streaming.md) | **Voice Activity Detection** | Silero VAD, 1.8s trailing silence stop, WebSocket streaming | [VoicePipeline.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/VoicePipeline.md) |
| **06** | [PHASE_06_Scaffold_and_Sandbox_Runner.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_06_Scaffold_and_Sandbox_Runner.md) | **Scaffolds & Sandbox Runner** | E2B microVM / Docker, 2GB RAM cap, pre-cached npm dependencies | [Sandboxing_Execution.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Sandboxing_Execution.md) |
| **07** | [PHASE_07_LangGraph_and_Checkpointer.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_07_LangGraph_and_Checkpointer.md) | **LangGraph State Machine** | Cyclic state graph, PostgresSaver checkpointer, interrupt() | [Agents_Orchestration.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Agents_Orchestration.md) |
| **08** | [PHASE_08_Router_and_Clarifier_Agent.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_08_Router_and_Clarifier_Agent.md) | **Router & Clarifier Agent** | Claude 3.5 Haiku, 3-turn interview, "You Decide", decisions DB | [Agents_Orchestration.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Agents_Orchestration.md) |
| **09** | [PHASE_09_Architectural_Planner_Agent.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_09_Architectural_Planner_Agent.md) | **Stack Architectural Planner** | Claude 3.5 Sonnet, data/site.json central copy separation | [Agents_Orchestration.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Agents_Orchestration.md) |
| **10** | [PHASE_10_Sequential_Coder_Agent.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_10_Sequential_Coder_Agent.md) | **Sequential Coder Agent** | File-by-file TSX/Tailwind code generator, WebSocket progress | [Agents_Orchestration.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Agents_Orchestration.md) |
| **11** | [PHASE_11_Playwright_Verifier_Node.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_11_Playwright_Verifier_Node.md) | **Playwright Visual Verifier** | Headless DOM audit, layout overflow check, S3 screenshot | [Sandboxing_Execution.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Sandboxing_Execution.md) |
| **12** | [PHASE_12_Fixer_Agent_Self_Healing.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_12_Fixer_Agent_Self_Healing.md) | **Targeted Fixer Self-Healing** | Autonomously patches compiler/lint errors (max 3 retries) | [Agents_Orchestration.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Agents_Orchestration.md) |
| **13** | [PHASE_13_GitHub_MCP_Committer.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_13_GitHub_MCP_Committer.md) | **GitHub MCP & Committer** | Commits verified tree to main, tags vN, syncs versions DB | [REPOSITORY_STRATEGY.md](file:///d:/VoicetoAI/docs/REPOSITORY_STRATEGY.md) |
| **14** | [PHASE_14_File_Manifest_pgvector_Locator.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_14_File_Manifest_pgvector_Locator.md) | **Manifest pgvector Locator** | 3-signal hybrid retrieval (pgvector + BM25 + AST graph) | [RAG_ManifestSearch.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/RAG_ManifestSearch.md) |
| **15** | [PHASE_15_Surgical_Editor_and_Rollback.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_15_Surgical_Editor_and_Rollback.md) | **Surgical Editor & Rollback** | Unified diff patches for 1-3 files, instant Git tag rollback | [RAG_ManifestSearch.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/RAG_ManifestSearch.md) |
| **16** | [PHASE_16_Auth_RBAC_and_Quotas.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_16_Auth_RBAC_and_Quotas.md) | **Auth, RBAC & Subscriptions** | JWT sessions, User/Dev/Admin roles, monthly token quota guard | [Authentication_RBAC.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Authentication_RBAC.md) |
| **17** | [PHASE_17_Marketplace_and_Escrow_Ledger.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_17_Marketplace_and_Escrow_Ledger.md) | **Human Marketplace & Ledger** | Tickets, workroom chat, mock escrow, double-entry ledger math | [Marketplace_Deployment_Ledger.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Marketplace_Deployment_Ledger.md) |
| **18** | [PHASE_18_Observability_and_Eval_Suite.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_18_Observability_and_Eval_Suite.md) | **Observability & FYP Evals** | Langfuse traces, Prometheus metrics, 4 benchmark eval suites | [Monitoring_Logging_Evaluation.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Monitoring_Logging_Evaluation.md) |
| **19** | [PHASE_19_Docker_Traefik_SSL_and_CICD.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_19_Docker_Traefik_SSL_and_CICD.md) | **Docker, Traefik, SSL & CI/CD** | Multi-stage Dockerfiles, Let's Encrypt SSL, GitHub Actions CD | [DEVOPS.md](file:///d:/VoicetoAI/docs/DEVOPS.md), [CICD.md](file:///d:/VoicetoAI/docs/CICD.md) |
| **20** | [PHASE_20_Hardening_Recovery_and_Ship.md](file:///d:/VoicetoAI/docs/PHASES/PHASE_20_Hardening_Recovery_and_Ship.md) | **Hardening, Recovery & Defense** | 50-user load test, S3 backup/restore, 8-min defense script | [RISK_ASSESSMENT.md](file:///d:/VoicetoAI/docs/RISK_ASSESSMENT.md) |

---

## 3. How to Execute Each Phase

Every phase file contains exactly **33 sections**. When implementing a phase:
1. Open the phase document (e.g., `PHASE_01_Repo_Setup_and_Contracts.md`).
2. Read the **Objective**, **Business Goal**, and **Technical Goal**.
3. Implement the list under **Tasks** and **Subtasks**.
4. Run the commands specified in **Unit Tests** and **Integration Tests**.
5. Go through the **Manual Testing Checklist**.
6. Verify the **Acceptance Criteria** and **Definition of Done**.
7. Run the **Regression Tests** (ensure previous phases didn't break).
8. Once verified, click the **Next Phase** link at the top of the file to move forward!
