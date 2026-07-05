# Veloura AI Stylist

Veloura AI Stylist is a full-stack fashion automation platform that helps users curate products, generate AI-assisted outfits, render Pinterest-ready collage boards, and schedule publishing workflows.

## Stack

- Frontend: React, TypeScript, Tailwind CSS, Vite
- Backend: FastAPI, SQLAlchemy, Alembic, Celery, Redis
- Database: PostgreSQL
- Storage: AWS S3
- AI: OpenAI API with deterministic fallbacks
- Deployment: Docker and Docker Compose

## Repository Layout

```text
.
├── backend
├── frontend
├── infra
└── docker-compose.yml
```

## Quick Start

### 1. Environment

Copy the example files and fill in your secrets:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 2. Run With Docker Compose

```bash
docker compose up --build
```

Services:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

### 3. Local Development

Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Core Capabilities

- Product management with AI enrichment
- Outfit generation across multiple aesthetics
- Pinterest board metadata and collage generation job orchestration
- Pin scheduling, campaign planning, and analytics summaries
- Affiliate revenue tracking and keyword/caption generation scaffolding

## Testing

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
npm run build
```

## Notes

- OpenAI, Pinterest, and S3 integrations are implemented behind service abstractions so they can run with real credentials or graceful fallbacks during development.
- Docker is wired in the repository, but it was not executable in the current environment because the Docker CLI is unavailable here.

