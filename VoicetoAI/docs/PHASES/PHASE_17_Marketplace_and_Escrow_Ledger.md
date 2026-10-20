# Phase 17: Human-in-the-Loop Marketplace & Double-Entry Ledger Engine

---

### Navigation
- **Current Phase:** Phase 17 of 20
- **Previous Phase:** [Phase 16: Authentication, Multi-Tenant RBAC & Quota Subscriptions](file:///d:/VoicetoAI/docs/PHASES/PHASE_16_Auth_RBAC_and_Quotas.md)
- **Next Phase:** [Phase 18: Observability, Langfuse Tracing & Full Benchmark Evaluation Suite](file:///d:/VoicetoAI/docs/PHASES/PHASE_18_Observability_and_Eval_Suite.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [Marketplace_Deployment_Ledger.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Marketplace_Deployment_Ledger.md), [TDD.md](file:///d:/VoicetoAI/docs/TDD.md)

---

### Objective
Deploy the Human-in-the-Loop (HITL) Deployment Marketplace, connecting shop owners with verified developers via dedicated chat workrooms, mock escrow payments, and an immutable double-entry ledger.

### Business Goal
Solve the production deployment bottleneck, monetize via a 20% platform commission on developer deployments, and maintain zero regulatory banking risk via an internal ledger.

### Technical Goal
Implement deployment ticket lifecycle, scoped GitHub token dispensing, real-time WebSocket workroom chat, mock payment gateway, and balanced double-entry accounting engine (`ledger_entries`).

### Features Included
- Deployment ticket creation for verified version `vN`.
- Admin assignment portal to dispatch developers.
- Scoped temporary read-only GitHub token generation for assigned developer.
- Dedicated client-developer WebSocket chat room.
- Developer quote submission and client payment approval.
- Double-entry ledger engine enforcing $\sum \text{Debits} = \sum \text{Credits}$.
- Monthly developer payout report generation.

### Features NOT Included
- Real money banking integration (mock gateway with manual bank transfers).

### Dependencies
- Phase 2 (Database Ledger), Phase 13 (GitHub MCP), Phase 16 (Auth & RBAC).

### Deliverables
- `backend/app/services/marketplace.py`.
- `backend/app/services/ledger.py`.
- `frontend/components/marketplace/WorkroomChat.tsx`.
- Admin payout dashboard in `frontend/app/admin/payouts/`.

### Architecture Changes
- Marketplace module connects Users, Developers, and Admins into collaborative workrooms.

### Database Changes
- Writes to `deployment_requests`, `quotes`, `payments`, `ledger_entries`, `payout_periods`, `payouts`.

### API Changes
- `POST /api/v1/marketplace/requests`
- `POST /api/v1/marketplace/quotes`
- `POST /api/v1/marketplace/pay`
- `POST /api/v1/marketplace/confirm-live`
- `GET /api/v1/admin/payouts/report`

### Frontend Changes
- "Deploy to Live Domain" modal in client UI.
- Developer portal dashboard showing assigned tickets and earnings.
- Admin dashboard showing platform ledger balance and pending payouts.

### Backend Changes
- Double-entry ledger service with strict database transaction locking.

### ML Changes
- None.

### Infrastructure Changes
- None.

### Configuration Required
- Platform commission percentage: 20%.

### Environment Variables
- `PLATFORM_COMMISSION_RATE=0.20`

### Third-party Services
- Mock Payment Gateway API.

### Tasks
- [x] Task 17.1: Implement deployment request state machine.
- [x] Task 17.2: Build scoped GitHub installation token dispenser for developers.
- [x] Task 17.3: Build real-time WebSocket chat room for client and developer.
- [x] Task 17.4: Implement double-entry ledger service with mathematical verification.
- [x] Task 17.5: Build monthly payout report generator.

### Subtasks
- Subtask 17.4.1: Write database transaction enforcing debit/credit balance.
- Subtask 17.5.1: Generate CSV export of monthly developer balances.

### Acceptance Criteria
- Every payment, fee, and payout creates balanced ledger rows ($\sum \text{Debits} = \sum \text{Credits}$).
- Assigned developer receives read-only GitHub token valid strictly for assigned repository.
- Client approval releases escrow, allocating 20% to platform and 80% to developer balance.

### Definition of Done
- Complete end-to-end marketplace flow successfully demonstrated from ticket to payout report; PR merged.

### Unit Tests
- `test_ledger_double_entry_balance_invariant()`
- `test_commission_split_exact_math()`
- `test_quote_status_transitions()`

### Integration Tests
- `test_full_marketplace_lifecycle_transaction()`
- `test_scoped_github_token_dispenser()`

### End-to-End Tests
- Full multi-role Playwright test: Shop Owner requests deployment $\to$ Admin assigns Developer $\to$ Developer quotes $\$30$ $\to$ Owner pays $\to$ Developer marks live $\to$ Owner confirms $\to$ Ledger balances.

### Manual Testing Checklist
- [ ] Open 3 browser windows: Client, Developer, Admin.
- [ ] Request deployment as Client; assign Developer as Admin.
- [ ] Send message in workroom; verify real-time arrival in both windows.
- [ ] Submit quote as Developer; pay quote as Client.
- [ ] Inspect `ledger_entries` table in database; verify debits equal credits to the exact cent.

### Regression Tests
- Re-run all previous phase test suites.

### Rollback Strategy
- Transactions wrap all ledger operations; failure triggers immediate rollback without partial state.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Race conditions during concurrent payment confirmation releasing escrow twice.
- *Mitigation:* `SELECT ... FOR UPDATE` row-level locks on `deployment_requests` and `payments`.

### Future Improvements
- Safepay / JazzCash live gateway integration for Pakistani market.
