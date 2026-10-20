# Feature Specification: Observability, Logging & Evaluation Framework
## Langfuse Tracing, Prometheus Telemetry, Structured Logging & Automated Evals

---

### Feature Metadata
- **Feature ID:** SPEC-007-MONITORING-EVAL
- **Feature Owner:** Member 4 (Delivery/Observability) & Member 2 (Build Evals)
- **Status:** APPROVED & LOCKED
- **Target Release:** Milestone M1 (Tracing Foundation) & Milestone M5 (Final Eval Harness)

---

## 1. Observability Architecture

The platform implements unified enterprise observability spanning three pillars: **Traces** (LLM operations), **Metrics** (system & sandbox performance), and **Logs** (application events).

```
┌────────────────────────────────────────────────────────────────────────┐
│                        OBSERVABILITY ARCHITECTURE                      │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Traces (Langfuse Cloud / Self-Hosted)                               │
│    • Tracks 100% of LLM calls across Router, Clarifier, Planner,       │
│      Coder, Locator, Editor, Fixer, and Verifier.                     │
│    • Ingests exact input prompts, completions, latency, and costs.     │
├────────────────────────────────────────────────────────────────────────┤
│ 2. Metrics (Prometheus + Grafana Dashboard)                            │
│    • HTTP request rate, error rate (4xx/5xx), P50/P95/P99 latency.     │
│    • E2B MicroVM build durations and memory utilization.               │
│    • Real-time WebSocket connection count and queue depths.            │
├────────────────────────────────────────────────────────────────────────┤
│ 3. Structured Logging (Loguru / Python structlog -> Loki / ELK)        │
│    • JSON-formatted logs with correlation IDs: trace_id, project_id,   │
│      user_id, and version_n.                                           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Langfuse LLM Tracing & Cost Attribution

Every LangGraph agent execution wraps its model client with the Langfuse Python SDK. Traces are automatically correlated with the platform's `runs` relational table:

```python
from langfuse import Langfuse
from langfuse.openai import openai

langfuse = Langfuse()

def execute_agent_with_trace(project_id: str, version_n: int, agent_name: str, prompt: str):
    trace = langfuse.trace(
        name=f"Agent:{agent_name}",
        metadata={"project_id": project_id, "version_n": version_n},
        tags=[agent_name, "production"]
    )
    
    generation = trace.generation(
        name=agent_name,
        model="claude-3-5-sonnet-20241022",
        model_parameters={"temperature": 0.2, "max_tokens": 4096},
        input=prompt
    )
    
    response = call_llm(prompt)
    
    generation.end(
        output=response.content,
        usage={
            "prompt_tokens": response.usage.input_tokens,
            "completion_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.total_tokens
        }
    )
    return response.content
```

---

## 3. Automated Evaluation Harness & Benchmarks

The project establishes a rigorous, quantitative evaluation harness to validate the AI system across four core benchmarks:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      AUTOMATED EVALUATION BENCHMARKS                   │
├────────────────────────────────────────────────────────────────────────┤
│ Benchmark 1: Speech-to-Text (ASR) Benchmark                            │
│ • Dataset: 30 recorded audio clips (15 Urdu, 10 English, 5 Mixed).     │
│ • Metric: Word Error Rate (WER) < 14% on Pakistani English/Urdu.       │
├────────────────────────────────────────────────────────────────────────┤
│ Benchmark 2: Clarification Efficiency Benchmark                        │
│ • Dataset: 20 synthetic shop owner personas with incomplete prompts.   │
│ • Metric: 100% reach confirmed requirements in <= 3 turns.             │
├────────────────────────────────────────────────────────────────────────┤
│ Benchmark 3: Greenfield Code Build Benchmark                           │
│ • Dataset: 30 end-to-end website generation scenarios across retail.   │
│ • Metric: >= 85% build and pass Playwright smoke tests within <= 3 fix │
│   retries (stretch: 95%).                                              │
├────────────────────────────────────────────────────────────────────────┤
│ Benchmark 4: Surgical Edit Accuracy Benchmark                          │
│ • Dataset: 30 modification tasks (copy, styling, layout, components).  │
│ • Metric: >= 90% accuracy in Locator isolating exact files; zero       │
│   regressions in untouched components.                                 │
└────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Evaluating ASR Word Error Rate (WER)
```python
import jiwer

def evaluate_asr_benchmark(test_clips):
    ground_truths = [clip["reference_text"] for clip in test_clips]
    hypotheses = [transcribe_audio(clip["audio_path"]) for clip in test_clips]
    
    wer = jiwer.wer(ground_truths, hypotheses)
    mer = jiwer.mer(ground_truths, hypotheses)
    print(f"Bilingual Whisper ASR Evaluation: WER={wer:.2%}, MER={mer:.2%}")
    assert wer <= 0.14, f"ASR WER {wer} exceeds target threshold of 14%"
```

### 3.2 Greenfield Build Eval Harness (`evals/build_benchmark.py`)
Executes the full pipeline headlessly across 30 distinct commercial domains (e.g., pharmacy, bakery, clothier, real estate, repair shop):
- Measures first-pass compilation rate.
- Measures Fixer recovery success rate on attempts 1, 2, and 3.
- Computes average token consumption and monetary cost per site.

---

## 4. Structured JSON Logging Schema

All server logs adhere to standard JSON format:
```json
{
  "timestamp": "2026-10-18T17:42:01.124Z",
  "level": "INFO",
  "logger": "voicetoai.agents.coder",
  "trace_id": "trc_9a8b7c6d5e",
  "project_id": "proj_12345678",
  "user_id": "usr_87654321",
  "version_n": 1,
  "message": "Coder successfully generated src/components/Hero.tsx",
  "tokens_consumed": 1842,
  "duration_ms": 1420
}
```

---

## 5. Acceptance Criteria

1. **Trace Coverage:** 100% of LLM calls in staging and production emit complete spans to Langfuse.
2. **Cost Alerting:** Any single project generation run exceeding $\$3.00$ or 250,000 tokens immediately raises an alert to Platform Ops.
3. **Eval Execution:** The complete benchmark suite (30 build scenarios, 30 edit tasks, 30 audio clips) executes via a single CLI command: `pytest evals/` and produces an HTML report.
