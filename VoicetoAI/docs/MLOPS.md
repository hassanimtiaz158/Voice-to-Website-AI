# MLOps Strategy & AI Lifecycle Engineering
## Prompt Versioning, Evaluation Harnesses, Model Serving & Drift Detection

---

### Document Metadata
- **Document Version:** 2.0.0
- **Status:** APPROVED & LOCKED
- **Standard:** Production LLM engineering, continuous prompt regression testing, and empirical evaluation.

---

## 1. MLOps Architecture Overview

Unlike traditional ML pipelines that focus on model weight training, an Enterprise Agentic LLM Platform focuses on **Prompt Engineering Versioning**, **Deterministic Agent Evaluation**, **Token Cost Attribution**, and **Inference Drift Detection**.

```
  ┌───────────────────────────────────────────────────────────────┐
  │ 1. Git-Versioned Prompts & DVC Audio Datasets                 │
  │    (backend/app/prompts/*.vN.txt & evals/audio_clips/)        │
  └──────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
  ┌───────────────────────────────────────────────────────────────┐
  │ 2. Automated Benchmark Evaluation Gates (CI / Pre-Release)     │
  │    • ASR WER Benchmark (30 bilingual Urdu/English clips)      │
  │    • Clarifier Efficiency Benchmark (20 synthetic personas)   │
  │    • Greenfield Build Benchmark (30 end-to-end scenarios)     │
  │    • Surgical Locator Benchmark (30 precision edit tasks)     │
  └──────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
  ┌───────────────────────────────────────────────────────────────┐
  │ 3. Runtime Telemetry & Cost Attribution (Langfuse + Postgres) │
  │    • Trace ID propagation across all LangGraph nodes          │
  │    • Input/Output token tracking & dollar cost calculation    │
  │    • Token ceiling alerting (threshold: 250k tokens)          │
  └──────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
  ┌───────────────────────────────────────────────────────────────┐
  │ 4. Drift & Anomaly Detection (Prometheus + Grafana)           │
  │    • P95 Latency drift, First-pass compilation drop alerts    │
  └───────────────────────────────────────────────────────────────┘
```

---

## 2. Prompt Management & Version Control

All system and user prompt templates are treated as immutable software artifacts version-controlled in the repository:

### 2.1 Prompt Registry Directory Layout
```
backend/app/prompts/
├── router/
│   ├── v1.txt                         # Initial keyword-assisted prompt
│   └── v2.txt                         # Few-shot tri-modal classifier (Active)
├── clarifier/
│   ├── v1.txt                         # Freeform interview prompt
│   └── v2.txt                         # 3-turn option generator with "You Decide" (Active)
├── planner/
│   └── v1.txt                         # Pinned vite-react-tailwind architect (Active)
├── coder/
│   ├── v1.txt                         # Whole-project generator (Deprecated)
│   └── v2.txt                         # Sequential single-file generator (Active)
└── fixer/
    └── v1.txt                         # Targeted stderr patch engineer (Active)
```

### 2.2 Prompt Regression Testing in CI
Before any prompt version bump is merged, CI executes the corresponding benchmark suite to ensure accuracy has not regressed:
- Router: Must achieve $\ge 96\%$ accuracy on 50 reference intent prompts.
- Clarifier: Must complete within $\le 3$ turns across all 20 benchmark personas.
- Coder: Must compile without syntax errors on 15 reference plans.

---

## 3. Dataset Versioning & Test Corpora

The evaluation datasets in `evals/` are versioned and stored using Git LFS / DVC:

1. **Bilingual ASR Audio Dataset (`evals/audio_clips/`):**
   - 30 uncompressed 16kHz WAV audio recordings.
   - Distribution: 15 Conversational Urdu, 10 Pakistani English, 5 Mixed "Urdish" code-switching.
   - Paired with human-transcribed ground-truth transcripts in `transcripts.json`.
2. **Shop Owner Persona Dataset (`evals/personas/`):**
   - 20 realistic retail business personas representing Pakistani and global commerce (e.g., pharmacy, custom shoe maker, biryani caterer, electronics repair shop).
3. **Greenfield Generation Benchmark (`evals/build_scenarios/`):**
   - 30 complete requirement sets testing diverse visual layouts (e.g., hero video, sticky headers, multi-tier pricing, product grid).
4. **Surgical Edit Benchmark (`evals/edit_tasks/`):**
   - 30 distinct change requests (text tweaks, color swaps, button additions) with ground-truth target file expectations.

---

## 4. Model Tiering & Cost Attribution Engine

To maintain an average greenfield creation cost below $\$2.50$, the system enforces a strict **Model Tiering Strategy**:

```python
MODEL_TIERING = {
    "router": {
        "model": "claude-3-5-haiku-20241022",
        "temperature": 0.1,
        "prompt_caching": True,
        "max_tokens": 1000
    },
    "clarifier": {
        "model": "claude-3-5-haiku-20241022",
        "temperature": 0.4,
        "prompt_caching": True,
        "max_tokens": 2500
    },
    "planner": {
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.2,
        "prompt_caching": True,
        "max_tokens": 4096
    },
    "coder": {
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.2,
        "prompt_caching": True,
        "max_tokens": 4096
    },
    "editor": {
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.1,
        "prompt_caching": True,
        "max_tokens": 4000
    },
    "fixer": {
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.1,
        "prompt_caching": True,
        "max_tokens": 4096
    }
}
```

### Prompt Caching Savings:
Anthropic Prompt Caching (`cache_control: {"type": "ephemeral"}`) is applied to system prompts, scaffold file layouts, and `data/site.json` contexts. This reduces input token costs by **up to 90%** on multi-turn clarification and multi-file code generation steps.

---

## 5. Drift Detection & Quality Alerts

Prometheus and Langfuse telemetry monitor for three critical operational failure modes:
1. **Compilation Pass Rate Drift:** If first-pass compilation falls below $70\%$ over a trailing 24-hour window, alert Platform Ops to inspect Coder prompt stability.
2. **Token Inflation Drift:** If average tokens per greenfield build cross $180,000$ tokens, alert to inspect Planner context bloat.
3. **Fixer Escalation Rate:** If the percentage of builds requiring $\ge 3$ fix attempts exceeds $15\%$, freeze deployments until investigated.
