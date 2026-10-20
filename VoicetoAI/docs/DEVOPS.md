# DevOps Strategy & Infrastructure Operations
## Containerization, Reverse Proxy, SSL Automation, Secrets Management & Disaster Recovery

---

### Document Metadata
- **Document Version:** 2.0.0
- **Status:** APPROVED & LOCKED
- **Standard:** Cloud-native architecture, infrastructure-as-code, and zero-trust security.

---

## 1. Production Topology & Service Mesh

The platform is deployed using production Docker containers managed via Docker Compose (with Kubernetes Helm chart migration specifications for horizontal scale).

```
                             Internet Traffic
                                    │
                                    ▼ Ports 80, 443
                        ┌───────────────────────┐
                        │ Traefik v3 Edge Proxy │ ◄── Let's Encrypt ACME SSL
                        │ (Reverse Proxy / TLS) │
                        └───────────┬───────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │ /api/*, /ws/*            │ /*                       │ /metrics
         ▼                          ▼                          ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│ FastAPI Backend  │       │ Next.js Frontend │       │ Prometheus       │
│ (3 Replicas)     │       │ (2 Replicas)     │       │ (Metrics Ingest) │
└────────┬─────────┘       └──────────────────┘       └────────┬─────────┘
         │                                                     │
         ├──────────────────────────┐                          ▼
         ▼                          ▼                 ┌──────────────────┐
┌──────────────────┐       ┌──────────────────┐       │ Grafana          │
│ PostgreSQL 16    │       │ MinIO / S3       │       │ (Dashboards)     │
│ (+ pgvector)     │       │ (Object Storage) │       └──────────────────┘
└──────────────────┘       └──────────────────┘
```

---

## 2. Production Docker Configurations

### 2.1 Backend Multi-Stage Dockerfile (`deploy/Dockerfile.backend`)
```dockerfile
# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.3

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root --only main

# Final runtime stage
FROM python:3.12-slim AS runner

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Run as non-root user
RUN addgroup --system appgroup && adduser --system --group appuser

COPY --from=builder /app/.venv /app/.venv
COPY ./backend /app/backend
COPY ./contracts /app/contracts

USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 2.2 Frontend Standalone Dockerfile (`deploy/Dockerfile.frontend`)
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
RUN apk add --no-cache libc6-compat
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile

COPY frontend/ ./
ENV NEXT_TELEMETRY_DISABLED=1 \
    NODE_ENV=production
RUN pnpm build

# Runner stage
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000

CMD ["node", "server.js"]
```

---

## 3. Reverse Proxy & Automated SSL (Traefik v3)

```yaml
# deploy/docker-compose.prod.yml
version: '3.8'

services:
  traefik:
    image: traefik:v3.0
    restart: always
    command:
      - "--api.insecure=false"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.myresolver.acme.tlschallenge=true"
      - "--certificatesresolvers.myresolver.acme.email=${LETSENCRYPT_EMAIL}"
      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"
      - "traefik-certificates:/letsencrypt"

  backend:
    build:
      context: .
      dockerfile: deploy/Dockerfile.backend
    restart: always
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.backend.rule=Host(`${DOMAIN}`) && PathPrefix(`/api`, `/ws`)"
      - "traefik.http.routers.backend.entrypoints=websecure"
      - "traefik.http.routers.backend.tls.certresolver=myresolver"

  frontend:
    build:
      context: .
      dockerfile: deploy/Dockerfile.frontend
    restart: always
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.frontend.rule=Host(`${DOMAIN}`)"
      - "traefik.http.routers.frontend.entrypoints=websecure"
      - "traefik.http.routers.frontend.tls.certresolver=myresolver"

volumes:
  traefik-certificates:
```

---

## 4. Secrets Management & Invariant Security

1. **Principle of Least Privilege:** Production secrets are injected exclusively via environment variables or an enterprise secret manager (Infisical / HashiCorp Vault).
2. **Absolute Sandbox Isolation:** The sandbox container/microVM has **zero environment variable inheritance** from the parent host. API keys for Anthropic, OpenAI, GitHub, or Postgres are completely absent from the execution runtime.
3. **Automated Secret Scanning:** Git pre-commit hooks (`gitleaks`) and GitHub Actions push protection reject any commit containing API key signatures.

---

## 5. Automated Database Backup & Disaster Recovery

### 5.1 Encrypted Backup Script (`scripts/backup_db.sh`)
```bash
#!/usr/bin/env bash
set -euo pipefail

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="/tmp/backup_${TIMESTAMP}.sql.gz"
ENCRYPTED_FILE="${BACKUP_FILE}.enc"

echo "[*] Starting PostgreSQL Backup..."
pg_dump -h "${DB_HOST:-localhost}" -U "${DB_USER:-postgres}" -d "${DB_NAME:-voicetoai_db}" | gzip > "$BACKUP_FILE"

echo "[*] Encrypting with AES-256..."
openssl enc -aes-256-cbc -salt -pbkdf2 -in "$BACKUP_FILE" -out "$ENCRYPTED_FILE" -pass "env:BACKUP_ENCRYPTION_KEY"

echo "[*] Uploading to Offsite S3 Storage..."
aws s3 cp "$ENCRYPTED_FILE" "s3://${BACKUP_S3_BUCKET}/db_backups/backup_${TIMESTAMP}.sql.gz.enc"

rm -f "$BACKUP_FILE" "$ENCRYPTED_FILE"
echo "[+] Backup successfully completed and uploaded: backup_${TIMESTAMP}.sql.gz.enc"
```

### 5.2 One-Command Restore Script (`scripts/restore_db.sh`)
```bash
#!/usr/bin/env bash
set -euo pipefail

if [ -z "${1:-}" ]; then
  echo "Usage: ./restore_db.sh <backup_filename.sql.gz.enc>"
  exit 1
fi

TARGET_ENCRYPTED="$1"
LOCAL_ENCRYPTED="/tmp/restore_target.enc"
DECRYPTED_SQL="/tmp/restore_target.sql"

echo "[*] Downloading backup from S3..."
aws s3 cp "s3://${BACKUP_S3_BUCKET}/db_backups/${TARGET_ENCRYPTED}" "$LOCAL_ENCRYPTED"

echo "[*] Decrypting archive..."
openssl enc -d -aes-256-cbc -pbkdf2 -in "$LOCAL_ENCRYPTED" -out "${DECRYPTED_SQL}.gz" -pass "env:BACKUP_ENCRYPTION_KEY"

gunzip "${DECRYPTED_SQL}.gz"

echo "[*] Restoring into PostgreSQL database..."
psql -h "${DB_HOST:-localhost}" -U "${DB_USER:-postgres}" -d "${DB_NAME:-voicetoai_db}" < "$DECRYPTED_SQL"

rm -f "$LOCAL_ENCRYPTED" "$DECRYPTED_SQL"
echo "[+] Database restore complete!"
```
