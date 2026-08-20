# ReachOut

> Find companies. Find the right person. Reach out.

ReachOut is a global company discovery and outreach intelligence platform for proactive job seekers. It helps users discover companies beyond traditional job boards, identify relevant decision-makers, understand opportunity signals, and create targeted outreach.

## MVP

- Global company discovery
- Company intelligence and source provenance
- Founder, CTO and engineering-lead discovery from public sources
- Job and hiring-signal discovery
- Candidate-to-company matching
- Personalized outreach drafting

## Architecture

- **Frontend:** React + Vite
- **Backend:** Python + FastAPI
- **Database:** PostgreSQL
- **Search:** provider abstraction, starting with Brave Search
- **AI:** pluggable LLM service
- **Infrastructure:** Docker → Terraform/AWS
- **CI/CD:** GitHub Actions

See [`docs/architecture.md`](docs/architecture.md) for the initial architecture.

## Development

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API health check: `http://localhost:8000/api/health`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### PostgreSQL

```bash
docker compose up -d postgres
```

## Data principle

ReachOut uses the public web as a discovery and update layer, while its own database becomes the user's searchable opportunity layer. Sources and verification timestamps should be retained so information can be checked and refreshed.

## Status

**Phase 1 — Project scaffold in progress.**
