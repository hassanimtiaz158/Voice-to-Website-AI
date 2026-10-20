# Technical Design Document (TDD)
## Voice-to-Website AI: Enterprise Autonomous Web Generation & Human Deployment Platform

---

### Document Metadata
- **Document Version:** 2.0.0
- **Status:** APPROVED & LOCKED
- **Author:** Principal AI Architect & Staff Backend Engineering Team
- **Target Audience:** Core Engineering Team, DevOps Leads, Security Architects
- **Related Documents:** [PRD](file:///d:/VoicetoAI/docs/PRD.md), [Architecture Plan](file:///d:/VoicetoAI/docs/ARCHITECTURE.md), [Implementation Roadmap](file:///d:/VoicetoAI/docs/IMPLEMENTATION_ROADMAP.md)

---

## 1. System Architecture Overview

The Voice-to-Website AI platform is a distributed, event-driven, multi-agent platform designed to autonomously generate, verify, and modify production-ready web applications while offering human-assisted deployment.

```
                           ┌───────────────────────────┐
                           │   Next.js 15 Web & PWA    │
                           │   (Voice / Chat / Preview)│
                           └─────────────┬─────────────┘
                                         │ HTTPS / WSS
                                         ▼
                           ┌───────────────────────────┐
                           │   FastAPI Gateway Router  │
                           │  (Auth, Quotas, Endpoints)│
                           └──────┬──────────────┬─────┘
                                  │              │
                   ┌──────────────┘              └──────────────┐
                   ▼                                            ▼
       ┌────────────────────────┐                   ┌───────────────────────┐
       │ Whisper ASR Service    │                   │ LangGraph Orchestrator│
       │ (Urdu/English Audio)   │                   │ (State Graph Machine) │
       └───────────┬────────────┘                   └───────────┬───────────┘
                   │                                            │
                   ▼                                            ▼
       ┌────────────────────────┐                   ┌───────────────────────┐
       │ AWS S3 Audio / Snaps   │                   │ PostgreSQL 16 + Vector│
       │ (Object Storage)       │                   │ (Checkpointer/Manifest│
       └────────────────────────┘                   └─────┬───────────┬─────┘
                                                          │           │
                                 ┌────────────────────────┘           └───────────────┐
                                 ▼                                                    ▼
                     ┌───────────────────────┐                            ┌───────────────────────┐
                     │ E2B Sandbox Runner    │                            │ GitHub MCP Server     │
                     │ (Isolated MicroVM)    │                            │ (Commit, Tag, Branch) │
                     └───────────────────────┘                            └───────────────────────┘
```

---

## 2. LangGraph State Machine Specification

The agentic pipeline is modeled as a cyclic state machine governed by LangGraph. All state transitions are deterministic, enforced in Python code, and persisted after every node execution using the `PostgresSaver` checkpointer.

### 2.1 State Schema (`ProjectGraphState`)
```python
from typing import TypedDict, List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

class ProjectGraphState(TypedDict):
    # Context & Identifiers
    project_id: str
    user_id: str
    thread_id: str
    current_version: int
    current_req_version: int
    
    # Input Processing
    user_input_type: Literal["voice", "text"]
    audio_s3_key: Optional[str]
    raw_transcript: Optional[str]
    confirmed_prompt: str
    request_type: Literal["QUESTION", "SMALL_EDIT", "NEW_OR_MAJOR"]
    
    # Clarification Engine
    clarification_turn: int
    clarifier_questions: List[Dict[str, Any]]
    clarifier_answers: Dict[str, Any]
    clarification_complete: bool
    requirements_summary: Optional[Dict[str, Any]]
    requirements_confirmed: bool
    
    # Planning & Code Generation
    stack_profile: Literal["vite-react-tailwind", "static-html"]
    file_plan: List[Dict[str, str]]  # [{"path": "...", "role": "...", "action": "create|modify"}]
    generated_files: Dict[str, str]  # {path: file_content}
    
    # Surgical Edit Flow
    shortlisted_files: List[str]
    file_diffs: Dict[str, str]      # {path: unified_diff}
    
    # Sandbox & Verification
    sandbox_id: Optional[str]
    build_exit_code: Optional[int]
    build_logs: str
    test_failures: Optional[str]
    fixer_retry_count: int
    verification_passed: bool
    dom_snapshot_url: Optional[str]
    screenshot_s3_key: Optional[str]
    
    # Git & Publication
    commit_sha: Optional[str]
    git_tag: Optional[str]
    preview_url: Optional[str]
    error_message: Optional[str]
```

### 2.2 LangGraph Nodes & Responsibilities
1. **`router_node`**: High-speed classification using Claude 3.5 Haiku. Evaluates `confirmed_prompt` and project state to route to `answer_question`, `locator_node`, or `clarifier_node`.
2. **`clarifier_node`**: Evaluates requirements completeness. Formulates 3 to 5 multi-choice questions. Invokes `interrupt()` to await human response.
3. **`planner_node`**: Uses Claude 3.5 Sonnet to translate verified requirements into an explicit, dependency-ordered file generation manifest.
4. **`coder_node`**: Sequentially generates full file contents for greenfield builds, writing to state.
5. **`locator_node`**: Performs hybrid search (pgvector embeddings + BM25 keyword matching + import graph expansion) over `files` manifest. Returns 1 to 5 target files.
6. **`editor_node`**: Generates unified diffs strictly for the files retrieved by the Locator.
7. **`sandbox_node`**: Initializes E2B microVM, applies code or diffs, and executes `npm ci`, `tsc`, `lint`, `build`, and Playwright smoke tests.
8. **`fixer_node`**: Invoked on sandbox failure. Receives only error stack trace and failing files. Patches code (Max 3 retries).
9. **`verifier_node`**: Validates DOM render, layout overflow, and captures Playwright screenshot.
10. **`committer_node`**: Calls GitHub MCP server to commit tree to `main`, tags `vN`, and registers file manifest embeddings in PostgreSQL.

---

## 3. Pydantic Inter-Agent Contracts (`contracts/`)

To prevent agent drift and ensure backward compatibility, all communication across agent boundaries is governed by immutable Pydantic V2 schemas.

### 3.1 Requirements Contract (`contracts/requirements.py`)
```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

class ColorPalette(BaseModel):
    primary: str = Field(description="Hex color code for primary branding")
    secondary: str = Field(description="Hex color code for accents")
    background: str = Field(description="Light or dark background hex")
    text: str = Field(description="Contrasting text hex")

class NavItem(BaseModel):
    label: str
    target_section: str

class SiteFeature(BaseModel):
    name: str
    description: str
    priority: Literal["must_have", "nice_to_have"]

class RequirementsContract(BaseModel):
    project_id: str
    version_n: int
    business_name: str
    business_type: str
    locale: str = Field(default="en", description="Default display language: 'en' or 'ur'")
    palette: ColorPalette
    navigation: List[NavItem]
    features: List[SiteFeature]
    hero_headline: str
    hero_subheadline: str
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    social_links: Dict[str, str] = Field(default_factory=dict)
```

### 3.2 Plan Contract (`contracts/plan.py`)
```python
from pydantic import BaseModel, Field
from typing import List, Literal

class FileAction(BaseModel):
    path: str = Field(description="Relative path, e.g. src/components/Hero.tsx")
    role: Literal["component", "content", "page", "style", "config", "api"]
    action: Literal["create", "modify", "delete"]
    description: str = Field(description="Exact purpose of this file")
    imports: List[str] = Field(default_factory=list)
    exports: List[str] = Field(default_factory=list)

class PlanContract(BaseModel):
    project_id: str
    stack_profile: Literal["vite-react-tailwind", "static-html"]
    files: List[FileAction]
    estimated_tokens: int
```

### 3.3 Build & Verification Contract (`contracts/build_result.py`)
```python
from pydantic import BaseModel, Field
from typing import Optional, List

class BuildResultContract(BaseModel):
    success: bool
    exit_code: int
    tsc_passed: bool
    lint_passed: bool
    build_passed: bool
    playwright_passed: bool
    failing_files: List[str] = Field(default_factory=list)
    raw_error_log: Optional[str] = None
    preview_url: Optional[str] = None
    screenshot_s3_key: Optional[str] = None
```

### 3.4 File Edit Contract (`contracts/file_edit.py`)
```python
from pydantic import BaseModel, Field
from typing import List

class SingleFileDiff(BaseModel):
    path: str
    original_hash: str
    unified_diff: str
    summary_of_change: str

class FileEditContract(BaseModel):
    project_id: str
    version_n: int
    trigger_message_id: str
    diffs: List[SingleFileDiff]
```

---

## 4. Database Schema (PostgreSQL 16 + pgvector)

The relational schema is normalized, with strict foreign key constraints and transactional integrity.

```sql
-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 1. Users & RBAC
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'developer', 'admin')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Subscriptions & Quota Management
CREATE TABLE plans (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    monthly_token_quota INTEGER NOT NULL,
    max_projects INTEGER NOT NULL,
    max_edits_per_month INTEGER NOT NULL,
    price_cents INTEGER NOT NULL
);

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_id VARCHAR(50) NOT NULL REFERENCES plans(id),
    status VARCHAR(50) NOT NULL CHECK (status IN ('active', 'past_due', 'canceled')),
    current_period_start TIMESTAMPTZ NOT NULL,
    current_period_end TIMESTAMPTZ NOT NULL
);

CREATE TABLE usage_counters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    period_date DATE NOT NULL,
    tokens_consumed INTEGER NOT NULL DEFAULT 0,
    generations_count INTEGER NOT NULL DEFAULT 0,
    edits_count INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT unique_user_period UNIQUE(user_id, period_date)
);

-- 3. Core Project Tables
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    stack_profile VARCHAR(50) NOT NULL DEFAULT 'vite-react-tailwind',
    current_version INTEGER NOT NULL DEFAULT 0,
    current_req_version INTEGER NOT NULL DEFAULT 0,
    github_repo VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 4. Messaging & Auditing
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    audio_s3_key VARCHAR(500),
    kind VARCHAR(50) NOT NULL CHECK (kind IN ('chat', 'clarification', 'summary', 'build_log')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 5. Requirements Versioning
CREATE TABLE requirements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    n INTEGER NOT NULL,
    data JSONB NOT NULL,
    diff JSONB,
    trigger_message_id UUID REFERENCES messages(id),
    confirmed_at TIMESTAMPTZ,
    CONSTRAINT unique_project_req_version UNIQUE(project_id, n)
);

CREATE TABLE decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    topic VARCHAR(150) NOT NULL,
    choice TEXT NOT NULL,
    reason TEXT NOT NULL,
    source VARCHAR(50) NOT NULL CHECK (source IN ('user', 'ai_default', 'ai_inferred')),
    message_id UUID REFERENCES messages(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 6. Project Versions & Code Tracking
CREATE TABLE versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    n INTEGER NOT NULL,
    parent_n INTEGER,
    requirements_n INTEGER NOT NULL,
    trigger_message_id UUID REFERENCES messages(id),
    commit_sha VARCHAR(40) NOT NULL,
    summary TEXT NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('draft', 'verified', 'failed', 'rolled_back')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_project_version UNIQUE(project_id, n)
);

-- 7. Manifest-Based File Locator with pgvector (1536d)
CREATE TABLE files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version_id UUID NOT NULL REFERENCES versions(id) ON DELETE CASCADE,
    path VARCHAR(500) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('component', 'content', 'page', 'style', 'config', 'api')),
    summary TEXT NOT NULL,
    exports TEXT[] NOT NULL DEFAULT '{}',
    imports TEXT[] NOT NULL DEFAULT '{}',
    content_hash VARCHAR(64) NOT NULL,
    embedding vector(1536),
    CONSTRAINT unique_version_file_path UNIQUE(version_id, path)
);

-- HNSW Vector Index for Instant Semantic Similarity Search
CREATE INDEX idx_files_embedding ON files USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 8. Execution Runs & Observability
CREATE TABLE runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version_id UUID REFERENCES versions(id) ON DELETE CASCADE,
    agent VARCHAR(100) NOT NULL,
    tokens_in INTEGER NOT NULL,
    tokens_out INTEGER NOT NULL,
    cost_usd NUMERIC(10, 6) NOT NULL,
    ok BOOLEAN NOT NULL,
    trace_id VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 9. Human-in-the-Loop Marketplace & Escrow Ledger
CREATE TABLE deployment_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    version_id UUID NOT NULL REFERENCES versions(id),
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending_assignment', 'assigned', 'quoted', 'in_progress', 'live_confirmed', 'canceled')),
    assigned_developer_id UUID REFERENCES users(id),
    chat_room_id UUID DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quotes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id UUID NOT NULL REFERENCES deployment_requests(id) ON DELETE CASCADE,
    amount_cents INTEGER NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(50) NOT NULL CHECK (status IN ('submitted', 'accepted', 'rejected', 'expired')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    quote_id UUID NOT NULL REFERENCES quotes(id),
    amount_cents INTEGER NOT NULL,
    gateway_ref VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('held', 'released', 'refunded')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Double-Entry Ledger Engine
CREATE TABLE ledger_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payment_id UUID REFERENCES payments(id),
    account_type VARCHAR(50) NOT NULL CHECK (account_type IN ('user_escrow', 'platform_commission', 'developer_payable')),
    entity_id UUID NOT NULL, -- user_id, developer_id, or platform_account_id
    debit_cents INTEGER NOT NULL DEFAULT 0,
    credit_cents INTEGER NOT NULL DEFAULT 0,
    reference_memo VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payout_periods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    period_month VARCHAR(7) NOT NULL, -- e.g. '2026-11'
    status VARCHAR(50) NOT NULL CHECK (status IN ('open', 'processing', 'closed'))
);

CREATE TABLE payouts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    period_id UUID NOT NULL REFERENCES payout_periods(id),
    developer_id UUID NOT NULL REFERENCES users(id),
    total_cents INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'paid', 'failed')),
    paid_at TIMESTAMPTZ
);
```

---

## 5. File Locator & Semantic Manifest Design

Traditional Code RAG breaks source files into 500-token chunks. This destroys JSX AST structure, confuses natural language intents, and explodes vector database indexing costs.

Our architecture implements **File-Level Semantic Manifest Routing**:

```
Prompt: "Make the Buy Now button gold and rename it to Reserve Spot"
                               │
                               ▼
 1. Signal A: pgvector Cosine Search on `path + summary + exports`
    Hits: components/ProductCard.tsx (0.84), components/Hero.tsx (0.78)
 2. Signal B: Keyword Token Matcher ('button', 'reserve', 'gold')
    Hits: data/site.json (0.91), tailwind.config.js (0.81)
 3. Signal C: Import Graph Traversal
    ProductCard imports data/site.json and Button.tsx
                               │
                               ▼
  Locator Decision Rule (Conventional Routing):
  - Label / Copy change  ──► Routed to data/site.json
  - Visual Styling / CSS ──► Routed to components/ProductCard.tsx
  - Final Shortlist: ['data/site.json', 'components/ProductCard.tsx'] (2 files loaded ONLY)
```

### pgvector Query Implementation
```sql
SELECT 
    path, 
    role, 
    summary, 
    exports,
    1 - (embedding <=> :query_embedding) AS similarity
FROM files
WHERE version_id = :current_version_id
ORDER BY similarity DESC
LIMIT 5;
```

---

## 6. Sandbox MicroVM Execution Protocol

Builds are executed inside isolated microVMs via **E2B** (or local Docker container fallback during offline development).

```
Host (FastAPI) ─── API Token ───► E2B MicroVM (Ubuntu 24.04 LTS)
                                  ├── Hardware: 2 vCPU, 2048 MB RAM
                                  ├── Timeout: 300 seconds
                                  ├── Pre-cached: /root/.npm & base node_modules
                                  └── Execution:
                                      1. Write files from state payload
                                      2. npm ci --offline || npm ci
                                      3. npx tsc --noEmit
                                      4. npm run lint
                                      5. npm run build
                                      6. npx playwright test smoke.spec.ts
```

### Sandbox Security Invariants:
1. **Zero Secrets in Sandbox:** The microVM environment does NOT contain AWS, GitHub, or Database credentials.
2. **Ephemeral Lifecycles:** Each sandbox is instantiated per build and destroyed immediately after Playwright verification completes.
3. **Egress Firewall:** All outbound ports blocked except HTTPS (443) to `registry.npmjs.org` and font CDNs.

---

## 7. Model Strategy & Token Budgeting

| Component | Target Model Tier | Temperature | Prompt Caching | Token Budget |
|---|---|---|---|---|
| **Audio ASR** | Whisper Large-v3-Turbo | 0.0 | N/A | N/A (Audio) |
| **Router** | Claude 3.5 Haiku | 0.1 | Enabled | 1,000 tokens |
| **Clarifier** | Claude 3.5 Haiku | 0.4 | Enabled | 2,500 tokens |
| **Planner** | Claude 3.5 Sonnet | 0.2 | Enabled | 8,000 tokens |
| **Coder (per file)** | Claude 3.5 Sonnet | 0.2 | Enabled | 4,000 tokens |
| **Locator** | Python Rules + Haiku | 0.0 | Enabled | 1,500 tokens |
| **Editor** | Claude 3.5 Sonnet | 0.1 | Enabled | 4,000 tokens |
| **Fixer** | Claude 3.5 Sonnet | 0.1 | Enabled | 6,000 tokens |
| **Verifier (Vision)** | Claude 3.5 Sonnet | 0.0 | Disabled | 2,000 tokens |

**Global Ceiling:** Hard limit of 300,000 tokens per workflow run. If accumulated tokens cross 250,000, LangGraph throws `BudgetExceededException` and quarantines the state.

---

## 8. Double-Entry Accounting Invariant

The marketplace operates on double-entry bookkeeping. For every transaction $T$:
$$\sum \text{Debits} = \sum \text{Credits}$$

### Scenario: Client pays \$30.00 quote for live deployment.
```
Transaction 1: Escrow Inflow (Client Payment)
  DEBIT:  user_escrow ($30.00)
  CREDIT: escrow_holding ($30.00)

Transaction 2: Completion & Settlement (80/20 Commission)
  DEBIT:  escrow_holding ($30.00)
  CREDIT: platform_commission ($6.00)
  CREDIT: developer_payable ($24.00)

Validation Check:
  Total Debits = $60.00 | Total Credits = $60.00 | Difference = $0.00 (BALANCED)
```
