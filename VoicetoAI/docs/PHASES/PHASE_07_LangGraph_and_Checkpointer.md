# Phase 7: LangGraph State Machine Skeleton & Postgres Checkpointer

---

### Navigation
- **Current Phase:** Phase 7 of 20
- **Previous Phase:** [Phase 6: Pinned Scaffolds & E2B / Docker Sandbox Runner Engine](file:///d:/VoicetoAI/docs/PHASES/PHASE_06_Scaffold_and_Sandbox_Runner.md)
- **Next Phase:** [Phase 8: Tri-Modal Router & Diagnostic Clarifier Agent with Interrupts](file:///d:/VoicetoAI/docs/PHASES/PHASE_08_Router_and_Clarifier_Agent.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [Agents_Orchestration.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Agents_Orchestration.md), [TDD.md](file:///d:/VoicetoAI/docs/TDD.md)

---

### Objective
Implement the deterministic LangGraph state machine with persistent PostgreSQL checkpointing (`PostgresSaver`) and human-in-the-loop `interrupt()` support.

### Business Goal
Guarantee that complex, multi-turn AI interactions never lose state, survive server restarts, and can pause for user decisions indefinitely without data loss.

### Technical Goal
Construct the cyclic `StateGraph` using `ProjectGraphState`, wire all conditional edges, and attach the async Postgres checkpointer.

### Features Included
- LangGraph state machine definition in `backend/app/orchestrator/graph.py`.
- Persistence using `langgraph.checkpoint.postgres.aio.AsyncPostgresSaver`.
- State schema validation with typed Pydantic handoffs.
- Human-in-the-loop interruption mechanism (`interrupt()`).

### Features NOT Included
- Complex LLM agent prompts (mock agent nodes used to validate state transitions).

### Dependencies
- Phase 1 (Contracts), Phase 2 (Postgres Database), Phase 6 (Sandbox).

### Deliverables
- `backend/app/orchestrator/state.py`.
- `backend/app/orchestrator/graph.py`.
- Unit tests verifying 100% of state graph branch paths.

### Architecture Changes
- Introduction of the centralized LangGraph execution engine governing all workflow routing.

### Database Changes
- Automatic creation of LangGraph checkpoint tables (`checkpoints`, `checkpoint_blobs`, `checkpoint_writes`) via `AsyncPostgresSaver`.

### API Changes
- `POST /api/v1/projects/{id}/graph/invoke`: Dispatches or resumes graph thread.
- `GET /api/v1/projects/{id}/graph/state`: Retrieves current thread state.

### Frontend Changes
- None (API-level state testing).

### Backend Changes
- Orchestration service wiring FastAPI background tasks to LangGraph runner.

### ML Changes
- None.

### Infrastructure Changes
- None.

### Configuration Required
- LangGraph thread ID formatting (`project_id:version_n`).

### Environment Variables
- `LANGGRAPH_CHECKPOINT_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/voicetoai_db`

### Third-party Services
- None.

### Tasks
- [x] Task 7.1: Define `ProjectGraphState` TypedDict.
- [x] Task 7.2: Wire nodes: `router`, `clarifier`, `planner`, `coder`, `sandbox`, `fixer`, `verifier`, `committer`.
- [x] Task 7.3: Implement conditional branching edges.
- [x] Task 7.4: Initialize `AsyncPostgresSaver` checkpointer.
- [x] Task 7.5: Implement resumption test after simulated server crash.

### Subtasks
- Subtask 7.2.1: Implement mock node functions returning deterministic state updates.
- Subtask 7.3.1: Write conditional routing functions (`should_continue_clarification`, `should_fix_or_verify`).

### Acceptance Criteria
- Graph execution halts at `clarifier` node when `interrupt()` is called.
- Backend can resume execution by submitting answers to the same `thread_id`.
- Complete execution history is retrievable from Postgres checkpoints.

### Definition of Done
- State graph passes cyclic execution and recovery tests with 100% branch coverage; PR merged.

### Unit Tests
- `test_state_initialization_defaults()`
- `test_conditional_routing_router_decisions()`
- `test_conditional_routing_fixer_retry_counter()`

### Integration Tests
- `test_postgres_saver_persistence()`
- `test_graph_interrupt_and_resumption()`

### End-to-End Tests
- Mock end-to-end execution through all nodes without LLM API calls.

### Manual Testing Checklist
- [ ] Invoke graph via curl; verify checkpoint row written in `checkpoints` table.
- [ ] Kill FastAPI server while graph is paused on interrupt.
- [ ] Restart FastAPI; send resume payload; verify graph completes successfully.

### Regression Tests
- Re-run Phase 2 and 6 tests.

### Rollback Strategy
- Revert graph definition to linear mock pipeline.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Database deadlocks during concurrent checkpoint writes on high-volume threads.
- *Mitigation:* Ensure strict 1-to-1 thread mapping per project with row-level locking.

### Future Improvements
- Graph execution visualization streaming via LangGraph Studio integration.
