# Phase 9: Stack-Aware Architectural Planner Agent

---

### Navigation
- **Current Phase:** Phase 9 of 20
- **Previous Phase:** [Phase 8: Tri-Modal Router & Diagnostic Clarifier Agent with Interrupts](file:///d:/VoicetoAI/docs/PHASES/PHASE_08_Router_and_Clarifier_Agent.md)
- **Next Phase:** [Phase 10: Sequential Coder Agent & Greenfield Code Generation](file:///d:/VoicetoAI/docs/PHASES/PHASE_10_Sequential_Coder_Agent.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [Agents_Orchestration.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Agents_Orchestration.md)

---

### Objective
Deploy the Planner Agent using Claude 3.5 Sonnet to convert verified `RequirementsContract` specifications into a modular, dependency-ordered `PlanContract` for `vite-react-tailwind`.

### Business Goal
Prevent monolithic, spaghetti code generation by enforcing clean software engineering architecture and central data separation.

### Technical Goal
Synthesize architectural file plans specifying paths, roles, exact single-responsibility descriptions, imports, and exports, while enforcing the `data/site.json` invariant.

### Features Included
- Production `planner_node` using Claude 3.5 Sonnet.
- Conventional data separation enforcement (`data/site.json` holds 100% of copy).
- File dependency topological sorter (ensuring data and UI primitives are created before composite views).
- Validation against `PlanContract` schema.

### Features NOT Included
- Full code generation, sandbox execution.

### Dependencies
- Phase 1 (Contracts), Phase 8 (Clarifier & Requirements).

### Deliverables
- `backend/app/agents/planner.py`.
- `backend/app/orchestrator/topological_sorter.py`.
- Unit and integration tests for plan generation.

### Architecture Changes
- LangGraph transitions from Requirements confirmation directly to the Planner node.

### Database Changes
- None (Plan is maintained in LangGraph state).

### API Changes
- None (internal graph node).

### Frontend Changes
- UI displays real-time "Architecting site structure..." progress bar in chat view.

### Backend Changes
- Planner service with prompt caching to reduce token costs on repeated planning runs.

### ML Changes
- Planner system prompt with strict Vite + React 19 + Tailwind architecture rules.

### Infrastructure Changes
- None.

### Configuration Required
- Model assignment: `claude-3-5-sonnet-20241022`, max tokens 4096, temperature 0.2.

### Environment Variables
- Inherited from Phase 8 (`ANTHROPIC_API_KEY`).

### Third-party Services
- Anthropic Claude API.

### Tasks
- [x] Task 9.1: Author Planner system prompt enforcing data separation.
- [x] Task 9.2: Implement Pydantic output parsing for `PlanContract`.
- [x] Task 9.3: Build topological dependency sorter for generated files.
- [x] Task 9.4: Implement validation test suite against 15 diverse retail specs.

### Subtasks
- Subtask 9.1.1: Include standard Vite component tree examples in prompt context.
- Subtask 9.3.1: Verify no circular dependencies exist in generated plan.

### Acceptance Criteria
- Every generated plan includes `data/site.json`, `src/App.tsx`, and modular components in `src/components/`.
- Zero circular dependencies in the file dependency graph.
- 100% of generated plans parse into `PlanContract` without schema errors.

### Definition of Done
- Planner generates valid file trees across all 15 benchmark test requirements; PR merged.

### Unit Tests
- `test_planner_schema_validation()`
- `test_topological_sorter_order()`
- `test_enforcement_of_site_json_in_plan()`

### Integration Tests
- `test_clarifier_to_planner_handoff()`

### End-to-End Tests
- None for this phase.

### Manual Testing Checklist
- [ ] Pass Bakery RequirementsContract into Planner.
- [ ] Inspect emitted file plan; verify `data/site.json`, `Navbar.tsx`, `Hero.tsx`, `MenuGrid.tsx` exist.
- [ ] Verify each file has clear import/export lists.

### Regression Tests
- Re-run Phase 1 and 8 tests.

### Rollback Strategy
- Fall back to static template file plan if dynamic planner produces schema violations.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 3 days.

### Risks
- Planner hallucinating non-existent npm libraries not present in scaffold.
- *Mitigation:* Planner system prompt explicitly pins allowed packages (`lucide-react`, `clsx`, `tailwind-merge`).

### Future Improvements
- Support for multi-page routing configurations (`react-router-dom`).
