# Phase 16: Authentication, Multi-Tenant RBAC & Quota Subscriptions

---

### Navigation
- **Current Phase:** Phase 16 of 20
- **Previous Phase:** [Phase 15: Surgical Editor Agent & Automated Version Diff Engine](file:///d:/VoicetoAI/docs/PHASES/PHASE_15_Surgical_Editor_and_Rollback.md)
- **Next Phase:** [Phase 17: Human-in-the-Loop Marketplace & Double-Entry Ledger Engine](file:///d:/VoicetoAI/docs/PHASES/PHASE_17_Marketplace_and_Escrow_Ledger.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [Authentication_RBAC.md](file:///d:/VoicetoAI/docs/FEATURE_SPECS/Authentication_RBAC.md), [TDD.md](file:///d:/VoicetoAI/docs/TDD.md)

---

### Objective
Deploy enterprise authentication, Role-Based Access Control (`user`, `developer`, `admin`), tenant project isolation, and subscription token quota management.

### Business Goal
Protect platform margins, monetize via Free/Pro subscription tiers, and prepare security boundaries for the freelance developer marketplace.

### Technical Goal
Implement JWT + Refresh token sessions, Bcrypt hashing, FastAPI security dependencies, and database-driven usage quota counters.

### Features Included
- User registration, login, and session refresh endpoints.
- Role-based authorization (`user`, `developer`, `admin`).
- Multi-tenant data isolation (users cannot view/edit other tenants' projects).
- Subscription quota enforcement middleware (checks monthly token caps before LLM runs).
- Daily usage counter updates in `usage_counters` table.

### Features NOT Included
- Live payment processing (Phase 17).

### Dependencies
- Phase 2 (Postgres Database), Phase 5 (API Gateway).

### Deliverables
- `backend/app/services/auth.py`.
- `backend/app/middleware/quota.py`.
- Frontend login, registration, and account settings pages.

### Architecture Changes
- All API and WebSocket routes protected by JWT authorization middleware.

### Database Changes
- Populates `users`, `subscriptions`, and `usage_counters` tables.

### API Changes
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/auth/me`

### Frontend Changes
- Login modal, sign-up flow, account navigation, and quota consumption meter in header.

### Backend Changes
- Security dependencies: `get_current_user`, `require_role`, `check_quota_available`.

### ML Changes
- None.

### Infrastructure Changes
- None.

### Configuration Required
- JWT secret key, token expiration times (Access: 60m, Refresh: 30d).

### Environment Variables
- `JWT_SECRET_KEY=super-secret-hex-key-change-in-prod`
- `JWT_ALGORITHM=HS256`

### Third-party Services
- None.

### Tasks
- [x] Task 16.1: Implement password hashing and JWT encoding/decoding.
- [x] Task 16.2: Build registration and login endpoints.
- [x] Task 16.3: Implement multi-tenant project ownership check dependency.
- [x] Task 16.4: Implement quota enforcement middleware checking monthly token burn.
- [x] Task 16.5: Build frontend authentication state provider and login forms.

### Subtasks
- Subtask 16.1.1: Configure `pwd_context` with bcrypt 12 rounds.
- Subtask 16.4.1: Write atomic SQL counter increment for `tokens_consumed`.

### Acceptance Criteria
- User cannot access or modify projects owned by another user (returns HTTP 404).
- User who exceeds monthly token quota receives HTTP 402 / friendly upgrade modal.
- Passwords stored in database are salt-hashed; plain text is never logged.

### Definition of Done
- Auth and quota security suite passes 100% of penetration and isolation tests; PR merged.

### Unit Tests
- `test_password_hashing_and_verification()`
- `test_jwt_signature_validation()`
- `test_quota_middleware_blocks_exhausted_plan()`

### Integration Tests
- `test_multi_tenant_isolation_enforcement()`
- `test_login_and_token_refresh_lifecycle()`

### End-to-End Tests
- Playwright test: register new account $\to$ login $\to$ create project $\to$ verify token counter increments.

### Manual Testing Checklist
- [ ] Create User A and User B.
- [ ] User A creates Project 1.
- [ ] Attempt to load Project 1 using User B's token; verify access is forbidden.
- [ ] Manually set User A's token usage to limit in database; assert next prompt is blocked by quota.

### Regression Tests
- Re-run all previous API tests with authorization headers attached.

### Rollback Strategy
- In emergency, set `BYPASS_QUOTA_CHECK=true` environment variable.

### Estimated Complexity
- Medium (3/5).

### Estimated Time
- 4 days.

### Risks
- Token leakage via client-side storage vulnerabilities.
- *Mitigation:* Store refresh tokens in `HttpOnly`, `SameSite=Strict`, `Secure` cookies.

### Future Improvements
- Social login (Google / GitHub OAuth).
