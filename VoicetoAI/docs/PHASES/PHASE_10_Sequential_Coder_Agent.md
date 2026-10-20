# Phase 10: Sequential Coder Agent & Greenfield Code Generation

---

### Navigation
- **Current Phase:** Phase 10 of 20
- **Previous Phase:** [Phase 9: Stack-Aware Architectural Planner Agent](file:///d:/VoicetoAI/docs/PHASES/PHASE_09_Architectural_Planner_Agent.md)
- **Next Phase:** [Phase 11: Playwright Headless Visual & Functional Verifier Node](file:///d:/VoicetoAI/docs/PHASES/PHASE_11_Playwright_Verifier_Node.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [Agents_Orchestration.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Agents_Orchestration.md), [Sandboxing_Execution.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Sandboxing_Execution.md)

---

### Objective
Deploy the Coder Agent using Claude 3.5 Sonnet to generate complete, production-ready TypeScript and Tailwind files sequentially (one file at a time) based on the Planner's blueprint.

### Business Goal
Deliver clean, maintainable, bespoke website source code that small business owners actually own—not minified black-box templates.

### Technical Goal
Implement file-by-file sequential generation, managing context windows efficiently and streaming generation progress to the user interface.

### Features Included
- Production `coder_node` using Claude 3.5 Sonnet.
- Sequential file generation loop with progress tracking.
- Markdown code fence stripping and syntax validation.
- Real-time WebSocket code generation progress streaming to frontend.

### Features NOT Included
- Sandbox compilation, automatic bug fixing (handled in Phase 11 & 12).

### Dependencies
- Phase 6 (Scaffolds), Phase 9 (Planner).

### Deliverables
- `backend/app/agents/coder.py`.
- `frontend/components/chat/FileGenerationProgress.tsx`.
- Test suite validating syntactic correctness of generated files.

### Architecture Changes
- LangGraph executes the sequential Coder node loop, populating `state["generated_files"]`.

### Database Changes
- None (Code kept in memory / state until sandbox verification).

### API Changes
- WebSocket event: `file_generation_started`, `file_generation_completed`.

### Frontend Changes
- Animated file tree view showing checkmarks as files are generated in real time.

### Backend Changes
- Async generator streaming file creation events over WebSockets.

### ML Changes
- Coder system prompt enforcing strict TypeScript and Tailwind conventions.

### Infrastructure Changes
- None.

### Configuration Required
- Model: `claude-3-5-sonnet-20241022`, max tokens 4096 per file, temperature 0.2.

### Environment Variables
- `ANTHROPIC_API_KEY`.

### Third-party Services
- Anthropic Claude API.

### Tasks
- [x] Task 10.1: Author Coder system prompt with strict typing constraints.
- [x] Task 10.2: Implement single-file generation loop with context pruning.
- [x] Task 10.3: Wire WebSocket progress emission to frontend.
- [x] Task 10.4: Implement AST syntax checker for generated TypeScript.

### Subtasks
- Subtask 10.2.1: Provide `data/site.json` as persistent context to all component generation calls.
- Subtask 10.4.1: Use `esprima` or TypeScript compiler API to catch raw syntax errors before sandbox.

### Acceptance Criteria
- Coder generates all files listed in `PlanContract` without truncation.
- All copy rendered in components is sourced from `data/site.json`.
- Zero syntax errors in generated `.tsx` and `.json` files.

### Definition of Done
- Complete file generation loop executes reliably across 15 benchmark plans; PR merged.

### Unit Tests
- `test_coder_code_fence_extraction()`
- `test_coder_site_json_import_validation()`
- `test_coder_lucide_icon_usage()`

### Integration Tests
- `test_planner_to_coder_execution_pipeline()`

### End-to-End Tests
- None.

### Manual Testing Checklist
- [ ] Run generation for a test jewelry shop plan.
- [ ] Inspect generated files on disk; verify zero placeholders like `// TODO: add code`.
- [ ] Verify UI shows live checkmarks as each component completes.

### Regression Tests
- Re-run Phase 6, 8, and 9 tests.

### Rollback Strategy
- Revert Coder prompt changes to last pinned prompt version in Git.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Large files exceeding completion token limits causing truncated code.
- *Mitigation:* Planner enforces modular file size limits; Coder generates files one at a time.

### Future Improvements
- Parallel file generation for independent leaf components.
