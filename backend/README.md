# TalentIQ-AI — Backend

Compact backend documentation intended for contributors, alpha testers, and early adopters. Written in an open-source style for a startup: clear, practical, and focused on getting the project running locally for Alpha validation and development.

---

## 1. Project overview

TalentIQ-AI is an explainable, deterministic Career Operating System built to help professionals and recruiters analyze resumes, generate career intelligence, and create actionable AI-driven missions. This repository contains the backend services powering the API, deterministic calculators (CareerIntel / TalentCore), the TalentParse resume intelligence pipeline, and demo in-memory persistence for fast alpha iteration.

Key goals for the backend:
- Deterministic, explainable scoring (no LLMs required by default).
- Developer-friendly run experience (SQLite fallback for local dev).
- Clear API surface for frontend integration and E2E demos.

## 2. Architecture

- Flask-based microservice with modular blueprints:
  - `auth` — registration, login, tokens
  - `dashboard` — mission control and UI payloads
  - `resume_pipeline` — TalentParse engine (validation → parsing → normalizer → orchestrator)
  - `career_intel` — deterministic calculators and orchestrator
- SQLAlchemy for persistence (PostgreSQL recommended in production; SQLite fallback for local dev)
- Rate limiting via `Flask-Limiter` and basic environment readiness checks at startup

## 3. Folder structure

- `app/` — main Flask application package
  - `auth/` — models, routes, services, schemas
  - `career_intel/` — calculators and orchestration
  - `dashboard/` — dashboard routes and services
  - `resume_pipeline/` — validators, parsers, normalizer, orchestrator, routes
  - `common/` — utils, logging
- `app.py` — very small health-check runner used in local dev
- `requirements.txt` — pinned Python dependencies

## 4. Technologies used

- Python 3.11+ (project developed with 3.11+ in mind)
- Flask 3.x
- Flask-SQLAlchemy
- Flask-Limiter
- Marshmallow (validation)
- pdfplumber, python-docx (deterministic parsers)
- PyJWT, bcrypt (authentication)
- python-dateutil
- psycopg2-binary (PostgreSQL adapter)

## 5. Required environment variables

- `DATABASE_URL` — PostgreSQL connection string (optional in dev; if unset, app falls back to SQLite)
- `JWT_SECRET_KEY` — secret for signing JWTs (default `change-me` if unset; set in production)
- `SECRET_KEY` — Flask secret (default `change-me` if unset)
- `JWT_ACCESS_TOKEN_EXPIRES` — seconds until access token expiry (default `900`)
- `JWT_REFRESH_TOKEN_EXPIRES` — seconds until refresh token expiry (default `2592000`)
- `RATELIMIT_STORAGE_URL` — Flask-Limiter storage (defaults to in-memory `memory://`)

Store environment variables in a `.env` file in the `backend/` folder for local development (see `.env.example`).

## 6. SQLite development mode

Behavior:
- If `DATABASE_URL` is NOT set, the app will automatically use a local SQLite database at `backend/dev.sqlite`.
- This mode allows teammates and recruiters to run the backend without PostgreSQL installed.

Notes:
- SQLite is intended for local development and testing only. It preserves the same SQLAlchemy models so database migrations and schema compatibility remain consistent when moving to PostgreSQL.

## 7. PostgreSQL production mode

Behavior:
- If `DATABASE_URL` IS set, the app uses it as the SQLALCHEMY_DATABASE_URI and attempts to connect to PostgreSQL.
- Do not remove PostgreSQL support — it remains the recommended production datastore.

## 8. Installation

1. Create a Python 3.11+ virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.venv\Scripts\Activate.ps1 # Windows PowerShell
```

2. Install backend dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Create a `.env` file with required environment variables or set them in your shell.

## 9. Running the backend

Quick start (development):

```bash
# from backend/ directory
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

On Windows PowerShell:

```powershell
$env:FLASK_APP = 'app.py'
$env:FLASK_ENV = 'development'
flask run --host=0.0.0.0 --port=5000
```

The app prints a startup environment report showing which subsystems are READY or NOT READY (Database, Authentication, TalentParse Engine, TalentCore Engine, Dashboard API, Resume Upload API). If `DATABASE_URL` is unset, the report will indicate SQLite (dev fallback).

## 10. Running the frontend (local dev)

The frontend is a separate Vite React app in the repository root. From project root, run:

```bash
cd .. # if you're inside backend/
# install JS deps if not already
npm install
npm run dev
```

The frontend expects the backend API at `/api` by default. `src/contexts/AuthContext.jsx` sets the axios base URL to `VITE_API_BASE_URL` or `http://localhost:5000/api` when not provided. For local development you can run both frontend and backend locally.

## 11. API endpoints (overview)

- `GET /api/health` — basic API health
- `POST /api/auth/register` — register user
- `POST /api/auth/login` — login (returns access_token + refresh_token)
- `POST /api/auth/refresh` — refresh access token
- `GET /api/auth/me` — fetch current user (requires `Authorization: Bearer <token>`)
- `GET /api/dashboard` — mission control dashboard payload
- `GET /api/dashboard/demo` — demo dashboard using `demo_user`
- `POST /api/resumes/upload` — multipart file upload (file, optional `user_id`, optional `target_career`)
- `GET /api/resumes/demo` — demo resume processing (builds demo profile for `demo_user`)

Refer to the frontend service implementations (`src/services/resumeService.js`, `src/services/dashboardService.js`) for example usage.

## 12. TalentParse Engine

Location: `app/resume_pipeline`

High-level flow:
- `validation.validate_upload` — performs size and basic format checks and computes a file hash
- `parsers.*` — `pdf_parser` and `docx_parser` attempt deterministic extraction using `pdfplumber` and `python-docx` (if installed)
- `normalizer` — sectionization, contact extraction, skill detection, experience parsing, achievements
- `service.TalentParseService` — orchestrates the pipeline and returns `profile`, `intel`, `stages`, and `meta`.

Important notes:
- If `pdfplumber` or `python-docx` are not installed, the pipeline will return an extraction failure for binary files; the demo route (`/api/resumes/demo`) bypasses binary parsing and uses `process_text_resume` for reliable demos.

## 13. TalentCore Engine (CareerIntel)

Location: `app/career_intel`

Deterministic calculators compute:
- `careerScore`, `resumeScore`, `atsScore`
- `skillGaps`, `jobMatches`, `careerDNA`, and `recommendations`

Weights and benchmarks are configurable in `career_intel/config.py`. The engine is intentionally deterministic and explainable for alpha.

## 14. Dashboard API

Location: `app/dashboard`

`DashboardService.get_dashboard` composes the UI payload. When a processed profile is available (via the demo in-memory store), it populates the dashboard with the real parsed profile and CareerIntel results. Otherwise it uses demo context.

## 15. Resume Upload API

Location: `app/resume_pipeline/routes.py`

Endpoint expects a multipart `file` field. It returns a JSON response containing:
- `status` — `ok` or `failed`
- `profile` — normalized profile (when `ok`)
- `intel` — CareerIntel results
- `stages` — array of pipeline stage events for UI mapping

Example from frontend: `src/services/resumeService.js` shows how to send the file and optional `user_id`.

## 16. Authentication

Auth uses a simple JWT flow:
- `AuthService.register` — create user and hashed password (bcrypt)
- `AuthService.login` — verifies password and returns `access_token` and `refresh_token`
- `AuthService.get_user_from_token` — helper for `GET /api/auth/me`

For local alpha, tokens are signed with `JWT_SECRET_KEY` (default `change-me` if unset). Always set a strong secret for public or production deployments.

## 17. Troubleshooting

- Backend fails on start with `DATABASE_URL must be set`:
  - This should not occur with the current code unless the environment is non-standard. Ensure you are running the `backend/` package entry point (`flask run` from `backend/`) so the fallback logic applies. If you purposely set `DATABASE_URL` and it's unreachable, the app may still initialize but DB connections will fail at first query.
- Resume upload returns `extraction_empty_or_scanned`:
  - Ensure `pdfplumber` and/or `python-docx` are installed when uploading PDFs or DOCX. Scanned PDFs require OCR and are not supported in the alpha pipeline.
- Auth errors on login/registration:
  - Ensure the database is initialized and migrations (if any) have been applied. For local dev the SQLite fallback will create `dev.sqlite` automatically on first run.
- Missing Python packages:
  - Run `pip install -r requirements.txt` from the `backend/` folder.
- CORS / API base URL problems:
  - The frontend defaults to `http://localhost:5000/api`. Set `VITE_API_BASE_URL` in the frontend `.env` if your backend runs elsewhere.

---

If you want, I can now add a brief `backend/CONTRIBUTING.md` with run-check commands and common troubleshooting snippets. Otherwise I will stop here and await Phase 6 instructions.
