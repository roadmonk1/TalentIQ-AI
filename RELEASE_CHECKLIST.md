# TalentIQ-AI Production Release Checklist

This checklist guides the engineering team through deploying, verifying, and rolling back the TalentIQ-AI application in a production environment.

---

## 1. Environment Configurations

Ensure the following variables are securely set in your production container/host dashboard:

### Backend Environments
- `SECRET_KEY`: A high-entropy cryptographically secure random string.
- `JWT_SECRET_KEY`: A separate high-entropy random string for signing JWT tokens.
- `DATABASE_URL`: PostgreSQL production database URI (e.g. `postgresql://<user>:<password>@<host>:<port>/<db>`).
- `GROQ_API_KEY`: API key for mentor AI features.
- `FLASK_APP`: `app`
- `FLASK_ENV`: `production`

### Frontend Environments
- `VITE_API_BASE_URL`: The fully-qualified backend domain API URL (e.g. `https://api.talentiq-ai.com/api`). Do **NOT** use `localhost` fallbacks in production.

---

## 2. Step-by-Step Deployment Protocol

Follow these steps sequentially to deploy:

### Step 2.1: Database Migrations
Always run migrations before starting the application worker servers:
```bash
cd backend
# Apply all pending Alembic schema migrations
flask db upgrade
```

### Step 2.2: Backend WSGI Server Startup
Deploy the Gunicorn runner using the wsgi entrypoint and environment configuration:
```bash
cd backend
gunicorn -c gunicorn.conf.py wsgi:app
```

### Step 2.3: Frontend Asset Compilation & Build
Build the client static React bundle:
```bash
npm install
npm run build
```
Verify that the outputs are compiled into the `dist/` directory, then synchronize the static directory to your host (Netlify, Vercel, AWS S3, or Nginx static root).

---

## 3. Staging Smoke Test Flow

Run this verification check post-deployment:

1. **Verify Health Endpoint**:
   - Query `GET /api/mentor/health` (publicly accessible).
   - Ensure the JSON reports:
     ```json
     {
       "status": "ok",
       "database": "connected",
       "provider": "available",
       "version": "1.0.0-beta"
     }
     ```
2. **Verify Auth signup/login**:
   - Navigate to the register/login screen.
   - Create a test account, and log in.
3. **Verify Resume Parse & calculation**:
   - Upload a sample text resume.
   - Verify the dashboard switches from the **Welcome Empty State** to showing parsed sections and calculated scores.
4. **Verify TalentCoach**:
   - Start a mentor chat and confirm the AI responds.
   - Accept a daily mission.

---

## 4. Rollback & Recovery Protocols

If any issues arise during deployment:

### Step 4.1: Code Rollback
Rollback to the previous stable Git commit on your production branch:
```bash
git reset --hard <previous-stable-commit-hash>
```

### Step 4.2: Database Migration Downgrade
If the deployment added database schemas that must be rolled back:
```bash
flask db downgrade <previous-revision-id>
```
If a complete database restoration is required from a daily backup snapshot:
```bash
pg_restore -h <db-host> -U <db-user> -d <db-name> <backup-file-path>
```
