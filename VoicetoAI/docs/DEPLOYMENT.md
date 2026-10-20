# Deployment Strategy & Production Infrastructure Plan
## Cloud Topology, Zero-Downtime Rollouts, Preview Hosting & Disaster Recovery

---

### Document Metadata
- **Document Version:** 2.0.0
- **Status:** APPROVED & LOCKED
- **Audience:** DevOps Engineers, Platform Administrators & Site Reliability Team

---

## 1. Cloud Architecture & Target Infrastructure

The platform is designed to run efficiently on cost-effective cloud virtual machines (e.g., Hetzner Cloud, DigitalOcean, or AWS EC2) fronted by automated edge proxies.

```
                                Cloudflare DNS & CDN
                                (Proxied / Anti-DDoS)
                                         │
                                         ▼ Port 443
                        ┌─────────────────────────────────┐
                        │ Edge Server (Ubuntu 24.04 LTS)  │
                        │ 4 vCPU, 16 GB RAM, 200 GB NVMe  │
                        ├─────────────────────────────────┤
                        │ Traefik v3 (Let's Encrypt SSL)  │
                        ├────────────────┬────────────────┤
                        │ Backend (3x)   │ Frontend (2x)  │
                        ├────────────────┴────────────────┤
                        │ PostgreSQL 16 + pgvector        │
                        │ MinIO / Cloudflare R2           │
                        └─────────────────────────────────┘
                                         │
                                         ▼ Dedicated Egress
                        ┌─────────────────────────────────┐
                        │ E2B Firecracker Cloud Sandboxes │
                        └─────────────────────────────────┘
```

---

## 2. Preview Environment Architecture

A core platform capability is providing the non-technical shop owner with an instant, interactive live preview of their generated website.

### Preview Serving Strategy:
1. **Immediate Visual Preview (0 to 3 seconds):** The moment Playwright finishes verification in the sandbox, a full-page PNG screenshot is uploaded to S3 and displayed in the client UI preview viewport. This eliminates loading delays.
2. **Interactive Hydrated Preview (3 to 8 seconds):**
   - The compiled static production build (`/dist` directory) is served directly from an isolated static host container or uploaded to an S3/R2 bucket configured for static web hosting.
   - Preview URL Format: `https://preview-{project_id_prefix}-{version_n}.preview.voicetoai.com`
   - Sandboxed Iframe Security: The client embeds the preview within an `<iframe>` configured with strict sandboxing:
     ```html
     <iframe 
       src="https://preview-..."
       sandbox="allow-scripts allow-same-origin allow-forms"
       csp="default-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts.gstatic.com;"
     ></iframe>
     ```

---

## 3. Zero-Downtime Rolling Deployment Protocol

To deploy new versions of the platform without interrupting active voice streams or background agent builds:

```mermaid
sequenceDiagram
    autonumber
    participant CD as GitHub Actions CD
    participant Host as Production VPS
    participant Proxy as Traefik v3
    participant AppOld as Backend Container (V1)
    participant AppNew as Backend Container (V2)

    CD->>Host: SSH trigger deployment script
    Host->>Host: Pulls newest container image from ghcr.io
    Host->>Host: Executes database migrations: `alembic upgrade head`
    Host->>AppNew: Starts new backend instance on dynamic port
    
    loop Health Check Verification
        Host->>AppNew: Pings http://localhost:PORT/healthz
        AppNew-->>Host: Returns 200 OK
    end

    Host->>Proxy: Updates routing label to point traffic to AppNew
    Proxy->>AppNew: Routes all incoming requests to AppNew
    Host->>AppOld: Sends SIGTERM; allows 30-second drain for active WebSockets
    Host->>AppOld: Stops and removes old container V1
```

---

## 4. Hardware Sizing & Capacity Planning

| Component | Minimum Dev Spec | Production Spec (100 Active Users) | Scaling Strategy |
|---|---|---|---|
| **API Gateway / Backend** | 1 vCPU, 2 GB RAM | 4 vCPU, 8 GB RAM (3 Replicas) | Horizontal scaling behind Traefik |
| **Next.js Web Client** | 1 vCPU, 1 GB RAM | 2 vCPU, 4 GB RAM (2 Replicas) | Horizontal scaling |
| **PostgreSQL 16 + Vector** | 1 vCPU, 2 GB RAM | 4 vCPU, 16 GB RAM | Dedicated NVMe storage + PgBouncer |
| **Sandbox Execution** | Local Docker | E2B Cloud MicroVM Tier | Dynamic elastic microVM auto-scaling |
| **Object Storage** | Local MinIO | Cloudflare R2 / AWS S3 | Infinite scalable object storage |

---

## 5. Emergency Rollback Runbook

If a newly deployed container passes synthetic health checks but encounters edge-case runtime exceptions in production:

1. **Step 1: Revert Container Version Instantly**
   ```bash
   ssh deploy@prod.voicetoai.com
   cd /opt/voicetoai
   # Roll back docker-compose to previous pinned tag
   sed -i 's/backend:latest/backend:PREVIOUS_STABLE_SHA/g' deploy/docker-compose.prod.yml
   docker compose -f deploy/docker-compose.prod.yml up -d --no-deps backend
   ```
2. **Step 2: Database Migration Reversal (If schema altered)**
   ```bash
   docker compose exec backend alembic downgrade -1
   ```
3. **Step 3: Verification**
   ```bash
   curl -f https://voicetoai.com/api/healthz
   ```
