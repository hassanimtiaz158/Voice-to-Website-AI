# Future Roadmap: Post-FYP Evolution & Commercialization
## Long-Term Vision: From Final Year Project to Scalable SaaS Venture

---

### Document Metadata
- **Document Version:** 2.0.0
- **Status:** APPROVED & LOCKED
- **Horizon:** 12 to 24 Months Post-Graduation

---

## 1. Post-FYP Evolution Horizon

While the 16-week Final Year Project delivers a hardened, production-ready system for static component-driven websites (`vite-react-tailwind`), the long-term architectural vision scales into a complete autonomous software agency.

```
       [FYP Scope: Pinned React + HITL Deployment]
                           │
                           ▼ Post-Graduation Phase 1
       [Next.js Full-Stack + Automated Custom Domains]
                           │
                           ▼ Post-Graduation Phase 2
       [Direct Local Payments (Safepay / Raast) + AI WhatsApp Bot]
                           │
                           ▼ Post-Graduation Phase 3
       [Autonomous Full-Stack Engineering Agency with Mobile Apps]
```

---

## 2. Advanced Future Phases

### Phase 21: Next.js Full-Stack App Profiles (SSR, Server Actions & DB)
- **Objective:** Expand the Planner and Coder beyond static landing pages to full-stack applications with built-in database models and authentication.
- **Architecture:** Add `nextjs-app-router` scaffold profile.
- **Capabilities:**
  - Automated generation of Prisma schemas and SQLite/PostgreSQL migrations.
  - Server actions handling form submissions (e.g., customer contact forms, appointment booking).
  - Integration with serverless database providers (Neon Postgres / Turso).

### Phase 22: Automated Custom Domain Binding & Caddy Reverse Proxy
- **Objective:** Eliminate human domain configuration for standard domains by introducing automated DNS verification and reverse-proxy binding.
- **Architecture:**
  - Caddy Server integration via dynamic REST API (`/config/apps/http/servers/`).
  - Automated ACME HTTP-01 challenge issuance for arbitrary client custom domains (`www.tariqshoes.pk`).
  - Automated Cloudflare DNS record management via Cloudflare API.

### Phase 23: Production Pakistani Payment Gateway (Safepay & Raast)
- **Objective:** Transition from mock escrow gateway to real financial settlement in Pakistan.
- **Architecture:**
  - Safepay Checkout integration for Visa/Mastercard processing.
  - SBP Raast P2M (Person-to-Merchant) instant QR code payment rails.
  - JazzCash and EasyPaisa mobile wallet webhooks.
  - Automated 1Link IBFT bank transfer API for monthly developer balance payouts.

### Phase 24: Direct Conversational Urdu Speech Synthesis (TTS)
- **Objective:** Provide natural, conversational spoken voice responses in Urdu so non-literate shop owners can have a complete voice-in, voice-out diagnostic experience.
- **Architecture:**
  - Fine-tuned Coqui TTS / VITS model trained on native Pakistani Urdu speech corpora.
  - Low-latency edge inference via ONNX WebAssembly or GPU streaming endpoint.

### Phase 25: AI WhatsApp Business Bot Ingestion
- **Objective:** Allow merchants to build and edit websites without opening a desktop browser, operating 100% inside WhatsApp.
- **Architecture:**
  - Meta Cloud API / WhatsApp Business API webhook receiver.
  - Voice notes recorded in WhatsApp forwarded directly to Whisper ASR pipeline.
  - Clarifier questions rendered as interactive WhatsApp List and Reply Buttons.
  - Live preview links and screenshot snapshots delivered directly in the WhatsApp chat.

### Phase 26: Multi-Region Firecracker MicroVM Pooling
- **Objective:** Reduce sandbox cold-start latency from 8 seconds to $<500\text{ ms}$ for global users.
- **Architecture:**
  - Deploy custom Firecracker microVM orchestrator across 3 edge regions (Europe, Middle East, Asia).
  - Maintain a pre-warmed pool of running Linux microVMs with pre-mounted node_modules.

---

## 3. Commercialization & Unit Economics at Scale

```
Target Pricing Model:
• Free Tier: 1 site, 5 edits/month, platform subdomain (e.g., store.voicetoai.site).
• Pro Plan ($12/month / PKR 3,500/month): Unlimited edits, custom domain, priority build queue.
• Marketplace Commission: 20% flat fee on developer deployment gigs ($30 - $100 avg ticket size).

Projected Margins at 1,000 Active Merchants:
• Total Revenue: ~$18,000 / month
• Cloud Infrastructure & MicroVMs: ~$1,400 / month
• LLM Token API Spend (Claude 3.5 Sonnet + Haiku with prompt caching): ~$2,800 / month
• Net Operating Margin: ~76%
```
