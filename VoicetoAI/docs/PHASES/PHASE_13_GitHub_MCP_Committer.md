# Phase 13: GitHub MCP Integration & Committer Node Versioning

---

### Navigation
- **Current Phase:** Phase 13 of 20
- **Previous Phase:** [Phase 12: Targeted Fixer Agent & Self-Healing Build Loop](file:///d:/VoicetoAI/docs/PHASES/PHASE_12_Fixer_Agent_Self_Healing.md)
- **Next Phase:** [Phase 14: File Manifest Indexing & pgvector Semantic Locator Agent](file:///d:/VoicetoAI/docs/PHASES/PHASE_14_File_Manifest_pgvector_Locator.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [REPOSITORY_STRATEGY.md](file:///d:/VoicetoAI/docs/REPOSITORY_STRATEGY.md), [TDD.md](file:///d:/VoicetoAI/docs/TDD.md)

---

### Objective
Integrate the official GitHub Model Context Protocol (MCP) server to establish GitHub as the single source of truth, committing verified code to `main` and tagging versions (`vN`).

### Business Goal
Provide enterprise-grade source code ownership and version control, enabling clients to access their real GitHub repository and roll back changes safely.

### Technical Goal
Deploy the `github/github-mcp-server` client in Python, executing authenticated Git operations (create private repo, commit tree, create Git tag, manage branches).

### Features Included
- GitHub MCP client service in `backend/app/mcp/github_client.py`.
- Committer node in LangGraph (executes only after sandbox verification passes).
- Dedicated private repository creation under platform organization per project.
- Atomic commit to `main` tagged with `vN`.
- Database synchronization with `versions` table (recording commit SHA, parent version, requirements version).

### Features NOT Included
- Incremental surgical editing (Phase 14 & 15).

### Dependencies
- Phase 2 (Database), Phase 11 (Verifier Node).

### Deliverables
- GitHub MCP server wrapper module.
- `committer_node` in LangGraph.
- Integration test suite executing live Git operations against a test GitHub organization.

### Architecture Changes
- GitHub Cloud integrated as external source of truth; backend writes verified code directly to Git repositories.

### Database Changes
- Inserts new row into `versions` table with `commit_sha`, `n`, `parent_n`, and `status = 'verified'`.

### API Changes
- `GET /api/v1/projects/{id}/versions`: Returns list of all verified version tags and commit SHAs.

### Frontend Changes
- UI displays GitHub repository badge with clickable commit link and version tag pills (`v1`, `v2`).

### Backend Changes
- Committer node invoking GitHub MCP `create_or_update_file_contents` / Git Tree API.

### ML Changes
- None (deterministic code-only node).

### Infrastructure Changes
- GitHub App or fine-grained Personal Access Token provisioned with repository administration permissions.

### Configuration Required
- Platform GitHub Organization name and token.

### Environment Variables
- `GITHUB_ORG_NAME=voicetoai-projects`
- `GITHUB_APP_ID=123456`
- `GITHUB_APP_PRIVATE_KEY=...`

### Third-party Services
- GitHub Cloud API / Official GitHub MCP Server.

### Tasks
- [x] Task 13.1: Configure GitHub App with repository administration permissions.
- [x] Task 13.2: Implement GitHub MCP client in Python.
- [x] Task 13.3: Implement Committer node committing files and creating tag `vN`.
- [x] Task 13.4: Wire database record creation in `versions` table.

### Subtasks
- Subtask 13.2.1: Write tree builder creating atomic multi-file Git commit.
- Subtask 13.3.1: Implement tag creation API call (`refs/tags/vN`).

### Acceptance Criteria
- Every verified build creates a single atomic commit on `main` and a matching Git tag `v1`.
- Commit message contains structured metadata (trigger message, requirements version).
- Database `versions` table accurately mirrors GitHub commit SHA.

### Definition of Done
- Committer node verified with live GitHub test repository; PR merged.

### Unit Tests
- `test_github_mcp_payload_formatting()`
- `test_version_record_db_mapping()`

### Integration Tests
- `test_github_repo_creation_and_atomic_commit()`
- `test_git_tag_creation()`

### End-to-End Tests
- Greenfield generation from voice prompt resulting in a live verified repository on GitHub.

### Manual Testing Checklist
- [ ] Run test build; verify new private repository appears in GitHub organization.
- [ ] Inspect repository commits; verify exactly one commit on `main` tagged `v1`.
- [ ] Inspect code; verify all files match sandbox output.

### Regression Tests
- Re-run Phases 2, 7, and 11 tests.

### Rollback Strategy
- In case of GitHub API rate limits, write tarball archive to S3 bucket as temporary fallback.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 4 days.

### Risks
- GitHub API secondary rate limits during rapid parallel generation tests.
- *Mitigation:* Use authenticated GitHub App tokens with high rate limit quotas (5,000 requests/hr).

### Future Improvements
- Webhook listener to sync external developer commits back to platform database.
