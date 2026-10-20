# Phase 15: Surgical Editor Agent & Automated Version Diff Engine

---

### Navigation
- **Current Phase:** Phase 15 of 20
- **Previous Phase:** [Phase 14: File Manifest Indexing & pgvector Semantic Locator Agent](file:///d:/VoicetoAI/docs/PHASES/PHASE_14_File_Manifest_pgvector_Locator.md)
- **Next Phase:** [Phase 16: Authentication, Multi-Tenant RBAC & Quota Subscriptions](file:///d:/VoicetoAI/docs/PHASES/PHASE_16_Auth_RBAC_and_Quotas.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [Agents_Orchestration.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Agents_Orchestration.md), [RAG_ManifestSearch.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/RAG_ManifestSearch.md)

---

### Objective
Deploy the Editor Agent using Claude 3.5 Sonnet to produce unified diffs strictly for the 1 to 3 files shortlisted by the Locator, verifying and committing version `v(N+1)`.

### Business Goal
Enable rapid, sub-30-second site updates for pennies, providing customers with responsive iterative refinement without breaking existing features.

### Technical Goal
Implement unified diff generation, git-apply patching in the sandbox, full-project regression testing, and atomic GitHub commits for incremental versions.

### Features Included
- Production `editor_node` using Claude 3.5 Sonnet.
- Unified diff synthesizer targeting only shortlisted files.
- Patch application engine in sandbox (`git apply --check && git apply`).
- Full-project sandbox verification (ensuring edits don't break dependent components).
- Committer creates new commit and tags `v(N+1)`.
- Reversible rollback engine via tag checkout.

### Features NOT Included
- Human deployment marketplace (Phase 17).

### Dependencies
- Phase 6 (Sandbox), Phase 12 (Fixer), Phase 13 (GitHub MCP), Phase 14 (Locator).

### Deliverables
- `backend/app/agents/editor.py`.
- `backend/app/services/patcher.py`.
- Rollback service in `backend/app/services/rollback.py`.
- Frontend diff viewer component.

### Architecture Changes
- The incremental modification loop is fully operational end-to-end.

### Database Changes
- Inserts new row into `versions` linked to parent version; updates `files` content hashes.

### API Changes
- `POST /api/v1/projects/{id}/edit`: Dispatches edit workflow.
- `POST /api/v1/projects/{id}/rollback/{version_n}`: Executes rollback.

### Frontend Changes
- Version history timeline in UI with "Rollback to this version" button.
- Code diff preview drawer showing green/red line changes.

### Backend Changes
- Editor agent prompt integration; Git patch application handler.

### ML Changes
- Editor system prompt optimized for emitting clean unified diffs.

### Infrastructure Changes
- None.

### Configuration Required
- Model: `claude-3-5-sonnet-20241022`, max tokens 4000, temperature 0.1.

### Environment Variables
- `ANTHROPIC_API_KEY`.

### Third-party Services
- Anthropic Claude API, GitHub MCP.

### Tasks
- [x] Task 15.1: Implement Editor agent producing unified diffs.
- [x] Task 15.2: Implement patch application service in sandbox.
- [x] Task 15.3: Wire Editor $\to$ Sandbox $\to$ Verifier $\to$ Committer loop in LangGraph.
- [x] Task 15.4: Implement rollback API checking out historical tag.
- [x] Task 15.5: Run 30-task surgical edit benchmark measuring regression rate.

### Subtasks
- Subtask 15.2.1: Implement fallback to full file replacement if `git apply` rejects fuzzy whitespace diff.
- Subtask 15.4.1: Write Git revert / checkout tag logic via GitHub MCP.

### Acceptance Criteria
- Incremental edit modifies only the intended files, touching $\le 3$ files.
- Full sandbox build and Playwright tests pass before committing tag `v2`.
- Rollback to `v1` restores exact previous files and preview URL.
- Zero regressions across the 30 benchmark edit tasks.

### Definition of Done
- Complete edit and rollback flow verified in browser; eval benchmark passing; PR merged.

### Unit Tests
- `test_diff_parsing_and_sanitization()`
- `test_patch_application_clean()`
- `test_patch_application_reject_handling()`

### Integration Tests
- `test_end_to_end_edit_workflow()`
- `test_version_rollback_git_checkout()`

### End-to-End Tests
- User creates site (v1) $\to$ speaks edit: "Make header sticky" $\to$ site updates to v2 $\to$ user clicks rollback $\to$ site returns to v1.

### Manual Testing Checklist
- [ ] Edit headline text; verify only `data/site.json` changed in GitHub commit diff.
- [ ] Edit button color; verify only `ProductCard.tsx` changed.
- [ ] Click "Rollback to v1" in UI; assert preview immediately reverts to original state.

### Regression Tests
- Re-run all previous phase test suites.

### Rollback Strategy
- Automatic: If patch fails tests, attempt stays on draft branch and main remains untouched.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Fuzzy diffs failing to apply due to LLM line number hallucinations.
- *Mitigation:* Patcher engine attempts `git apply -3` (3-way merge) and falls back to whole-file replacement for the target file if diff fails.

### Future Improvements
- Interactive visual point-and-click element selector in the preview iframe to guide the Locator.
