Markdown# Flask Microloans API + PostgreSQL (Docker)

Production-ready REST API for managing microloan applications, built with Flask, SQLAlchemy, Alembic, and PostgreSQL.

**Live Demo**: https://dummy-branch-app.onrender.com/health  
**CI/CD**: Fully automated (tests → build → security scan → push → deploy)  
**Deployed automatically** on every push to `main`

## Features
- Full loan CRUD + statistics
- Alembic migrations
- Comprehensive test coverage (all endpoints)
- Docker + Docker Compose (dev & prod)
- GitHub Actions CI/CD with Trivy vulnerability scanning
- Auto-deploy to Render.com via GHCR

## Architecture Diagram
┌────────────────────┐       ┌─────────────────────┐
│   Client (Browser) │ HTTPS  │   Nginx (Reverse    │
└────────────────────┘ ───►   │   Proxy + TLS)      │
└─────────────────────┘
│
▼
┌─────────────────────┐
│ Flask API (Gunicorn)│
└─────────────────────┘
│
▼
┌─────────────────────┐
│   PostgreSQL 16     │
└─────────────────────┘
textIn production → GHCR image → Render.com (auto-deploy)

## Quick Local Start

```bash
# 1. Copy env
cp .env.example .env

# 2. Start everything
docker compose up -d --build

# 3. Run migrations
docker compose exec api alembic upgrade head

# 4. Seed dummy data (optional, idempotent)
docker compose exec api python scripts/seed.py

# 5. Test
curl http://localhost:8000/health
curl http://localhost:8000/api/loans
API available at http://localhost:8000 (or https://localhost:443 with Nginx)
API Endpoints



MethodURLDescriptionGET/healthHealth checkGET/api/loansList all loansGET/api/loans/<id>Get loan by IDPOST/api/loansCreate new loan (status: pending)GET/api/statsAggregated statistics
Example POST:
Bashcurl -X POST http://localhost:8000/api/loans \
  -H "Content-Type: application/json" \
  -d '{
    "borrower_id": "usr_india_999",
    "amount": 12000.50,
    "currency": "INR",
    "term_months": 6,
    "interest_rate_apr": 24.0
  }'




API available at http://localhost:8000 (or https://localhost:443 with Nginx)
API Endpoints



































MethodURLDescriptionGET/healthHealth checkGET/api/loansList all loansGET/api/loans/<id>Get loan by IDPOST/api/loansCreate new loan (status: pending)GET/api/statsAggregated statistics
Example POST:
Bashcurl -X POST http://localhost:8000/api/loans \
  -H "Content-Type: application/json" \
  -d '{
    "borrower_id": "usr_india_999",
    "amount": 12000.50,
    "currency": "INR",
    "term_months": 6,
    "interest_rate_apr": 24.0
  }'
Environment Variables (from .env.example)





















































VariableDescriptionDefault ValueRequiredFLASK_ENVFlask environmentdevelopmentYesDATABASE_URLFull PostgreSQL connection stringauto-generatedYesDB_USERDB usernamepostgresYesDB_PASSDB passwordpostgresYesDB_NAMEDatabase namemicroloansYesLOG_LEVELLogging levelINFONoPORTInternal API port8000No
CI/CD Pipeline (GitHub Actions)
Runs on every push and PR to main:

Spin up PostgreSQL service
Start Flask API with Gunicorn
Run full integration tests (all 5 endpoints + DB)
Build Docker image
Scan image with Trivy (fails on CRITICAL/HIGH vulnerabilities)
Push clean image to GitHub Container Registry (ghcr.io)
Render.com automatically pulls and deploys :latest

→ Zero manual deployment. Green pipeline = safe to ship.
Design Decisions & Trade-offs


















































AreaChoiceReason & Trade-offs ConsideredFrameworkFlask + Flask-RESTfulMature, simple, excellent for small-to-medium APIs. FastAPI considered but overkillDatabasePostgreSQL + SQLAlchemyACID compliance essential for money. MySQL/Mongo rejectedMigrationsAlembicIndustry standard, works perfectly with SQLAlchemyContainerizationDocker + docker-composeIdentical dev/prod environmentsProduction ServerGunicorn + NginxProven, stable, easy TLS terminationCI/CDGitHub Actions + GHCRFree, native, no extra accounts neededDeploymentRender.comFree tier, auto-HTTPS, zero server management, auto-deploySecurity ScanningTrivy (SARIF → GitHub)Open-source, fast, blocks critical vulns before deploy
Result: Maximum developer velocity with production-grade reliability and security.
Development
Bash# Run tests locally
pytest -vv

# Run linter
ruff check .

# Manual image build
docker build -t branch-loan-api .



Project Structure

DUMMY-BRANCH-APP-MAIN
> alembic
app
> routes
__init__.py
→ config.py
→ db.py models.py
schemas.py
docker\nginx
Dockerfile
✡nginx.conf
ssl.crt
ssl.key
scripts
→ seed.py
tests
test_basic.py
> venv
✡.env
✡ .env.dev
* .env.prod
❤ .env.staging
.gitignore
alembic.ini
docker-compose.yml
Dockerfile
℗ README.md
requirements.txt
wsgi.py
