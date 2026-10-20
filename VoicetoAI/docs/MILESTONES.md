# Milestone Plan: Voice-to-Website AI
## 16-Week Production Execution Plan & Team Ownership Allocation

---

### Document Metadata
- **Document Version:** 2.0.0
- **Status:** APPROVED & LOCKED
- **Timeline:** 16 Weeks (Milestones M0 to M5)
- **Team Size:** 4 Software Engineers (Equal ~25% Load Across Vertical Slices)

---

## 1. Team Ownership & Vertical Slice Allocation

The engineering work is divided into four distinct end-to-end vertical slices. Each member owns their slice across backend, agents, UI, tests, and evaluation harness to prevent frontend/backend silos.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FOUR VERTICAL TEAM SLICES                       │
├────────────────────────────────────────────────────────────────────────┤
│ MEMBER 1: Conversation & Requirements Lead                             │
│ • Voice recording, audio normalization, Whisper ASR, transcript modal  │
│ • Chat UI with streaming WebSockets; tri-modal Router agent            │
│ • Clarifier agent with interrupt() and checkpointer; decisions table   │
│ • Requirements schema vN, summary modal, user confirmation flow        │
│ • Subscription plans & monthly token quota enforcement                 │
├────────────────────────────────────────────────────────────────────────┤
│ MEMBER 2: Generation Engine & Build Lead                               │
│ • Pinned scaffold (vite-react-tailwind) with cached dependencies       │
│ • Planner agent (stack-aware architecture & data/site.json separation) │
│ • Sequential Coder agent (file-by-file generation)                     │
│ • Sandbox runner (E2B microVM / local Docker fallback, 2GB RAM cap)    │
│ • Self-healing Fixer agent (max 3 retries, targeted compiler stderr)   │
│ • 30-scenario build benchmark eval harness & build-log streaming UI    │
├────────────────────────────────────────────────────────────────────────┤
│ MEMBER 3: Edit, RAG & Versioning Lead                                  │
│ • PostgreSQL + pgvector manifest schema, HNSW indexing & S3 setup      │
│ • Manifest builder (AST parser, Haiku summaries, 1536d embeddings)     │
│ • Semantic Locator agent (3-signal hybrid retrieval & convention rules)│
│ • Surgical Editor agent (unified diff generation for 1-3 files only)   │
│ • GitHub MCP Committer node (one private repo per project, vN tagging) │
│ • Version history timeline & instant Git rollback UI                   │
│ • 30-task surgical edit benchmark eval harness                         │
├────────────────────────────────────────────────────────────────────────┤
│ MEMBER 4: Delivery, Business & Operations Lead                         │
│ • Automated Verifier node (Playwright headless smoke tests, screenshot)│
│ • Live preview URL serving architecture                                │
│ • Authentication, JWT sessions & Role-Based Access Control (RBAC)      │
│ • Human deployment marketplace: tickets, admin dispatch, workroom chat │
│ • Double-entry accounting ledger engine (debits = credits invariant)   │
│ • Mock escrow payment gateway & monthly developer payout reports       │
│ • Langfuse observability tracing & Prometheus system metrics           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Working Agreements & Team Rhythm

1. **Ring Review Rule:** All pull requests are reviewed by the next team member in a ring:
   $$\text{Member 1} \longrightarrow \text{Member 2} \longrightarrow \text{Member 3} \longrightarrow \text{Member 4} \longrightarrow \text{Member 1}$$
   This guarantees that every engineer deeply understands at least two vertical slices and can demo any part of the system if a member is unavailable.
2. **Weekly Sprint Rhythm:**
   - **Monday 09:30 AM (30 min):** Sprint planning, roadmap alignment, blocker identification.
   - **Wednesday 02:00 PM (15 min):** Mid-week sanity sync and contract PR review.
   - **Friday 04:00 PM (45 min):** End-to-end live demo of whatever works in staging. Log cumulative LLM API spend.
3. **Contracts First:** All cross-slice boundaries are defined as Pydantic schemas in `contracts/`. A contract can only be modified via a dedicated PR approved by all four members.

---

## 3. Detailed 16-Week Milestone Plan

```
Weeks: 01   02   03   04   05   06   07   08   09   10   11   12   13   14   15   16
       [─── M0 ───] [────── M1 ──────] [────── M2 ──────] [────── M3 ──────] [────── M4 ──────] [── M5 ──]
       De-Risk Spikes   Build Engine      Create Flow       Edit & RAG      Marketplace/Money   Harden & Ship
```

### Milestone M0: Align, Spike & De-Risk (Weeks 1 – 2)
- **Primary Objective:** Validate high-risk technical assumptions through 4 isolated engineering spikes and freeze inter-service contracts.
- **Weekly Deliverables:**
  - *Week 1:* Initialize Monorepo, CI linting, and author all Pydantic schemas in `contracts/`.
  - *Week 2:* Execute 4 mandatory spikes:
    - **Member 1 Spike:** Run Whisper ASR on 25 Urdu/English audio clips; measure baseline WER and transcribe latency.
    - **Member 2 Spike:** Execute `npm ci`, `tsc`, `lint`, and `build` in E2B microVM at 2GB RAM; verify no memory OOM crash.
    - **Member 3 Spike:** Have GitHub MCP client create a private repo, commit sample files, and tag `v1`.
    - **Member 4 Spike:** Serve a static build at a preview URL and capture a full-page screenshot using Playwright.
- **Exit Criteria:** All 4 spikes pass or have named architectural fallbacks; contracts PR merged; all open design questions resolved.

---

### Milestone M1: Core Build Engine (Weeks 3 – 5)
- **Primary Objective:** Build an autonomous headless engine that takes a structured prompt and generates a compiling, verified website.
- **Weekly Deliverables:**
  - *Week 3:* Member 1 builds LangGraph skeleton and Router node. Member 3 builds Postgres + pgvector schema and S3 bucket setup.
  - *Week 4:* Member 2 integrates Planner and sequential Coder with `vite-react-tailwind` scaffold. Member 4 implements JWT auth, user models, and Langfuse tracing.
  - *Week 5:* Member 2 connects E2B sandbox runner. Member 4 wires Verifier node (Playwright smoke tests).
- **Exit Criteria:** 10 scripted benchmark prompts produce a working site that builds in the sandbox via an API call with zero UI needed; each slice has passing automated unit tests.

---

### Milestone M2: Greenfield Create Flow (Weeks 6 – 8)
- **Primary Objective:** Connect conversational voice/text front-end to the build engine, delivering the complete user-facing creation flow.
- **Weekly Deliverables:**
  - *Week 6:* Member 1 implements Clarifier agent with `interrupt()` and checkpointer. Member 2 tunes Fixer agent error recovery loop.
  - *Week 7:* Member 1 integrates voice recording with transcript confirmation modal. Member 3 implements GitHub Committer node with `versions` table synchronization.
  - *Week 8:* Member 4 wires dynamic preview iframe and S3 screenshot display. Full end-to-end integration test.
- **Exit Criteria:** A user can speak or type in the browser, answer clarification questions, confirm requirements, and receive a verified site committed to GitHub as `v1` with a live preview.

---

### Milestone M3: Surgical Edit & Versioning (Weeks 9 – 11)
- **Primary Objective:** Deploy the file manifest RAG pipeline, enabling fast, low-cost surgical edits and instant version rollbacks.
- **Weekly Deliverables:**
  - *Week 9:* Member 3 implements AST manifest extractor, pgvector embeddings, and Locator agent. Member 1 wires Q&A path and quota checks.
  - *Week 10:* Member 3 implements Editor agent (diff generation) and Git rollback engine. Member 2 builds the 30-scenario build benchmark eval suite.
  - *Week 11:* Member 4 builds deployment ticket schemas and admin dashboard skeleton. Member 3 builds version history UI.
- **Exit Criteria:** Edit requests touch only 1 to 3 expected files; rollback restores exact prior commit; first comprehensive evaluation benchmark report published.

---

### Milestone M4: Human Deployment Marketplace & Financial Ledger (Weeks 12 – 14)
- **Primary Objective:** Complete the human-in-the-loop deployment workflow and the double-entry accounting ledger engine.
- **Weekly Deliverables:**
  - *Week 12:* Member 4 implements deployment tickets, developer assignment, and dedicated WebSocket workrooms. Member 1 enforces subscription plan quotas end-to-end.
  - *Week 13:* Member 4 implements developer quotes, mock escrow payment, and balanced double-entry ledger (`ledger_entries`). Member 2 tunes token caps and global step timeouts.
  - *Week 14:* Member 4 builds monthly developer payout reports. Member 3 runs 30-task surgical edit regression evaluation.
- **Exit Criteria:** Full deployment story functions end-to-end (Request $\to$ Assign $\to$ Quote $\to$ Pay $\to$ Deploy $\to$ Confirm $\to$ Ledger Settle); double-entry math proven balanced on every transaction.

---

### Milestone M5: Hardening, Polish & Final Defense (Weeks 15 – 16)
- **Primary Objective:** System load testing, disaster recovery rehearsal, security audit, and final FYP presentation preparation.
- **Weekly Deliverables:**
  - *Week 15:* Member 1 executes bilingual Urdu ASR evaluation. Member 2 implements `static-html` profile (stretch goal). Member 3 polishes version history UI. Member 4 hardens error states.
  - *Week 16:* Team executes full evaluation benchmark run, conducts 3 live demo rehearsals of the 8-minute defense script, and records an offline backup demo video.
- **Exit Criteria:** All acceptance criteria measured and documented; zero high-severity bugs; project ready for committee defense.

---

## 4. Prioritized Scope Cut Line

If the team falls behind schedule due to unexpected technical hurdles, scope must be shed strictly in the following pre-agreed sequence:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PRIORITIZED CUT LINE                            │
├────────────────────────────────────────────────────────────────────────┤
│ 1. CUT FIRST: static-html stack profile (keep vite-react-tailwind).   │
│ 2. CUT SECOND: Claude vision-based screenshot judge in Verifier.       │
│ 3. CUT THIRD: Dynamic subscription quota upgrades (use hardcoded caps).│
│ 4. CUT FOURTH: WebSocket chat fallback to HTTP polling.               │
│ 5. CUT FIFTH: Payout report PDF formatting (keep CSV/JSON ledger).     │
├────────────────────────────────────────────────────────────────────────┤
│                       NEVER CUT UNDER ANY CIRCUMSTANCE                 │
│ • Sandboxed build verification (npm ci, tsc, lint, build, Playwright). │
│ • GitHub MCP version control and commit tagging (v1, v2).              │
│ • Human-in-the-loop deployment marketplace with balanced ledger.       │
│ • Voice audio input with transcript confirmation modal.                │
└────────────────────────────────────────────────────────────────────────┘
```
