Markdown# Design Decisions, Trade-offs & Future Improvements

## 1. Core Technology Choices

| Area                  | Decision                         | Why This Choice                                                                 | Alternatives Considered & Why Rejected                                  |
|-----------------------|----------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| Framework             | Flask + Blueprint structure      | Mature, predictable, excellent documentation, minimal magic                     | FastAPI (async complexity, Pydantic v2 breaking changes), Django (too heavy) |
| Database              | PostgreSQL 16                    | Full ACID, excellent JSON support, battle-tested in fintech                     | MySQL (weaker consistency), SQLite (not production-safe), MongoDB (no transactions) |
| ORM & Migrations      | SQLAlchemy + Alembic             | Industry standard combo, powerful query builder, safe migrations                | Raw psycopg2 (too verbose), Peewee (limited features)                    |
| Containerization      | Docker + multi-stage Dockerfile  | Guarantees identical dev/prod environments, easy onboarding                     | Podman (less ecosystem), bare metal (drift risk)                         |
| Production Server     | Gunicorn + Nginx                 | Proven, stable, excellent performance for Flask                                 | uvicorn (not needed), waitress (Windows-only focus)                      |
| Deployment Platform   | Render.com (from GHCR)           | Zero ops, free HTTPS, auto-deploys in <60s, generous free tier                  | Railway (good), Fly.io (complex), AWS ECS (overkill & costly)            |
| CI/CD                 | GitHub Actions + GHCR + Trivy    | Native integration, free minutes, SARIF upload to Security tab                  | GitLab CI (not using GitLab), CircleCI (paid)                            |
| Security Scanning     | Trivy (aquasecurity/trivy-action)| Fully open-source, fast, reliable SARIF output, no account needed               | Snyk (freemium), Grype (less mature SARIF support)                       |

**Result**: Fast development velocity with zero compromise on production reliability and security.

## 2. Key Architectural Decisions

- **Monolith (not microservices)**  
  → Scope is small and cohesive. Splitting would add complexity with no benefit.

- **Nginx as reverse proxy**  
  → Terminates TLS, serves future static assets, hides Gunicorn workers.

- **Database migrations via Alembic**  
  → Zero-downtime schema changes in production (critical for financial data).

- **Full integration tests (not just unit)**  
  → Start real Flask + PostgreSQL in CI → guarantees the entire stack works.

- **Fail CI on CRITICAL/HIGH vulnerabilities**  
  → Prevents shipping known-exploitable images (non-negotiable in fintech).

## 3. What I Would Improve With More Time

| Priority | Improvement                                 | Estimated Effort | Impact |
|----------|---------------------------------------------|------------------|--------|
| High     | Add JWT authentication + role-based access  | 1–2 days         | Production security |
| High     | OpenAPI/Swagger UI (`flask-spectacular` or `drf-spectacular`) | 4–6 hours | Developer experience |
| High     | Rate limiting (`flask-limiter`)             | 2 hours          | Abuse protection |
| Medium   | Redis caching for `/api/stats`              | 1 day            | Performance at scale |
| Medium   | Admin panel (Flask-Admin or Django-like)    | 1 day            | Operations visibility |
| Medium   | Structured logging → ELK or Papertrail      | 2 days           | Observability |
| Low      | Prometheus metrics endpoint                 | 1 day            | Monitoring |
| Low      | Blue-green or canary deploys on Render      | 2 days           | Zero-downtime deploys |

## 4. Troubleshooting Guide

### Common Issues & Fixes

| Symptom                                      | Likely Cause                                | Fix |
|----------------------------------------------|---------------------------------------------|-----|
| `Connection refused` to `localhost:8000`    | API container not started                   | `docker compose up -d api` |
| `Database does not exist`                    | DB container started after API              | Depends_on + healthcheck + wait script, or run migrations again |
| `alembic: command not found`                 | Running command in wrong container          | Use `docker compose exec api alembic ...` |
| Tests fail with `ConnectionError` in CI      | Gunicorn not started or health check failed | Ensure `gunicorn ... --daemon` + wait loop in workflow |
| Trivy job red with telemetry error           | GitHub Actions bug                          | Add `permissions: { actions: write, security-events: write }` |
| Push to GHCR fails with "denied"             | Missing `packages: write` permission        | Add `permissions: { packages: write }` to push job |
| Render shows 502 / app not starting          | Wrong start command or missing env vars     | Render → Settings → Start Command: leave empty (uses Dockerfile) |

### How to Verify Everything Is Healthy

```bash
# 1. Local
docker compose ps                  # all services Up
curl http://localhost:8000/health # {"status": "ok"}
curl http://localhost:8000/api/stats

# 2. In CI
Check GitHub Actions → all jobs green → Security tab (Trivy results)

# 3. Production (Render)
Visit https://your-app.onrender.com/health
Check Render Logs →
