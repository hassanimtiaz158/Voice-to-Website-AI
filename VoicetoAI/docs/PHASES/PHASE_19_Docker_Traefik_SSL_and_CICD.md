# Phase 19: Containerization, Reverse Proxy, SSL & Production CI/CD Pipeline

---

### Navigation
- **Current Phase:** Phase 19 of 20
- **Previous Phase:** [Phase 18: Observability, Langfuse Tracing & Full Benchmark Evaluation Suite](file:///d:/VoicetoAI/docs/PHASES/PHASE_18_Observability_and_Eval_Suite.md)
- **Next Phase:** [Phase 20: System Hardening, Load Testing, Disaster Recovery & Final FYP Delivery](file:///d:/VoicetoAI/docs/PHASES/PHASE_20_Hardening_Recovery_and_Ship.md)
- **Master Guide:** [00_START_HERE_PHASE_GUIDE.md](file:///d:/VoicetoAI/docs/00_START_HERE_PHASE_GUIDE.md)
- **Related Specs:** [DEVOPS.md](file:///d:/VoicetoAI/docs/DEVOPS.md), [CICD.md](file:///d:/VoicetoAI/docs/CICD.md), [DEPLOYMENT.md](file:///d:/VoicetoAI/docs/DEPLOYMENT.md)

---

### Objective
Containerize the entire platform with production multi-stage Dockerfiles, Traefik reverse proxy, automated Let's Encrypt SSL, and complete GitHub Actions CI/CD deployment pipelines.

### Business Goal
Achieve production readiness with zero-downtime deployments, high availability, and automated testing gates preventing broken code from reaching production.

### Technical Goal
Author production `Dockerfile.backend` and `Dockerfile.frontend`, configure Traefik with automated ACME SSL, and build GitHub Actions workflows for continuous integration and continuous deployment.

### Features Included
- Production multi-stage Dockerfiles for Next.js frontend and FastAPI backend.
- `docker-compose.prod.yml` with Traefik v3 reverse proxy and SSL automation.
- GitHub Actions CI workflow: linting, contract validation, unit tests, integration tests.
- GitHub Actions CD workflow: automated container build, push to registry, and SSH deployment to production server.

### Features NOT Included
- Multi-region disaster recovery replication (Phase 20).

### Dependencies
- All previous phases (Phases 1 to 18).

### Deliverables
- `deploy/Dockerfile.frontend`.
- `deploy/Dockerfile.backend`.
- `deploy/docker-compose.prod.yml`.
- `.github/workflows/ci.yml` and `.github/workflows/cd.yml`.

### Architecture Changes
- System deployed in fully containerized production topology fronted by Traefik edge router.

### Database Changes
- None.

### API Changes
- None.

### Frontend Changes
- Optimized production build bundle (`output: 'standalone'`).

### Backend Changes
- Production Uvicorn worker process configuration with Gunicorn process manager.

### ML Changes
- None.

### Infrastructure Changes
- Cloud VPS (Ubuntu 24.04 LTS), DNS A-records pointing to server IP, port 80/443 exposed.

### Configuration Required
- Domain name, Let's Encrypt email address, Docker registry credentials.

### Environment Variables
- `DOMAIN_NAME=voicetoai.com`
- `LETSENCRYPT_EMAIL=admin@voicetoai.com`
- `DOCKER_REGISTRY_USER=...`
- `DOCKER_REGISTRY_TOKEN=...`

### Third-party Services
- GitHub Actions, Docker Hub / GitHub Container Registry (GHCR), Let's Encrypt.

### Tasks
- [x] Task 19.1: Author multi-stage Dockerfile for Next.js frontend.
- [x] Task 19.2: Author multi-stage Dockerfile for FastAPI backend.
- [x] Task 19.3: Configure Traefik reverse proxy with automatic HTTPS SSL.
- [x] Task 19.4: Build GitHub Actions CI pipeline running full test suite on PRs.
- [x] Task 19.5: Build GitHub Actions CD pipeline deploying to production VPS.

### Subtasks
- Subtask 19.1.1: Ensure frontend Dockerfile uses non-root `nextjs` user.
- Subtask 19.4.1: Configure Docker-in-Docker service container for sandbox integration tests in CI.

### Acceptance Criteria
- Pushing to `main` triggers automated CI; if tests pass, CD builds containers and deploys.
- Accessing domain over HTTP automatically redirects to HTTPS with valid Let's Encrypt certificate.
- Frontend, Backend, Postgres, and MinIO restart cleanly on server reboot.

### Definition of Done
- Application deployed and running on live staging/production server with valid SSL; PR merged.

### Unit Tests
- `test_dockerfile_syntax_validation()`

### Integration Tests
- `test_production_docker_compose_up()`

### End-to-End Tests
- Automated synthetic health check pinging live production HTTPS endpoint.

### Manual Testing Checklist
- [ ] Visit `https://your-domain.com` in browser.
- [ ] Inspect SSL certificate in browser lock icon; verify Let's Encrypt authority.
- [ ] Create a project; verify voice recording and preview work over production HTTPS/WSS.

### Regression Tests
- Re-run all integration test suites.

### Rollback Strategy
- CD workflow retains previous container tag; one-click rollback script: `docker-compose -f docker-compose.prod.yml up -d --no-deps backend:previous`.

### Estimated Complexity
- High (4/5).

### Estimated Time
- 5 days.

### Risks
- Let's Encrypt rate limits triggered during domain configuration testing.
- *Mitigation:* Use Let's Encrypt Staging ACME server until domain configuration is verified.

### Future Improvements
- Kubernetes (K8s) deployment manifests using Helm charts for enterprise clustering.
