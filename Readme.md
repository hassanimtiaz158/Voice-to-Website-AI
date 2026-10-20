# Voice-to-Website AI

> Enterprise Autonomous Web Generation & Human Deployment Platform

[![CI](https://github.com/hassanimtiaz158/Voice-to-Website-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/hassanimtiaz158/Voice-to-Website-AI)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18.3-61DAFB.svg)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC.svg)](https://tailwindcss.com/)

---

## Overview

**Voice-to-Website AI** is an enterprise-grade autonomous software engineering SaaS platform. A non-technical shop owner describes their dream website in natural spoken voice (Urdu, English, or Roman Urdu) or text. An orchestrated multi-agent system conducts a diagnostic interview, extracts verified specifications, plans a bespoke architecture, generates real component-based code (`vite-react-tailwind`), compiles and executes the code inside a hardened, isolated sandbox, and runs automated visual and functional verification checks.

Every verified version is version-controlled via GitHub commits (`v1`, `v2`, ... `vN`). Subsequent modification requests use semantic file-manifest retrieval with pgvector to surgically locate and edit only the affected 1 to 3 files. When the business owner is ready to go live, the platform bridges the digital divide with a **Human-in-the-Loop (HITL) Marketplace**, connecting the client to verified developers via a dedicated escrow-backed workroom with an automated double-entry ledger.

---

## 3 Core Inviolable Laws

1. **Code Controls the Flow:** A deterministic LangGraph state machine governs execution routing. LLMs never decide the next state freely.
2. **Verify with Tools, Not Opinions:** A version is NEVER marked complete until sandbox TypeScript compilation, linting, production build, and Playwright smoke tests exit with code 0.
3. **Clarify Before Generating:** No code is written until the user explicitly confirms a structured requirements summary.

---

## Repository Structure

```
├── contracts/                             # Shared Pydantic V2 Data Schemas (Zero DB Dependencies)
│   ├── requirements.py                    # RequirementsContract & ColorPalette
│   ├── plan.py                            # PlanContract & FileAction
│   ├── build_result.py                    # BuildResultContract
│   ├── file_edit.py                       # FileEditContract & SingleFileDiff
│   ├── version_record.py                  # VersionRecordContract
│   └── deployment_request.py              # DeploymentRequestContract
│
├── backend/                               # Core FastAPI & Python Agentic Platform
│   ├── app/
│   │   ├── main.py                        # FastAPI entry point & CORS configuration
│   │   ├── core/                          # Settings & configurations
│   │   ├── models/                        # SQLAlchemy models
│   │   ├── schemas/                       # API Pydantic schemas
│   │   ├── agents/                        # Autonomous AI agents
│   │   └── sandbox/                       # MicroVM execution runner
│   └── tests/                             # Backend integration & unit tests
│
├── frontend/                              # Vite + React + Tailwind Web Client
│   ├── src/                               # Auth UI, chat streams, preview iframe
│   └── package.json
│
├── scaffolds/                             # Pinned Stack Templates for Greenfield Builds
│   └── vite-react-tailwind/               # Pinned Primary Stack Profile with data/site.json
│
├── evals/                                 # Automated FYP Evaluation Harness
├── deploy/                                # Production Infrastructure & Container Configs
├── scripts/                               # Maintenance & Operational Automation
└── VoicetoAI/docs/                        # Master Documentation Single Source of Truth
```

---

## Quickstart

### Running Backend Tests & Contracts

```bash
# Run contracts and backend test suite
pytest
```

### Running Backend Server

```bash
uvicorn backend.app.main:app --reload --port 8000
```

### Running Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Master Documentation

Comprehensive architectural blueprints and specifications are documented in [`VoicetoAI/docs/`](./VoicetoAI/docs/README.md).
