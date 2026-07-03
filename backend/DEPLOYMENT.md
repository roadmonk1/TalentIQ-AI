# Backend Deployment Guide (Production Readiness)

This guide outlines the steps to prepare and deploy the TalentIQ-AI backend to a production environment.

## 1. Environment Configuration

Production configuration must strictly separate settings from code. All sensitive data must be supplied via environment variables.

### Required Environment Variables
| Variable | Description | Recommended Production Value |
| :--- | :--- | :--- |
| `FLASK_APP` | Flask application entry point | `app` |
| `FLASK_ENV` | Environment mode | `production` |
| `SECRET_KEY` | Flask cryptographic secret | A long random string (e.g. generated via `openssl rand -hex 32`) |
| `JWT_SECRET_KEY` | JWT signing secret | A distinct long random string |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://<user>:<password>@<host>:<port>/<db>` |
| `GROQ_API_KEY` | API key for LLM mentor coaching | Valid Groq API Key |
| `RATELIMIT_STORAGE_URL` | Rate limit storage backend | Redis instance URL (e.g. `redis://default:<password>@<host>:<port>`) |

---

## 2. Server & WSGI Runner

Do not use the built-in Flask development server (`flask run`) in production. Use a production WSGI HTTP server such as **Gunicorn**.

### Running Gunicorn
Install `gunicorn` in your production environment:
```bash
pip install gunicorn
```

Start the application with Gunicorn using a production configuration (e.g. 4 worker processes):
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:app"
```

---

## 3. Database Setups & Migrations

For production environments, **PostgreSQL** is the recommended database system.

### Execution Plan:
1. Ensure the PostgreSQL database is provisioned and the credentials are supplied in the `DATABASE_URL` environment variable.
2. Initialize and run migration schemas using Flask-Migrate:
   ```bash
   flask db upgrade
   ```
3. Verify that the migrations applied successfully before starting the WSGI processes.

---

## 4. Production Security Hardening

- **CORS Protection**: Restrict CORS origins to only specify the client web app domains.
- **SSL/TLS**: Ensure the application is behind a reverse proxy (e.g., Nginx, Cloudflare) that terminates SSL and forwards requests over HTTPS.
- **Rate Limiting**: Confirm that `RATELIMIT_STORAGE_URL` points to a persistent caching server (like Redis) so that rate limits are shared across multiple Gunicorn workers.
