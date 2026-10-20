# Phase 12: Targeted Fixer Agent & Self-Healing Build Loop

---

### Navigation
- **Current Phase:** Phase 12 of 20
- **Previous Phase:** [Phase 11: Playwright Headless Visual & Functional Verifier Node](file:///d:/VoicetoAI/docs/PHASES/PHASE_11_Playwright_Verifier_Node.md)
- **Next Phase:** [Phase 13: GitHub MCP Integration & Committer Node Versioning](file:///d:/VoicetoAI/docs/PHASES/PHASE_13_GitHub_MCP_Committer.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [Agents_Orchestration.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Agents_Orchestration.md), [Sandboxing_Execution.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Sandboxing_Execution.md)

---

### Objective
Deploy the self-healing Fixer Agent using Claude 3.5 Sonnet to autonomously patch compilation, linting, and Playwright verification errors within a strict 3-retry budget.

### Business Goal
Achieve an autonomous build success rate $\ge 85\%$ without requiring human engineering intervention when minor syntax or import errors occur.

### Technical Goal
Implement targeted self-healing: deliver strictly the failing files and terminal error output to Claude 3.5 Sonnet, apply surgical patches, and quarantine failed runs on draft branches.

### Features Included
- Production `fixer_node` using Claude 3.5 Sonnet.
- Targeted context injection (only error stderr and failing files delivered).
- 3-retry ceiling enforcement with LangGraph conditional loop.
- Quarantine failure path: preserves draft branch on exhaustion and emits friendly user explanation.

### Features NOT Included
- GitHub main branch commits (handled in Phase 13).

### Dependencies
- Phase 6 (Sandbox), Phase 7 (LangGraph), Phase 10 (Coder), Phase 11 (Verifier).

### Deliverables
- `backend/app/agents/fixer.py`.
- Automated test harness simulating 10 common compiler errors and measuring auto-fix recovery.

### Architecture Changes
- LangGraph closes the cyclic self-healing loop: `Sandbox -> Fixer -> Sandbox`.

### Database Changes
- Records retry attempts and repair tokens in `runs` table.

### API Changes
- Real-time build log streaming event: `build_attempt_failed`, `fixer_patching_commenced`.

### Frontend Changes
- Build log console view in UI displaying real-time compiler outputs and fix attempt counter (e.g., "Auto-healing attempt 1/3...").

### Backend Changes
- Fixer agent execution and file patching logic.

### ML Changes
- Fixer system prompt optimized for diagnosing TypeScript and React import errors.

### Infrastructure Changes
- None.

### Configuration Required
- Max retry limit: 3 attempts.

### Environment Variables
- `ANTHROPIC_API_KEY`.

### Third-party Services
- Anthropic Claude API.

### Tasks
- [x] Task 12.1: Author Fixer system prompt with strict surgical patching rules.
- [x] Task 12.2: Implement error context extractor filtering compiler traces.
- [x] Task 12.3: Wire retry decrement and quarantine routing in LangGraph.
- [x] Task 12.4: Validate Fixer across 10 synthetic error cases (missing imports, type mismatches).

### Subtasks
- Subtask 12.2.1: Parse TypeScript error codes (`TS2304`, `TS2322`, `TS2339`).
- Subtask 12.3.1: Implement quarantine state preserving files on `draft/failed-vN`.

### Acceptance Criteria
- Fixer resolves common errors (missing imports, unclosed tags, misspelled props) in $\le 2$ attempts.
- If errors persist after 3 attempts, graph terminates gracefully without crashing and leaves `main` untouched.
- 100% of fix attempts log token usage and costs to `runs` table.

### Definition of Done
- Fixer recovers at least 8 out of 10 synthetic broken builds; PR merged.

### Unit Tests
- `test_fixer_prompt_construction()`
- `test_retry_counter_exhaustion()`
- `test_failing_files_context_isolation()`

### Integration Tests
- `test_sandbox_fixer_closed_loop_recovery()`

### End-to-End Tests
- Greenfield generation with intentional prompt ambiguity recovering and passing within 3 tries.

### Manual Testing Checklist
- [ ] Inject syntax error into `src/components/Hero.tsx`.
- [ ] Run graph; observe UI display "Auto-healing attempt 1/3".
- [ ] Verify Fixer repairs error and sandbox completes with exit code 0.

### Regression Tests
- Re-run Phase 6, 10, and 11 tests.

### Rollback Strategy
- Cap retries at 1 to conserve token budget if API latency increases.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 4 days.

### Risks
- Fixer entering an oscillating loop (fixing error A introduces error B, fixing B re-introduces A).
- *Mitigation:* Feed cumulative error history to Fixer prompt across retries so it detects oscillations.

### Future Improvements
- Fine-tune a specialized, smaller model specifically on TypeScript AST repair diffs.
