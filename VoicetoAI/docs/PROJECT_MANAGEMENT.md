# Project Management & Agile Execution Plan
## Epics, Features, User Stories (INVEST), Sprint Schedule & Governance

---

### Document Metadata
- **Document Version:** 2.0.0
- **Status:** APPROVED & LOCKED
- **Methodology:** Agile / Scrum with 2-Week Sprints (8 Sprints Total across 16 Weeks)
- **Board Configuration:** Trello / Jira (`Backlog`, `This Week`, `In Progress`, `In Review`, `Done`)

---

## 1. Epic & Feature Hierarchy

```
┌────────────────────────────────────────────────────────────────────────┐
│                        EPIC & FEATURE HIERARCHY                        │
├────────────────────────────────────────────────────────────────────────┤
│ EPIC 1: Multilingual Voice Ingestion & Audio Processing                │
│   ├── FEAT-1.1: Web Audio Recording & Normalization                     │
│   ├── FEAT-1.2: Voice Activity Detection (VAD) & Silence Gating         │
│   ├── FEAT-1.3: Bilingual Whisper ASR with Retail Lexicon Priming      │
│   └── FEAT-1.4: Mandatory Transcript Confirmation Modal                 │
├────────────────────────────────────────────────────────────────────────┤
│ EPIC 2: Deterministic Multi-Agent State Machine (LangGraph)            │
│   ├── FEAT-2.1: Tri-Modal Request Routing (Question, Edit, Create)     │
│   ├── FEAT-2.2: 3-Turn Diagnostic Clarifier with "You Decide" Fallback │
│   ├── FEAT-2.3: Stack-Aware Architectural File Planner                  │
│   ├── FEAT-2.4: Sequential Single-File Coder Agent                     │
│   └── FEAT-2.5: Self-Healing Fixer Agent with 3-Retry Budget           │
├────────────────────────────────────────────────────────────────────────┤
│ EPIC 3: Hardened Sandboxed Execution & Automated Verification          │
│   ├── FEAT-3.1: MicroVM / Docker Sandbox Runner with 2GB RAM Cap       │
│   ├── FEAT-3.2: Pre-Cached Scaffold Dependency Hydration               │
│   ├── FEAT-3.3: 5-Stage Build Pipeline (npm ci, tsc, lint, build)       │
│   └── FEAT-3.4: Headless Playwright DOM & Layout Overflow Verification │
├────────────────────────────────────────────────────────────────────────┤
│ EPIC 4: Semantic Manifest Search & GitHub Version Control              │
│   ├── FEAT-4.1: PostgreSQL + pgvector Manifest & 1536d Embeddings      │
│   ├── FEAT-4.2: 3-Signal Hybrid Retrieval (Vector + BM25 + AST Graph)  │
│   ├── FEAT-4.3: Surgical Editor Agent (Unified Diffs for 1-3 Files)    │
│   ├── FEAT-4.4: GitHub MCP Committer Node (Tag vN Synchronization)     │
│   └── FEAT-4.5: Reversible Git Tag Rollback Engine                     │
├────────────────────────────────────────────────────────────────────────┤
│ EPIC 5: Enterprise Multi-Tenancy & Human Deployment Marketplace        │
│   ├── FEAT-5.1: JWT Authentication & Role-Based Access Control (RBAC)  │
│   ├── FEAT-5.2: Subscription Quotas & Token Burn Rate Limiting         │
│   ├── FEAT-5.3: Deployment Tickets & Scoped Read-Only GitHub Tokens    │
│   ├── FEAT-5.4: Dedicated Client-Developer WebSocket Workrooms        │
│   └── FEAT-5.5: Double-Entry Accounting Ledger Engine (Debits=Credits) │
├────────────────────────────────────────────────────────────────────────┤
│ EPIC 6: Observability, Evaluation Harnesses & Production Operations    │
│   ├── FEAT-6.1: Langfuse End-to-End LLM Tracing & Cost Tracking        │
│   ├── FEAT-6.2: Prometheus Metrics & Grafana Operational Dashboard     │
│   ├── FEAT-6.3: Automated Quantitative FYP Benchmark Suite (30 items)  │
│   └── FEAT-6.4: Production CI/CD Pipeline & Traefik Automated SSL      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core User Stories (INVEST Criteria)

### US-01: Multilingual Voice Note Ingestion
- **Story:** *As a non-technical shop owner*, I want to *record a voice note in Urdu or English describing my shop*, so that *I don't have to type long technical prompts on a mobile keyboard*.
- **Acceptance Criteria:**
  - Recording starts on mic click with animated waveform visualizer.
  - VAD automatically detects 1.8 seconds of trailing silence and stops recording.
  - Transcript appears in an editable confirmation modal within $<2\text{ seconds}$.
  - User can edit misspelled business names before confirming.

### US-02: Guided Decision Making (Clarification)
- **Story:** *As a merchant with no design experience*, I want to *answer 3 simple multiple-choice questions with a "You Decide" option*, so that *I am not blocked by technical design decisions*.
- **Acceptance Criteria:**
  - Clarifier never exceeds 3 turns of questions.
  - Every question presents 3 to 4 clickable options including "You Decide".
  - Selecting "You Decide" stores an AI-selected default in the `decisions` audit table.
  - Final requirements summary requires explicit user confirmation before generation.

### US-03: Autonomous Code Generation & Sandboxed Verification
- **Story:** *As the platform operator*, I want *AI-generated code to compile and pass Playwright tests in an isolated sandbox*, so that *broken code is never committed to GitHub or displayed to users*.
- **Acceptance Criteria:**
  - Sandbox compiles `vite-react-tailwind` within a 2GB RAM / 300s limit.
  - Compiler errors trigger Fixer self-healing loop (up to 3 retries).
  - Playwright audits DOM for console errors and horizontal layout overflow.
  - Verified code is committed to GitHub and tagged `v1`.

### US-04: Surgical Incremental Modifications
- **Story:** *As a shop owner reviewing my preview*, I want to *say "Make the Buy Now button gold" and have only the button change*, so that *the rest of my working site is not broken or regenerated*.
- **Acceptance Criteria:**
  - Locator isolates strictly 1 to 3 affected files using pgvector manifest search.
  - Editor produces unified diffs; untouched files remain identical.
  - Sandbox verifies full build with diff applied.
  - Changes committed as tag `v2` with sub-30-second turnaround.

### US-05: Instant Git Version Rollback
- **Story:** *As a shop owner who dislikes an edit*, I want to *click "Rollback to v1"*, so that *my website instantly reverts to its previous working state*.
- **Acceptance Criteria:**
  - Version timeline displays all verified tags (`v1`, `v2`, ...).
  - Clicking rollback checks out historical tag via GitHub MCP.
  - Preview iframe updates immediately; active pointer resets to chosen version.

### US-06: Human Deployment with Escrow Protection
- **Story:** *As a merchant ready to launch*, I want to *hire a verified developer through the platform with escrow protection*, so that *my custom domain is set up safely by a human without financial fraud*.
- **Acceptance Criteria:**
  - Ticket created; Admin assigns vetted developer.
  - Developer receives scoped 4-hour read-only GitHub token.
  - Developer submits fixed quote; Client deposits funds into escrow.
  - Client confirms live domain; double-entry ledger deducts 20% commission and credits 80% developer balance.

---

## 3. Sprint Schedule (8 Sprints Across 16 Weeks)

| Sprint | Weeks | Primary Focus & Milestones | Key Sprint Deliverable |
|---|---|---|---|
| **Sprint 1** | Weeks 1 – 2 | **Milestone M0:** Foundations, Contracts & Spikes | Monorepo setup, Pydantic contracts, 4 de-risking spikes passed. |
| **Sprint 2** | Weeks 3 – 4 | **Milestone M1 (Part 1):** Persistence, Router & Scaffold | Postgres + pgvector schema, LangGraph skeleton, Coder scaffold. |
| **Sprint 3** | Weeks 5 – 6 | **Milestone M1 (Part 2) & M2:** Sandbox, Verifier & Clarifier | E2B runner, Playwright smoke tests, Clarifier with `interrupt()`. |
| **Sprint 4** | Weeks 7 – 8 | **Milestone M2 (Completion):** Voice Flow & Greenfield v1 | Bilingual Whisper ASR, transcript modal, live preview, GitHub v1. |
| **Sprint 5** | Weeks 9 – 10 | **Milestone M3 (Part 1):** File Manifest RAG & Surgical Edit | Manifest indexer, pgvector search, Locator, Editor unified diffs. |
| **Sprint 6** | Weeks 11 – 12 | **Milestone M3 (Completion) & M4:** Rollback & Marketplace Shell| Version history UI, rollback engine, deployment tickets, RBAC auth. |
| **Sprint 7** | Weeks 13 – 14 | **Milestone M4 (Completion):** Escrow Ledger & Workroom | Workroom chat, quotes, double-entry ledger engine, payout reports. |
| **Sprint 8** | Weeks 15 – 16 | **Milestone M5:** System Hardening, Evals & FYP Defense | 30-scenario evals report, load test, 8-min demo rehearsal, backup video. |

---

## 4. Definition of Done (DoD) Checklist

A user story or task is considered **DONE** if and only if it satisfies all of the following criteria:
- [ ] **Code Complete:** Implemented strictly in accordance with architectural contracts.
- [ ] **Contract Compliant:** Pydantic schemas in `contracts/` verified with zero regressions.
- [ ] **Automated Tests Passing:** Unit, integration, and sandbox tests pass in CI with zero failures.
- [ ] **Ring Peer Reviewed:** Pull request approved by designated member in the review ring.
- [ ] **Traced & Costed:** All LLM operations emit complete traces to Langfuse.
- [ ] **Demoed on Friday:** Functionality demonstrated live in the weekly team demo sync.
- [ ] **Documented:** Relevant markdown documentation in `docs/` updated.
