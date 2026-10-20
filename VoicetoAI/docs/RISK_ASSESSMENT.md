# Comprehensive Risk Assessment & Mitigation Matrix
## Voice-to-Website AI: Enterprise Platform Risk Register

---

### Document Metadata
- **Document Version:** 2.0.0
- **Status:** APPROVED & LOCKED
- **Audience:** FYP Evaluation Committee, Engineering Team & Project Mentors

---

## 1. Risk Register & Impact Matrix

| Risk ID | Risk Category | Risk Description | Probability | Severity | Mitigation Strategy | Contingency Plan |
|---|---|---|---|---|---|---|
| **RSK-01** | **AI / Quality** | Build pass rate falls below 85% target due to LLM hallucinations or syntax bugs. | Medium | Critical | Pinned scaffolds, strict single-file generation, strict TypeScript mode, and 3-retry Fixer loop. | Pinned fallback template components; prompt tuning on failing AST patterns. |
| **RSK-02** | **Cost / Loop** | Runaway Fixer loops or recursive agent chatter exploding token budget. | Medium | High | Hard ceiling of 300,000 tokens per run; LangGraph step limit of 25; targeted compiler stderr context. | Automatic quarantine to draft branch on 3rd failure; circuit breaker trips. |
| **RSK-03** | **Sandbox** | E2B Hobby microVM limits (2GB RAM OOM during Vite build or 1-hour session cap). | Medium | High | Pre-cached dependencies, `NODE_OPTIONS=--max-old-space-size=1536`, ephemeral VM teardown. | Local unprivileged Docker runner fallback with host volume mounts. |
| **RSK-04** | **RAG / Locator** | Locator identifies wrong file, causing Editor to apply diffs to unrelated modules. | Low | High | 3-signal hybrid retrieval (pgvector + BM25 + import graph); convention routing for text copy. | Editor can request 1 additional file; tsc catches cross-file breakage in sandbox. |
| **RSK-05** | **ASR / Audio** | High Word Error Rate (WER) on regional Pakistani Urdu or heavy English accents. | Medium | Medium | Domain-specific priming prompt injection; mandatory transcript confirmation modal. | Shop owner can edit transcript in modal before agent graph invocation. |
| **RSK-06** | **Security** | Malicious prompt attempting to escape sandbox or exfiltrate platform API keys. | Low | Critical | Firecracker microVM hypervisor isolation; zero platform secrets in sandbox; strict egress firewall. | Kill running microVM immediately; blacklist user account. |
| **RSK-07** | **Regulatory** | Payment gateway legal compliance and merchant registration issues in Pakistan. | High | High | Scope isolated to mock gateway and double-entry ledger; zero real banking integrations in MVP. | Safepay gateway integration deferred to post-launch commercial phase. |
| **RSK-08** | **GitHub API** | Rate limiting or token leaks via GitHub MCP server. | Low | High | Dedicated GitHub App with installation tokens; scoped 4-hour tokens for developers; single Committer node. | Fallback to writing tarball zip archives directly to S3. |
| **RSK-09** | **Timeline** | Team falls behind schedule across 16-week FYP timeline. | Medium | High | Strict prioritized cut line (cut static-html, vision judge, quotas, use polling). | Cut features cleanly without breaking sandbox verification or versioning. |
| **RSK-10** | **Presentation** | Live demo failure caused by LLM API outage during university final defense. | Medium | Critical | Seeded reproducible shop owner personas; pre-cached agent runs; offline backup demo video. | Switch to pre-recorded 4K backup demo video; explain architecture from code. |

---

## 2. In-Depth Mitigation Protocols

### 2.1 Mitigation for RSK-01 & RSK-02: Build Healing & Token Circuit Breaker
```python
# LangGraph Circuit Breaker Guard
def token_guard_condition(state: ProjectGraphState) -> str:
    cumulative_tokens = state.get("cumulative_tokens", 0)
    if cumulative_tokens > 250000:
        logger.error(f"Project {state['project_id']} approaching token ceiling: {cumulative_tokens}")
    if cumulative_tokens >= 300000:
        raise TokenBudgetExceededException("Hard run token ceiling of 300,000 exceeded")
    
    if state.get("fixer_retry_count", 0) >= 3:
        return "quarantine_failure_node"
    return "fixer_node"
```

### 2.2 Mitigation for RSK-05: Speech-to-Text Bilingual Priming
Pakistani colloquial language contains code-switching between Urdu grammar and English terminology (e.g., *"Mujhe header mein logo lagana hai aur WhatsApp checkout button chahiye"*).
- By providing Whisper with a 45-word retail lexicon prompt, phonetic errors drop significantly.
- By enforcing a UI confirmation modal, transcription errors never propagate into the agent planner.

### 2.3 Mitigation for RSK-07: Financial Scope Isolation
Attempting to handle real credit card processing or Pakistani local bank disbursements in an academic project creates massive regulatory, KYC, and chargeback exposure. 
- The platform uses a **Mathematical Double-Entry Ledger** (`ledger_entries`) that proves the financial soundness of the escrow model without processing real money.
- Developer payouts are calculated in monthly statements; simulated disbursements update ledger balances cleanly.
