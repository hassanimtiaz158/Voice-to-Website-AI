# Phase 6: Pinned Scaffolds & E2B / Docker Sandbox Runner Engine

---

### Navigation
- **Current Phase:** Phase 6 of 20
- **Previous Phase:** [Phase 5: Voice Activity Detection (VAD) & Real-time Audio Ingestion Stream](file:///d:/VoicetoAI/docs/PHASES/PHASE_05_VAD_and_Audio_Streaming.md)
- **Next Phase:** [Phase 7: LangGraph State Machine Skeleton & Postgres Checkpointer](file:///d:/VoicetoAI/docs/PHASES/PHASE_07_LangGraph_and_Checkpointer.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [Sandboxing_Execution.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Sandboxing_Execution.md), [DEVOPS.md](file:///d:/VoicetoAI/docs/DEVOPS.md)

---

### Objective
Build the hardened sandbox execution engine using E2B microVMs (and local Docker fallback) with pre-cached dependencies for the pinned `vite-react-tailwind` stack.

### Business Goal
Ensure untrusted code execution happens in absolute isolation with zero danger to platform servers, while achieving $<15\text{s}$ build speeds.

### Technical Goal
Implement the 5-stage verification pipeline (`npm ci`, `tsc`, `lint`, `build`, `preview`) with resource quotas (2 vCPU, 2GB RAM, 300s timeout) and strict egress filtering.

### Features Included
- Base template scaffold in `scaffolds/vite-react-tailwind/`.
- Pre-cached `node_modules` image configuration.
- `backend/app/sandbox/runner.py` with E2B and local Docker implementations.
- 5-stage build execution pipeline returning structured `BuildResultContract`.

### Features NOT Included
- LLM code generation, automated fixing, GitHub commits.

### Dependencies
- Phase 1 (Contracts).

### Deliverables
- Hardened base image Dockerfile for sandbox runner.
- Pinned `vite-react-tailwind` scaffold with TypeScript strict mode enabled.
- Fully tested sandbox runner module in `backend/app/sandbox/`.

### Architecture Changes
- Integration of external compute isolation provider (E2B Cloud API / Docker daemon).

### Database Changes
- None.

### API Changes
- Internal execution interface: `await sandbox_runner.execute_build(files: Dict[str, str]) -> BuildResultContract`.

### Frontend Changes
- None.

### Backend Changes
- Sandbox lifecycle management (instantiate microVM $\to$ write files $\to$ run commands $\to$ teardown).

### ML Changes
- None.

### Infrastructure Changes
- E2B API integration or local Docker socket binding.

### Configuration Required
- Hardware resource limits: 2 vCPU, 2048 MB RAM, 300s execution deadline.

### Environment Variables
- `SANDBOX_PROVIDER=e2b` (or `docker`)
- `E2B_API_KEY=e2b_...`

### Third-party Services
- E2B Cloud MicroVM Sandbox.

### Tasks
- [x] Task 6.1: Author clean `vite-react-tailwind` scaffold with zero build errors.
- [x] Task 6.2: Build base sandbox template with pre-installed npm cache.
- [x] Task 6.3: Implement `E2BSandboxRunner` with timeout and memory monitoring.
- [x] Task 6.4: Implement fallback `DockerSandboxRunner` for local offline testing.
- [x] Task 6.5: Implement structured stderr/stdout parser.

### Subtasks
- Subtask 6.3.1: Configure outbound egress rules blocking all IPs except npm registry.
- Subtask 6.5.1: Write TypeScript compiler regex error parser (`TS\d{4}`).

### Acceptance Criteria
- Injecting clean scaffold files into sandbox completes full build pipeline in $<15\text{ seconds}$ with exit code 0.
- Injecting a file with a deliberate syntax error exits with code 1 and populates `BuildResultContract.raw_error_log`.
- Sandbox cannot access host network or host filesystem.

### Definition of Done
- Sandbox runner passes both clean and deliberate error test suites; CI runs Docker runner cleanly.

### Unit Tests
- `test_error_log_regex_parser()`
- `test_build_result_contract_mapping()`

### Integration Tests
- `test_sandbox_clean_scaffold_build()`
- `test_sandbox_typescript_error_capture()`
- `test_sandbox_timeout_enforcement()`

### End-to-End Tests
- None.

### Manual Testing Checklist
- [ ] Trigger test build of scaffold in E2B.
- [ ] Inspect E2B dashboard; verify session terminates cleanly after run.
- [ ] Disconnect internet on host; test local Docker runner fallback.

### Regression Tests
- Re-run Phase 1 contracts tests.

### Rollback Strategy
- Toggle `SANDBOX_PROVIDER=docker` if E2B experiences external outage.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Sandbox running out of memory (OOM) during Vite asset bundling on 2GB limit.
- *Mitigation:* Pin `NODE_OPTIONS=--max-old-space-size=1536` to prevent swapping and runaway heap growth.

### Future Improvements
- MicroVM warm pool recycling to reduce initial spin-up latency below 1 second.
