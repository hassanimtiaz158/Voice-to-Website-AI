# Phase 14: File Manifest Indexing & pgvector Semantic Locator Agent

---

### Navigation
- **Current Phase:** Phase 14 of 20
- **Previous Phase:** [Phase 13: GitHub MCP Integration & Committer Node Versioning](file:///d:/VoicetoAI/docs/PHASES/PHASE_13_GitHub_MCP_Committer.md)
- **Next Phase:** [Phase 15: Surgical Editor Agent & Automated Version Diff Engine](file:///d:/VoicetoAI/docs/PHASES/PHASE_15_Surgical_Editor_and_Rollback.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [RAG_ManifestSearch.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/RAG_ManifestSearch.md), [TDD.md](file:///d:/VoicetoAI/docs/TDD.md)

---

### Objective
Deploy the File Manifest Indexer and pgvector Semantic Locator to shortlist 1 to 5 affected files for modification requests using the 3-signal retrieval algorithm.

### Business Goal
Drastically reduce editing costs and latency by enabling surgical edits, avoiding catastrophic full-project regenerations.

### Technical Goal
Implement file manifest extraction (path, role, summary, exports, imports, hash) and 3-signal hybrid retrieval (pgvector cosine search + BM25 keyword matching + import graph traversal).

### Features Included
- Manifest builder: generates 1-sentence summaries and extracts AST exports/imports.
- pgvector 1536-dimensional embedding generation (`text-embedding-3-small`).
- Differential re-indexing (only changed files re-embedded; unchanged files copied).
- Production `locator_node` executing 3-signal retrieval and returning 1 to 5 files.
- Conventional routing: auto-routes copy edits to `data/site.json`.

### Features NOT Included
- Diff generation, sandbox diff application (Phase 15).

### Dependencies
- Phase 2 (Postgres + pgvector), Phase 13 (GitHub MCP & Versions).

### Deliverables
- `backend/app/services/manifest_indexer.py`.
- `backend/app/agents/locator.py`.
- 30 benchmark surgical edit retrieval evaluation scenarios.

### Architecture Changes
- PostgreSQL pgvector actively queried during `SMALL_EDIT` workflow paths.

### Database Changes
- Inserts file rows into `files` table with embeddings and HNSW indexing.

### API Changes
- Internal query interface: `await locator.locate_affected_files(project_id, version_n, prompt) -> List[str]`.

### Frontend Changes
- None (internal retrieval).

### Backend Changes
- Manifest indexing service executed immediately after Committer node succeeds.

### ML Changes
- Small LLM (Claude 3.5 Haiku) for file summarization; OpenAI `text-embedding-3-small`.

### Infrastructure Changes
- None.

### Configuration Required
- Embedding dimension: 1536; HNSW search parameter `ef_search = 40`.

### Environment Variables
- `OPENAI_API_KEY` (for embeddings).

### Third-party Services
- OpenAI Embeddings API.

### Tasks
- [x] Task 14.1: Build AST parser extracting `imports` and `exports` from TSX.
- [x] Task 14.2: Implement file summary generator using Claude 3.5 Haiku.
- [x] Task 14.3: Implement pgvector embedding storage in `files` table.
- [x] Task 14.4: Build 3-signal hybrid retrieval algorithm in SQL/Python.
- [x] Task 14.5: Run Locator accuracy evaluation across 30 edit tasks.

### Subtasks
- Subtask 14.4.1: Write SQL query combining cosine distance and keyword matching.
- Subtask 14.4.2: Implement import graph expansion in Python.

### Acceptance Criteria
- File manifest indexing completes in $<1.5\text{ seconds}$ for a 25-file repository.
- Locator identifies the exact correct files in $\ge 90\%$ of the 30 benchmark edit tasks.
- Text-only edit prompts route to `data/site.json` 100% of the time.

### Definition of Done
- Locator passes retrieval benchmark with $\ge 90\%$ accuracy; PR merged.

### Unit Tests
- `test_ast_import_export_extraction()`
- `test_file_summary_generation()`
- `test_convention_routing_rules()`

### Integration Tests
- `test_manifest_indexing_transaction()`
- `test_pgvector_similarity_search()`

### End-to-End Tests
- None.

### Manual Testing Checklist
- [ ] Index test e-commerce site.
- [ ] Query: "Change the WhatsApp order phone number".
- [ ] Verify Locator returns strictly `['data/site.json']`.
- [ ] Query: "Make the product card border rounded with a drop shadow".
- [ ] Verify Locator returns `['src/components/ProductCard.tsx']`.

### Regression Tests
- Re-run Phase 2, 7, and 13 tests.

### Rollback Strategy
- Fall back to reading entire file manifest directly in prompt if pgvector search fails.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Import graph circular references causing infinite loops in dependency traversal.
- *Mitigation:* Traversal depth strictly bounded to 1 hop (direct parents and direct children only).

### Future Improvements
- Self-hosted embedding model using Hugging Face `bge-small-en-v1.5` on CPU.
