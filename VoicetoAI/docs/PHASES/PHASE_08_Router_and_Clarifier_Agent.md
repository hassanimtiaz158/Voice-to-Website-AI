# Phase 8: Tri-Modal Router & Diagnostic Clarifier Agent with Interrupts

---

### Navigation
- **Current Phase:** Phase 8 of 20
- **Previous Phase:** [Phase 7: LangGraph State Machine Skeleton & Postgres Checkpointer](file:///d:/VoicetoAI/docs/PHASES/PHASE_07_LangGraph_and_Checkpointer.md)
- **Next Phase:** [Phase 9: Stack-Aware Architectural Planner Agent](file:///d:/VoicetoAI/docs/PHASES/PHASE_09_Architectural_Planner_Agent.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [Agents_Orchestration.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Agents_Orchestration.md), [PRD.md](file:///d:/VoicetoAI/docs/PRD.md)

---

### Objective
Deploy production LLM nodes for the tri-modal Router and diagnostic Clarifier using Claude 3.5 Haiku, capturing user decisions and structured requirements summaries.

### Business Goal
Transform vague, non-technical shop owner inputs into precise, unambiguous technical specifications within 3 turns, eliminating developer back-and-forth.

### Technical Goal
Implement Claude 3.5 Haiku structured prompting with few-shot examples, JSON schema validation, and database audit logging to `decisions` and `requirements` tables.

### Features Included
- Production `router_node`: classifies into `QUESTION`, `SMALL_EDIT`, or `NEW_OR_MAJOR`.
- Production `clarifier_node`: generates 3 to 5 multiple-choice questions per turn (with "You Decide" option).
- Turn counter enforcement (max 3 turns).
- Requirements summary generator and confirmation gate.
- Audit persistence in `decisions` and `requirements` tables.

### Features NOT Included
- Code planning, code generation, sandbox builds.

### Dependencies
- Phase 7 (LangGraph Engine), Phase 2 (Database).

### Deliverables
- `backend/app/agents/router.py`.
- `backend/app/agents/clarifier.py`.
- `frontend/components/chat/ClarifierQuestionCard.tsx`.
- 20 scripted shop owner persona test cases in `evals/personas/`.

### Architecture Changes
- Real LLM calls integrated into LangGraph pipeline using Anthropic Python SDK.

### Database Changes
- Writes to `decisions` table and `requirements` table.

### API Changes
- `POST /api/v1/projects/{id}/clarify/answer`: Submits user choices and resumes LangGraph thread.

### Frontend Changes
- Dynamic option card UI rendering multi-choice question bubbles with one-click selection.
- Sticky "Requirements Summary" card with "Approve & Build" CTA.

### Backend Changes
- Anthropic API client wrapper with prompt caching headers (`cache_control: {"type": "ephemeral"}`).

### ML Changes
- Prompt engineering for Clarifier and Router; few-shot bilingual Urdu/English examples.

### Infrastructure Changes
- Anthropic API key provisioning.

### Configuration Required
- Model assignment: `claude-3-5-haiku-20241022`, max tokens 2500, temperature 0.2.

### Environment Variables
- `ANTHROPIC_API_KEY=sk-ant-...`

### Third-party Services
- Anthropic Claude API.

### Tasks
- [x] Task 8.1: Implement Router agent with strict JSON output schema.
- [x] Task 8.2: Implement Clarifier agent with 3-turn state tracker.
- [x] Task 8.3: Implement "You Decide" fallback resolution logic.
- [x] Task 8.4: Build frontend Clarifier question options UI.
- [x] Task 8.5: Run Persona evaluation benchmark (20 synthetic shop owners).

### Subtasks
- Subtask 8.2.1: Format system prompt enforcing 3 to 5 options per question.
- Subtask 8.3.1: Write decision recorder saving choice and rationale to PostgreSQL.

### Acceptance Criteria
- Router achieves $\ge 96\%$ classification accuracy across 50 benchmark prompts.
- Clarifier completes requirements in $\le 3$ conversational turns for 100% of the 20 test personas.
- Every user decision is queryable in the `decisions` table.
- Requirements summary conforms 100% to `RequirementsContract` Pydantic schema.

### Definition of Done
- Interactive clarification flow fully functional in web UI; eval benchmark passing; PR merged.

### Unit Tests
- `test_router_prompt_classification()`
- `test_clarifier_option_generation()`
- `test_clarifier_turn_limit_guard()`

### Integration Tests
- `test_clarification_to_requirements_db_persistence()`
- `test_clarifier_resumption_via_api()`

### End-to-End Tests
- Complete browser test: enter prompt $\to$ answer 2 turns of questions $\to$ review summary $\to$ approve.

### Manual Testing Checklist
- [ ] Enter: "Mujhe Lahore mein bakery ke liye website chahiye".
- [ ] Verify Clarifier asks 3-5 questions with options (e.g. Products, Delivery, Theme).
- [ ] Select "You Decide" for color theme; verify default is recorded in decisions table.
- [ ] Verify final summary displays bakery details clearly.

### Regression Tests
- Re-run Phase 4 and Phase 7 tests.

### Rollback Strategy
- Fall back to static form-based requirements collector if LLM API fails.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 4 days.

### Risks
- Users providing freeform answers that do not match the multiple-choice options.
- *Mitigation:* Clarifier prompt instructs the model to synthesize freeform text and normalize it into structured fields.

### Future Improvements
- Voice playback of Clarifier questions using Edge-TTS Urdu voice.
