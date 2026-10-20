# CI/CD Pipeline Strategy: Voice-to-Website AI
## Automated Verification Gates, Multi-Stage Testing & Zero-Downtime Deployment

---

### Document Metadata
- **Document Version:** 2.0.0
- **Status:** APPROVED & LOCKED
- **Tooling:** GitHub Actions, Docker Buildx, Testcontainers, SSH Deployment

---

## 1. CI/CD Architecture Overview

The CI/CD pipeline enforces strict automated quality gates. No pull request can merge to `main` without passing contract validation, type safety, security scans, and integration tests.

```
 [Developer PR] ──► [Stage 1: Lint & Types] ──► [Stage 2: Contracts]
                                                       │
 [Merge to main] ◄── [Stage 4: Security] ◄── [Stage 3: Integration]
        │
        ▼
 [CD Workflow] ──► [Buildx Multi-Stage] ──► [GHCR Registry] ──► [VPS Deploy] ──► [Health Check]
```

---

## 2. GitHub Actions CI Workflow (`.github/workflows/ci.yml`)

```yaml
name: Continuous Integration (CI)

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  lint-and-typecheck:
    name: 1. Code Quality & Type Gates
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install Python Linters
        run: pip install black flake8 mypy poetry

      - name: Python Lint & Type Check
        run: |
          black --check backend contracts
          flake8 backend contracts --max-line-length=120
          mypy backend contracts --ignore-missing-imports

      - name: Set up Node.js 20
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"
          cache-dependency-path: frontend/pnpm-lock.yaml

      - name: Install pnpm
        run: npm install -g pnpm

      - name: Frontend Lint & TypeScript Check
        run: |
          cd frontend
          pnpm install --frozen-lockfile
          pnpm lint
          pnpm exec tsc --noEmit

  contract-validation:
    name: 2. Cross-Slice Contract Integrity
    needs: lint-and-typecheck
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install poetry && poetry install --with dev
      - name: Run Contract Tests
        run: poetry run pytest contracts/tests/

  integration-testing:
    name: 3. Integration & Database Tests
    needs: contract-validation
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_DB: voicetoai_test
          POSTGRES_PASSWORD: testpassword
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install poetry && poetry install --with dev
      - name: Run Database Migrations
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:testpassword@localhost:5432/voicetoai_test
        run: poetry run alembic upgrade head

      - name: Execute Integration Test Suite
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:testpassword@localhost:5432/voicetoai_test
          SANDBOX_PROVIDER: docker
        run: poetry run pytest backend/tests/integration/

  security-scan:
    name: 4. Vulnerability & Secret Scanning
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Gitleaks Secret Audit
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - name: Trivy Dependency Vulnerability Scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          severity: 'CRITICAL,HIGH'
```

---

## 3. GitHub Actions CD Workflow (`.github/workflows/cd.yml`)

```yaml
name: Continuous Deployment (CD)

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    name: Build Containers & Deploy to Production
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build & Push Backend Container
        uses: docker/build-push-action@v5
        with:
          context: .
          file: deploy/Dockerfile.backend
          push: true
          tags: ghcr.io/${{ github.repository }}/backend:latest,ghcr.io/${{ github.repository }}/backend:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Build & Push Frontend Container
        uses: docker/build-push-action@v5
        with:
          context: .
          file: deploy/Dockerfile.frontend
          push: true
          tags: ghcr.io/${{ github.repository }}/frontend:latest,ghcr.io/${{ github.repository }}/frontend:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Deploy to Production VPS via SSH
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /opt/voicetoai
            docker compose -f deploy/docker-compose.prod.yml pull
            docker compose -f deploy/docker-compose.prod.yml up -d --remove-orphans
            docker image prune -af --filter "until=72h"

      - name: Verify Live Health Endpoint
        run: |
          sleep 15
          curl -f https://${{ secrets.PROD_DOMAIN }}/api/healthz || exit 1
```
