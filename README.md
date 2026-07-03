# TalentIQ-AI

TalentIQ-AI is an AI Career Operating System that provides deterministic resume and career intelligence, integrated coaching workflows, and mission-driven learning plans.

## Vision

Empower professionals with deterministic, trustworthy career advice and AI-augmented coaching so they can close skill gaps and land the right roles faster.

## Architecture

High-level components:
- Frontend: React (Vite) SPA with Tailwind UI and Mentor UX.
- Backend: Flask API providing Resume Parsing (TalentParse), Career Intelligence (TalentCore), Dashboard, and Mentor orchestration.
- AI Providers: Pluggable provider adapters (Groq in alpha) with deterministic fallback.
- Persistence: (Phase 7) PostgreSQL via SQLAlchemy and Alembic migrations.

```mermaid
flowchart LR
  A[User Browser] -->|HTTP| B(Frontend React SPA)
  B -->|REST| C(Flask API Backend)
  C --> D[TalentParse]
  C --> E[TalentCore]
  C --> F[Mentor Orchestrator]
  F --> G[AI Provider Adapter (Groq)]
  C --> H[(Postgres) - Phase 7]
```

## Frontend Setup

Prerequisites: Node.js + npm

Commands:

```bash
cd frontend (root)
npm install
npm run build
npm run dev
```

Routes:
- `/` Landing
- `/auth` Authentication
- `/dashboard` User dashboard (protected)
- `/talentcoach` TalentCoach Mentor workspace (protected)

## Backend Setup

Prerequisites: Python 3.11+, virtualenv

Commands:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:FLASK_APP='app'
flask run --reload --host=127.0.0.1 --port=5050
```

API Endpoints (alpha):
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/resumes/demo` (demo resume parsing)
- `POST /api/resumes/upload` (multipart file upload)
- `GET /api/dashboard/demo`
- `GET /api/mentor/health`
- `POST /api/mentor/chat`

## Environment Variables

- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `DATABASE_URL` (Postgres URL, Phase 7)
- `GROQ_API_KEY` (set to enable Groq provider)
- `GROQ_API_URL`
- `RATELIMIT_STORAGE_URL` (optional)

## Current Alpha Features

- Frontend Mentor UI (`TalentCoach`) and dashboard panels
- Deterministic resume & career intelligence (TalentParse & TalentCore demos)
- Mentor orchestration pipeline with deterministic fallback
- Groq provider adapter scaffold and health endpoint
- In-memory session/memory store for alpha
- Pytest integration for Mentor flows

## Future Roadmap

- Phase 7: PostgreSQL persistence + SQLAlchemy models + Alembic migrations (design in docs/phase7_db_design.md)
- CI pipeline (frontend build + backend tests)
- Production deployment (WSGI, secrets management, rate limiting infra)
- Add E2E automated tests for UI flows

---
Alpha release: stable for local evaluation and demo. See `docs/phase7_db_design.md` for Phase 7 persistence design.
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the Oxlint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and Oxlint's TypeScript related rules in your project.
