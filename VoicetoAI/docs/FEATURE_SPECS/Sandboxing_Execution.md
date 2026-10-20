# Feature Specification: Sandboxed Build Execution & Verification Engine
## Isolated MicroVM Execution, Pre-Cached Dependencies, Playwright Testing & Self-Healing

---

### Feature Metadata
- **Feature ID:** SPEC-004-SANDBOX
- **Feature Owner:** Member 2 (Generation Engine Lead) & Member 4 (Verifier Lead)
- **Status:** APPROVED & LOCKED
- **Target Release:** Milestone M0 (Spike) & Milestone M1 (Production Build Engine)

---

## 1. Objective & Security Model

Executing untrusted AI-generated JavaScript/TypeScript code is an existential security threat to SaaS infrastructure. The platform requires absolute execution isolation to prevent host compromises, data exfiltration, or cryptographic mining.

### Core Security Invariants:
1. **Hypervisor-Level MicroVM Isolation:** Build execution runs inside ephemeral microVMs using **E2B** (powered by Firecracker). During local offline development, a strictly unprivileged Docker container with drop-all Linux capabilities (`--cap-drop=ALL`) serves as a fallback.
2. **Zero Credentials in Sandbox:** Under no circumstances are database credentials, GitHub tokens, or cloud API keys injected into the microVM environment.
3. **Egress Firewall Enforcement:** Outbound TCP traffic is restricted exclusively to port 443 for `registry.npmjs.org` and approved CDN asset origins. Local host network (`127.0.0.1`, `10.0.0.0/8`, `192.168.0.0/16`) is completely blackholed.
4. **Hardware & Execution Caps:**
   - Compute: Exactly 2 vCPU.
   - Memory: 2,048 MB RAM (OOM-killer terminates runaway processes).
   - Timeout: Hard deadline of 300 seconds (5 minutes) per build execution.

---

## 2. Five-Stage Verification Pipeline

The sandbox executes a deterministic multi-stage build and audit sequence:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        SANDBOX EXECUTION PIPELINE                      │
├────────────────────────────────────────────────────────────────────────┤
│ Stage 1: File Injection                                                │
│ Injects generated files or applies unified diffs over base template    │
├────────────────────────────────────────────────────────────────────────┤
│ Stage 2: Dependency Hydration                                          │
│ Executes `npm ci --prefer-offline` from pre-cached /root/.npm storage  │
├────────────────────────────────────────────────────────────────────────┤
│ Stage 3: Strict Static Analysis & Type Checking                       │
│ Executes `npx tsc --noEmit` and `npm run lint`                         │
├────────────────────────────────────────────────────────────────────────┤
│ Stage 4: Production Compilation                                        │
│ Executes `npm run build` (Vite compiles static assets to /dist)        │
├────────────────────────────────────────────────────────────────────────┤
│ Stage 5: Playwright Headless Verification                              │
│ Boots `npm run preview` -> Playwright audits DOM, console errors,      │
│ layout overflow -> Captures full-page visual screenshot                │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Dependency Pre-Caching Strategy

Cold `npm install` runs take 45–75 seconds, destroying interactive user experience. To achieve $<12\text{ s}$ build times, the platform utilizes **Pre-Baked Base Images**:
1. Base template repository (`scaffolds/vite-react-tailwind`) is maintained with pinned `package.json` and `package-lock.json`.
2. The E2B microVM template image pre-installs all required dependencies (`react`, `react-dom`, `lucide-react`, `tailwindcss`, `vite`, `typescript`, `@types/react`) into `/root/.cache/node_modules`.
3. When a new sandbox instantiates, the system symlinks or quickly copies the pre-cached `node_modules`, reducing `npm ci` overhead to $< 2\text{ seconds}$.

---

## 4. Self-Healing Integration with Fixer Node

When a compiler error or test failure occurs, the Sandbox Engine captures structured diagnostic telemetry:

```python
class SandboxExecutionReport(BaseModel):
    success: bool
    stage_failed: Optional[Literal["TSC", "LINT", "BUILD", "PLAYWRIGHT"]]
    exit_code: int
    raw_stderr: str
    failing_files: List[str]
    suggested_action: str
```

### Self-Healing Logic:
1. **Error Extraction:** Regex extracts exact file paths and line numbers from TypeScript and ESLint error output (e.g., `src/components/Navbar.tsx:14:5 - error TS2304: Cannot find name 'LucideIcon'`).
2. **Context Window Protection:** Only the raw error trace and the specific failing files are delivered to the Fixer Agent. Working files are omitted to protect the token budget.
3. **Retry Budget:** The Fixer gets up to 3 repair attempts. If `retry_count == 3` and tests still fail:
   - The build attempt is quarantined on a `draft/failed-vN` branch.
   - Main branch remains strictly clean.
   - User is informed with a friendly message explaining what could not be built.

---

## 5. Visual & Functional Auditing with Playwright

Once Vite compiles the site, the sandbox launches a local preview server on port `4173` and executes headless Playwright smoke tests:

```typescript
// tests/smoke.spec.ts
import { test, expect } from '@playwright/test';

test('Smoke Audit: Site loads, zero console errors, zero layout overflow', async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });

  await page.goto('http://localhost:4173', { waitUntil: 'networkidle' });

  // 1. Assert Title Exists
  await expect(page).toHaveTitle(/./);

  // 2. Assert Zero Uncaught Console Errors
  expect(consoleErrors).toHaveLength(0);

  // 3. Assert Zero Horizontal Layout Overflow
  const hasHorizontalScroll = await page.evaluate(() => {
    return document.documentElement.scrollWidth > window.innerWidth;
  });
  expect(hasHorizontalScroll).toBeFalsy();

  // 4. Capture Full Page Snapshot
  await page.screenshot({ path: '/tmp/artifacts/preview.png', fullPage: true });
});
```

---

## 6. Acceptance Criteria & Benchmarks

1. **Build Success Target:** Greenfield generation must build and pass smoke tests on $\ge 85\%$ of 30 standard benchmark prompts within $\le 3$ fix retries.
2. **Execution Latency:** Clean build with pre-cached dependencies must complete in $\le 25\text{ seconds}$ total.
3. **Memory Safety:** Memory spikes exceeding 2,048 MB must trigger graceful SIGKILL without hanging the parent backend.
4. **Screenshot Availability:** Every verified version must produce a full-page PNG screenshot stored in S3 within 5 seconds of build completion.
