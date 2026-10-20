# Feature Specification: Authentication, Authorization & Role-Based Access Control (RBAC)
## Multi-Tenant Security, Scoped Tokens, Rate Limiting & Access Boundaries

---

### Feature Metadata
- **Feature ID:** SPEC-005-AUTH-RBAC
- **Feature Owner:** Member 4 (Delivery and Business Lead)
- **Status:** APPROVED & LOCKED
- **Target Release:** Milestone M1 (Auth & Shell) & Milestone M4 (Marketplace RBAC)

---

## 1. Security Overview & Personas

The platform enforces strict multi-tenant isolation, cryptographically signed JWT sessions, and granular Role-Based Access Control (RBAC) across three distinct user roles:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ROLE-BASED ACCESS HIERARCHY                     │
├────────────────────────────────────────────────────────────────────────┤
│ 1. USER (Shop Owner / Client)                                          │
│    • Manage owned projects (create, voice/text prompt, trigger edits).  │
│    • View verified previews and GitHub repository commit history.      │
│    • Request live deployment, approve quotes, release escrow payments. │
├────────────────────────────────────────────────────────────────────────┤
│ 2. DEVELOPER (Verified Freelance Deployment Engineer)                  │
│    • View assigned deployment tickets and client specifications.       │
│    • Access scoped, temporary, read-only GitHub repository tokens.     │
│    • Chat in dedicated project workrooms; submit deployment quotes.    │
│    • Mark site deployed; view monthly earnings and payout history.     │
├────────────────────────────────────────────────────────────────────────┤
│ 3. ADMIN (Platform Operations & FYP Supervisor)                        │
│    • Manage user accounts, role elevations, and subscription plans.    │
│    • Assign developers to incoming deployment tickets.                 │
│    • Audit token burn rate, Langfuse traces, and system error rates.   │
│    • Inspect double-entry ledger balance; approve developer payouts.   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Authentication Protocol & Session Management

### 2.1 Cryptographic Standards
- **Password Hashing:** Passwords hashed using `bcrypt` with work factor 12.
- **Access Tokens:** Short-lived JSON Web Tokens (JWT) signed with HMAC-SHA256 (`HS256`).
  - Validity: 60 minutes.
  - Claims: `sub` (User UUID), `role` (`user`, `developer`, `admin`), `exp`, `iat`.
- **Refresh Tokens:** Long-lived cryptographically secure random 256-bit hex strings stored hashed in PostgreSQL.
  - Validity: 30 days.
  - Revocable on logout or security breach.

### 2.2 JWT Payload Structure
```json
{
  "sub": "b2c9d8e7-1234-4567-89ab-cdef01234567",
  "email": "tariq.khan@example.com",
  "role": "user",
  "plan_id": "free_tier",
  "iss": "voicetowebsite-ai-auth",
  "iat": 1792348800,
  "exp": 1792352400
}
```

---

## 3. Scoped GitHub Token Dispenser

Freelance developers need access to project source code to configure custom domains and deploy live sites. However, exposing platform-level GitHub credentials or permanent repository access is unacceptable.

### Scoped GitHub Access Pattern:
1. When an Admin assigns a Developer to a `deployment_request`, the backend calls the GitHub App REST API.
2. The platform generates an **Installation Access Token** strictly scoped to:
   - Repository: Only the specific project repo (e.g., `org/proj-b2c9d8e7`).
   - Permissions: `contents: read` (read-only code access).
   - TTL: Token automatically expires in 4 hours.
3. The developer uses this token to clone the repository, run local verification, and wire the repo to Vercel/Cloudflare.

---

## 4. Tenant Isolation & Middleware Authorization

All FastAPI endpoints apply declarative dependency injection to ensure users can only read or mutate their own resources:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> UserModel:
    payload = decode_jwt(token)
    user = await db.get(UserModel, payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")
    return user

def require_role(allowed_roles: List[str]):
    def role_checker(current_user: UserModel = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return current_user
    return role_checker

async def verify_project_ownership(project_id: UUID, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    project = await db.get(ProjectModel, project_id)
    if not project or (project.owner_id != current_user.id and current_user.role != "admin"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project
```

---

## 5. Quota & Rate Limiting Enforcement

To protect AI token infrastructure from abuse, the platform enforces token and generation rate limits:
- **Free Tier:** 1 active project, 50,000 tokens/month, 5 surgical edits/month.
- **Pro Tier:** 10 active projects, 500,000 tokens/month, 50 surgical edits/month.
- **API Rate Limiting:** 60 requests per minute per IP address enforced via Redis token bucket.

---

## 6. Test Suite & Acceptance Criteria

### Unit Tests
- `test_password_hashing`: Verifies bcrypt salt generation and verification correctness.
- `test_jwt_expiration`: Confirms expired tokens return HTTP 401 Unauthorized.
- `test_role_rbac_rejection`: Asserts a `user` calling an `/api/v1/admin/*` endpoint receives HTTP 403 Forbidden.

### Security Integration Tests
- `test_tenant_isolation_leak`: Asserts User A cannot retrieve or modify Project B belonging to User B.
- `test_scoped_github_token`: Verifies generated installation token cannot write to repository or read other repos in organization.
