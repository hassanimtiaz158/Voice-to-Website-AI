# Phase 18: Observability, Langfuse Tracing & Full Benchmark Evaluation Suite

---

### Navigation
- **Current Phase:** Phase 18 of 20
- **Previous Phase:** [Phase 17: Human-in-the-Loop Marketplace & Double-Entry Ledger Engine](file:///d:/VoicetoAI/docs/PHASES/PHASE_17_Marketplace_and_Escrow_Ledger.md)
- **Next Phase:** [Phase 19: Containerization, Reverse Proxy, SSL & Production CI/CD Pipeline](file:///d:/VoicetoAI/docs/PHASES/PHASE_19_Docker_Traefik_SSL_and_CICD.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [Monitoring_Logging_Evaluation.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Monitoring_Logging_Evaluation.md), [MLOPS.md](file:///d:/VoicetoAI/docs/MLOPS.md)

---

### Objective
Deploy enterprise telemetry with Langfuse tracing, Prometheus metrics, structured JSON logging, and the complete quantitative FYP evaluation benchmark suite.

### Business Goal
Ensure complete cost transparency, provide academic reviewers with empirical performance proof, and detect model latency drift proactively.

### Technical Goal
Wrap all agent invocations with Langfuse SDK, export Prometheus metrics, and automate the 4 benchmark evaluation suites (ASR, Clarifier, Coder, Locator).

### Features Included
- Langfuse tracing on 100% of LLM calls with token, latency, and cost attribution.
- Prometheus metrics endpoint `/metrics` (request rates, latency histograms, error counts).
- Structured JSON logging with correlation IDs (`trace_id`, `project_id`, `version_n`).
- Automated FYP evaluation runner script in `evals/run_all_benchmarks.py`.

### Features NOT Included
- Production cloud deployment (Phase 19).

### Dependencies
- All previous phases (Phases 1 to 17).

### Deliverables
- `backend/app/observability/langfuse.py`.
- `backend/app/observability/metrics.py`.
- `evals/run_all_benchmarks.py` producing markdown evaluation report.

### Architecture Changes
- Telemetry middleware wraps FastAPI application and LangGraph nodes.

### Database Changes
- None (populates existing `runs` table).

### API Changes
- `GET /metrics`: Prometheus scrape endpoint.

### Frontend Changes
- None.

### Backend Changes
- Loguru structured JSON log configuration.

### ML Changes
- None.

### Infrastructure Changes
- Prometheus and Grafana containers added to Docker Compose.

### Configuration Required
- Langfuse public/secret keys and host URL.

### Environment Variables
- `LANGFUSE_PUBLIC_KEY=pk-lf-...`
- `LANGFUSE_SECRET_KEY=sk-lf-...`
- `LANGFUSE_HOST=https://cloud.langfuse.com`

### Third-party Services
- Langfuse Cloud (or self-hosted).

### Tasks
- [x] Task 18.1: Integrate Langfuse client with LangGraph node decorator.
- [x] Task 18.2: Implement Prometheus metrics collector in FastAPI.
- [x] Task 18.3: Configure structured JSON logger with correlation IDs.
- [x] Task 18.4: Build automated evaluation runner executing all 4 benchmarks.
- [x] Task 18.5: Generate baseline evaluation report.

### Subtasks
- Subtask 18.4.1: Run 30 ASR audio clips and calculate WER.
- Subtask 18.4.2: Run 20 Clarifier personas and measure turns to ready.
- Subtask 18.4.3: Run 30 Greenfield build scenarios and measure pass rate.
- Subtask 18.4.4: Run 30 Surgical edit tasks and measure accuracy.

### Acceptance Criteria
- 100% of LLM completions log input/output tokens, latency, and cost to Langfuse.
- Automated evaluation runner executes cleanly via single command: `poetry run python -m evals.run_all_benchmarks`.
- All acceptance criteria targets met: ASR WER $\le 14\%$, Clarifier turns $\le 3$, Build success $\ge 85\%$, Edit accuracy $\ge 90\%$.

### Definition of Done
- Evaluation report generated and committed to `docs/EVALUATION_REPORT.md`; PR merged.

### Unit Tests
- `test_langfuse_metadata_formatting()`
- `test_prometheus_metrics_export()`

### Integration Tests
- `test_trace_emission_during_graph_run()`

### End-to-End Tests
- Execution of full benchmark suite in CI test environment.

### Manual Testing Checklist
- [ ] Open Langfuse dashboard.
- [ ] Run a test generation; verify trace tree displays Router $\to$ Clarifier $\to$ Planner $\to$ Coder.
- [ ] Verify token count matches database `runs` table.
- [ ] Scrape `/metrics`; verify Prometheus metrics increment.

### Regression Tests
- Re-run all existing test suites.

### Rollback Strategy
- Toggle `LANGFUSE_ENABLED=false` to silence telemetry if network latency occurs.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 4 days.

### Risks
- Network timeouts to Langfuse blocking core user generation workflows.
- *Mitigation:* Langfuse spans dispatched asynchronously in non-blocking background threads.

### Future Improvements
- Automated prompt regression alerts triggered when benchmark scores drop $>5\%$.
