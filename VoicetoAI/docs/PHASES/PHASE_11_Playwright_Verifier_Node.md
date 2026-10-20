# Phase 11: Playwright Headless Visual & Functional Verifier Node

---

### Navigation
- **Current Phase:** Phase 11 of 20
- **Previous Phase:** [Phase 10: Sequential Coder Agent & Greenfield Code Generation](file:///d:/VoicetoAI/docs/PHASES/PHASE_10_Sequential_Coder_Agent.md)
- **Next Phase:** [Phase 12: Targeted Fixer Agent & Self-Healing Build Loop](file:///d:/VoicetoAI/docs/PHASES/PHASE_12_Fixer_Agent_Self_Healing.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [Sandboxing_Execution.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Sandboxing_Execution.md), [TESTING.md](file:///d:/VoicetoAI/docs/TESTING.md)

---

### Objective
Deploy the automated Verifier Node running headless Playwright tests inside the sandbox to audit DOM structure, console error logs, layout overflow, and visual snapshots.

### Business Goal
Guarantee that a customer never sees a broken preview, blank screen, or misaligned layout.

### Technical Goal
Implement headless Chromium execution within the sandbox, capturing full-page PNG screenshots, detecting horizontal overflow, and evaluating console errors.

### Features Included
- `verifier_node` in LangGraph.
- Playwright automated smoke test suite (`tests/smoke.spec.ts`).
- Horizontal layout overflow detection script.
- Console error log interceptor.
- Full-page screenshot capture uploaded to S3.

### Features NOT Included
- Automated code fixing (Fixer node handles repairs in Phase 12).

### Dependencies
- Phase 3 (S3 Storage), Phase 6 (Sandbox), Phase 10 (Coder).

### Deliverables
- `backend/app/agents/verifier.py`.
- Pinned Playwright smoke test script in sandbox base image.
- S3 screenshot uploader utility.

### Architecture Changes
- Sandbox execution pipeline extended to include Stage 5 (Playwright Visual Verification).

### Database Changes
- None.

### API Changes
- None (internal graph node).

### Frontend Changes
- Live preview iframe displays full-page screenshot as instant placeholder while iframe hydrates.

### Backend Changes
- Verifier service parsing Playwright test results and screenshot paths.

### ML Changes
- Optional: Claude 3.5 Sonnet vision check on generated screenshot (stretch goal).

### Infrastructure Changes
- Playwright browser binaries pre-baked into sandbox base image.

### Configuration Required
- Viewport size: 1280x800 (Desktop) and 375x667 (Mobile).

### Environment Variables
- None.

### Third-party Services
- None (local to sandbox).

### Tasks
- [x] Task 11.1: Author `smoke.spec.ts` testing title, console errors, and horizontal scroll.
- [x] Task 11.2: Pre-bake Chromium binaries into sandbox Docker/E2B image.
- [x] Task 11.3: Wire Verifier node into LangGraph state machine.
- [x] Task 11.4: Implement screenshot upload to S3 `voicetoai-artifacts` bucket.

### Subtasks
- Subtask 11.1.1: Write DOM evaluation script checking `document.documentElement.scrollWidth`.
- Subtask 11.3.1: Map Playwright failure codes to `BuildResultContract`.

### Acceptance Criteria
- Sites with console errors or horizontal overflow are flagged as failing verification.
- Sites that pass render cleanly produce a high-resolution full-page PNG screenshot in S3 in $<4\text{ seconds}$.

### Definition of Done
- Verifier node runs cleanly inside sandbox; verified test suite passes; PR merged.

### Unit Tests
- `test_verifier_result_parsing()`
- `test_overflow_detection_logic()`

### Integration Tests
- `test_sandbox_playwright_execution()`
- `test_screenshot_s3_upload()`

### End-to-End Tests
- None.

### Manual Testing Checklist
- [ ] Intentionally inject `console.error("Critical failure")` into test component.
- [ ] Assert Verifier flags failure and blocks promotion.
- [ ] Inject 2000px wide div; assert Verifier detects horizontal layout overflow.

### Regression Tests
- Re-run Phase 6 and 10 tests.

### Rollback Strategy
- Soften verification assertions to warn-only if third-party CDN fonts trigger spurious console warnings.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 3 days.

### Risks
- Headless browser crashing due to sandbox memory constraints.
- *Mitigation:* Launch Chromium with `--disable-dev-shm-usage` and `--no-sandbox` flags.

### Future Improvements
- Automated visual regression diffing against previous version screenshots.
