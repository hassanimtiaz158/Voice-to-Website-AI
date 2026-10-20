# Architecture Plan (C4 Model & Sequence Specifications)
## Voice-to-Website AI: Enterprise Autonomous Web Generation & Human Deployment Platform

---

### Document Metadata
- **Document Version:** 2.0.0
- **Status:** APPROVED & LOCKED
- **Author:** Principal AI Architect & Staff Systems Architect
- **Related Documents:** [PRD](file:///d:/VoicetoAI/docs/PRD.md), [TDD](file:///d:/VoicetoAI/docs/TDD.md), [Implementation Roadmap](file:///d:/VoicetoAI/docs/IMPLEMENTATION_ROADMAP.md)

---

## 1. C4 Architecture Model

### 1.1 Level 1: System Context Diagram
The System Context diagram illustrates the boundaries of the Voice-to-Website AI system and how users and external systems interact with it.

```mermaid
C4Context
    title System Context Diagram - Voice-to-Website AI Platform

    Person(shopOwner, "Shop Owner / Client", "Non-technical merchant describing their website via spoken voice or text.")
    Person(freelancer, "Freelance Developer", "Verified deployment engineer setting up domains, DNS, and hosting.")
    Person(admin, "Platform Admin", "Monitors token costs, platform ledger, quotas, and worker payouts.")

    System(voiceToWebsite, "Voice-to-Website AI Platform", "Autonomous multi-agent web generation platform with sandboxed verification and human deployment marketplace.")

    System_Ext(githubMCP, "GitHub Cloud / MCP", "Stores project codebases in private repositories, versions via Git tags, and manages branches.")
    System_Ext(e2bSandbox, "E2B Sandbox Cloud", "Executes untrusted generated code, runs TypeScript compilation, linting, build, and Playwright tests.")
    System_Ext(awsS3, "AWS S3 / Cloudflare R2", "Stores voice audio recordings, Playwright screenshot artifacts, and build zip bundles.")
    System_Ext(langfuse, "Langfuse Observability", "Captures end-to-end LLM traces, prompt tokens, completion tokens, costs, and latency.")
    System_Ext(anthropicOpenAI, "LLM Providers (Anthropic / OpenAI)", "Powers Haiku/Sonnet reasoning, code generation, diff synthesis, and Whisper ASR.")

    Rel(shopOwner, voiceToWebsite, "Speaks prompts, confirms transcripts, reviews live previews", "HTTPS / WebSocket")
    Rel(freelancer, voiceToWebsite, "Reviews deployment requests, submits quotes, chats with client", "HTTPS / WebSocket")
    Rel(admin, voiceToWebsite, "Audits margins, settles payouts, monitors agent health", "HTTPS")

    Rel(voiceToWebsite, githubMCP, "Pushes verified trees, tags versions, fetches specific files", "JSON-RPC / REST")
    Rel(voiceToWebsite, e2bSandbox, "Deploys code into microVMs, runs build pipeline & Playwright", "gRPC / HTTPS")
    Rel(voiceToWebsite, awsS3, "Uploads raw audio blobs, downloads verification screenshots", "S3 API")
    Rel(voiceToWebsite, langfuse, "Emits traces, latencies, token consumption, and evals", "OpenTelemetry / HTTPS")
    Rel(voiceToWebsite, anthropicOpenAI, "Calls Whisper ASR, Haiku router, and Sonnet agents", "HTTPS REST")
```

---

### 1.2 Level 2: Container Diagram
The Container diagram illustrates the high-level technical building blocks of the platform.

```mermaid
C4Container
    title Container Diagram - Voice-to-Website AI

    Container(frontendApp, "Web & Mobile Client", "Next.js 15, React 19, Tailwind CSS, Web Audio API", "Delivers voice recorder, interactive streaming chat, requirements modal, live preview iframe, and marketplace portal.")
    Container(apiGateway, "API Gateway / Backend", "FastAPI, Python 3.12, Uvicorn, AsyncIO", "Exposes REST endpoints, manages WebSocket streaming, enforces JWT auth and user quota rate limiting.")
    Container(agentOrchestrator, "Agent Orchestration Engine", "LangGraph, Pydantic V2, Postgres Checkpointer", "Manages deterministic state graph, human interrupts, agentic transitions, and self-healing cycles.")
    Container(asrService, "Whisper Speech Ingestion Service", "Faster-Whisper / OpenAI Whisper API, Librosa, WebRTC VAD", "Handles audio validation, noise reduction, voice activity detection, and bilingual transcription.")
    ContainerDb(relationalDb, "Primary Relational DB", "PostgreSQL 16 + pgvector extension", "Persists projects, users, versions, requirements, file manifests, 1536d embeddings, and double-entry ledger.")
    ContainerDb(objectStore, "Object Storage", "AWS S3 / MinIO", "Stores raw voice audio files, Playwright visual screenshots, and site zip backups.")
    Container(sandboxEngine, "Sandbox Runner", "E2B microVM SDK / Docker", "Ephemeral microVM sandbox executing npm ci, tsc, lint, build, and headless browser tests.")
    Container(mcpClient, "GitHub MCP Client", "Official GitHub MCP Server", "Executes deterministic Git operations, tags, branches, and repo creations.")

    Rel(frontendApp, apiGateway, "Interacts via REST & WebSockets", "HTTPS / WSS")
    Rel(apiGateway, agentOrchestrator, "Dispatches execution jobs", "In-Process / Background Tasks")
    Rel(apiGateway, asrService, "Forwards audio buffer for transcription", "Async gRPC / Internal REST")
    Rel(agentOrchestrator, relationalDb, "Reads/writes state checkpoints & manifests", "asyncpg / SQLAlchemy")
    Rel(agentOrchestrator, sandboxEngine, "Transfers code & executes verification", "E2B Client API")
    Rel(agentOrchestrator, mcpClient, "Commits verified code to GitHub", "MCP Protocol (stdio/SSE)")
    Rel(asrService, objectStore, "Persists raw audio clips", "boto3 S3 API")
```

---

### 1.3 Level 3: Component Diagram (Agentic Subsystem)
The Component diagram drills into the internal architecture of the LangGraph Orchestrator container.

```mermaid
C4Component
    title Component Diagram - LangGraph Orchestration & Agent Subsystem

    Component(routerComp, "Router Node", "Claude 3.5 Haiku", "Tri-modal request classifier: QUESTION, SMALL_EDIT, or NEW_OR_MAJOR.")
    Component(clarifierComp, "Clarifier Node", "Claude 3.5 Haiku", "Generates diagnostic questions (max 3 turns), stores decisions, and produces requirements summary.")
    Component(plannerComp, "Planner Node", "Claude 3.5 Sonnet", "Transforms requirements contract into stack-aware file plan with component hierarchy.")
    Component(coderComp, "Coder Node", "Claude 3.5 Sonnet", "Generates complete files one at a time adhering strictly to conventions.")
    Component(locatorComp, "Locator Node", "pgvector + BM25 + AST", "Performs 3-signal manifest retrieval returning 1 to 5 target files for edits.")
    Component(editorComp, "Editor Node", "Claude 3.5 Sonnet", "Generates unified surgical diffs for targeted files only.")
    Component(sandboxComp, "Sandbox Runner Node", "E2B SDK / Python", "Orchestrates microVM execution: npm ci, tsc, lint, build, Playwright.")
    Component(fixerComp, "Fixer Node", "Claude 3.5 Sonnet", "Self-healing agent receiving failing files and compiler stderr (max 3 tries).")
    Component(verifierComp, "Verifier Node", "Playwright + Vision Judge", "Executes DOM integrity checks, detects UI layout overflows, captures screenshot.")
    Component(committerComp, "Committer Node", "GitHub MCP Client", "Commits clean tree to main, tags vN, writes manifest embeddings to Postgres.")

    Rel(routerComp, clarifierComp, "Routes NEW_OR_MAJOR requests")
    Rel(routerComp, locatorComp, "Routes SMALL_EDIT requests")
    Rel(clarifierComp, plannerComp, "Passes confirmed RequirementsContract")
    Rel(plannerComp, coderComp, "Passes PlanContract with file list")
    Rel(coderComp, sandboxComp, "Dispatches generated code bundle")
    Rel(locatorComp, editorComp, "Passes target files & original content")
    Rel(editorComp, sandboxComp, "Applies diffs to base repo")
    Rel(sandboxComp, fixerComp, "Build failure triggers self-healing")
    Rel(fixerComp, sandboxComp, "Re-runs sandbox verification")
    Rel(sandboxComp, verifierComp, "Build success triggers verification")
    Rel(verifierComp, committerComp, "Verification pass triggers commit & tag")
```

---

## 2. Comprehensive Sequence Diagrams

### 2.1 Greenfield Project Generation Flow
```mermaid
sequenceDiagram
    autonumber
    actor User as Shop Owner
    participant UI as Next.js Web App
    participant ASR as Whisper ASR
    participant LG as LangGraph Engine
    participant DB as Postgres + pgvector
    participant E2B as E2B MicroVM Sandbox
    participant MCP as GitHub MCP
    participant S3 as S3 Bucket

    User->>UI: Speaks voice prompt (Urdu/English)
    UI->>ASR: Streams audio buffer
    ASR-->>UI: Returns raw transcript
    UI-->>User: Displays transcript confirmation dialog
    User->>UI: Clicks "Confirm Transcript"
    UI->>LG: Initiates state graph execution
    LG->>DB: Validates subscription quota and daily token counters
    LG->>LG: Router classifies as NEW_OR_MAJOR
    
    loop Clarification (Max 3 Turns)
        LG->>UI: Emits 3-5 option questions (with "You Decide")
        User->>UI: Selects options or leaves default
        UI->>LG: Submits answers via LangGraph interrupt resumption
        LG->>DB: Writes decisions rows
    end

    LG->>UI: Presents structured Requirements Summary
    User->>UI: Clicks "Approve & Generate"
    LG->>DB: Commits confirmed Requirements row (v1)
    LG->>LG: Planner builds PlanContract for `vite-react-tailwind`
    
    loop File-by-File Generation
        LG->>LG: Coder generates single file JSON
    end

    LG->>E2B: Provisions microVM with pre-cached node_modules
    LG->>E2B: Injects generated files
    E2B->>E2B: Runs: npm ci -> tsc -> lint -> build -> vite preview
    
    alt Build Failure
        E2B-->>LG: Emits compiler stderr
        LG->>LG: Fixer patches failing files (up to 3 attempts)
        LG->>E2B: Re-executes build
    end

    E2B->>E2B: Executes Playwright smoke test & captures screenshot
    E2B->>S3: Uploads screenshot artifact
    LG->>MCP: Creates GitHub repo, pushes tree to main, tags `v1`
    LG->>DB: Inserts versions row + registers file manifest & embeddings
    LG->>UI: Returns live preview URL & celebration state
```

### 2.2 Surgical Edit & Manifest Retrieval Flow
```mermaid
sequenceDiagram
    autonumber
    actor User as Shop Owner
    participant UI as Next.js Web App
    participant LG as LangGraph Engine
    participant DB as Postgres (pgvector)
    participant MCP as GitHub MCP
    participant E2B as E2B Sandbox

    User->>UI: "Change hero headline to Summer Clearance Sale"
    UI->>LG: Sends edit message
    LG->>LG: Router classifies as SMALL_EDIT
    LG->>DB: Runs hybrid search on file manifest (Embedding + Keyword + Graph)
    DB-->>LG: Shortlists `data/site.json` and `src/components/Hero.tsx`
    LG->>LG: Rule Engine: Text change strictly routes to `data/site.json`
    LG->>MCP: Fetches `data/site.json` content from Git HEAD
    LG->>LG: Editor generates unified diff
    LG->>E2B: Clones repo from main, applies diff
    E2B->>E2B: Runs tsc, lint, build, Playwright
    E2B-->>LG: All tests exit code 0
    LG->>MCP: Commits diff to main, creates Git tag `v2`
    LG->>DB: Inserts versions row (v2), copies unchanged files, updates hash
    LG->>UI: Refreshes preview iframe seamlessly
```

---

## 3. Threat Model & Security Boundaries (STRIDE Analysis)

| Threat Category | Potential Attack Vector | Architectural Mitigation |
|---|---|---|
| **Spoofing** | Attacker impersonating platform admin or developer in marketplace. | Strict JWT authentication with cryptographically signed role claims; database-backed token invalidation. |
| **Tampering** | Malicious prompt attempting to alter git history or inject backdoors into generated code. | Isolated Committer node using GitHub MCP with scoped tokens; sandbox executes with zero network egress to internal infrastructure. |
| **Repudiation** | Client claiming they never approved requirements or developer disputing payout. | Immutable database audit trail: `decisions` table links user message IDs; double-entry `ledger_entries` cannot be updated or deleted. |
| **Information Disclosure** | LLM-generated code leaking platform environment variables or API keys. | Sandbox microVM runs in complete isolation with zero access to host environment variables or master API keys. |
| **Denial of Service** | Infinite Fixer loop or user submitting massive prompts to exhaust token limits. | Strict per-run ceiling of 300,000 tokens; global timeout of 300s in E2B; rate limiting at FastAPI gateway. |
| **Elevation of Privilege** | Code execution sandbox escape attempting to break out of Docker / microVM. | E2B hypervisor-level isolation (Firecracker microVM); local Docker fallback runs as unprivileged user with read-only root filesystem. |
