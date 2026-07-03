# TalentIQ-AI Step-by-Step Deployment Guide

Follow this guide to deploy the backend to Render, connect it to either Render PostgreSQL or Neon PostgreSQL, and deploy the frontend static React SPA to Vercel.

---

## 1. Database Provisioning Options

Select **one** of the two PostgreSQL options below to host your production database:

### Option A: Render PostgreSQL (Recommended for all-in-one setups)
1. Log in to the [Render Dashboard](https://dashboard.render.com).
2. Click **New +** and select **Database**.
3. Fill in the database settings:
   - **Name**: `talentiq-db`
   - **Database Name**: `talentiq`
   - **User**: `talentiq_admin`
4. Click **Create Database**.
5. Copy the **Internal Database URL** (for Render-to-Render links) or **External Database URL** (for local/external links).

### Option B: Neon PostgreSQL (Alternative serverless database)
1. Create a free account on [Neon.tech](https://neon.tech).
2. Create a new project named `TalentIQ-AI`.
3. In the project dashboard, select the default branch database.
4. Copy the connection string from the **Connection Details** box. Make sure it begins with `postgres://` or `postgresql://`.

---

## 2. Deploy the Backend to Render

1. Go to the [Render Dashboard](https://dashboard.render.com) and click **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. In the service setup configuration:
   - **Name**: `talentiq-backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements.txt && flask db upgrade`
   - **Start Command**: `cd backend && gunicorn -c gunicorn.conf.py wsgi:app`
4. Under **Advanced / Environment Variables**, add the following keys:
   - `FLASK_APP`: `app`
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: A secure random hex string (e.g. `openssl rand -hex 32` output).
   - `JWT_SECRET_KEY`: A separate secure random hex string.
   - `DATABASE_URL`: Paste the PostgreSQL connection string from **Step 1** (Render or Neon URL).
   - `GROQ_API_KEY`: Paste your production Groq API credentials.
5. Click **Create Web Service**. Render will automatically pull the code, install dependencies, run Alembic migrations, and start Gunicorn.

---

## 3. Deploy the Frontend to Vercel

1. Log in to [Vercel](https://vercel.com).
2. Click **Add New** -> **Project**.
3. Select and import your GitHub repository.
4. Under **Configure Project**:
   - **Framework Preset**: `Vite` (Vercel auto-detects this).
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Expand the **Environment Variables** section and add the target backend URL:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: The public URL of your Render backend service (e.g. `https://talentiq-backend.onrender.com/api`).
6. Click **Deploy**. Vercel compiles the assets, writes the routes, and deploys the SPA.

---

## 4. Staging Smoke Test Protocol

Run these verification checks on the live deployment:

1. **Verify Health Check**:
   - Navigate to `<your-render-backend-url>/api/mentor/health` in your browser.
   - Confirm it reports:
     ```json
     {
       "status": "ok",
       "database": "connected",
       "provider": "available",
       "version": "1.0.0-beta"
     }
     ```
2. **Verify Client SPA Routing Fallback**:
   - Navigate to `<your-vercel-frontend-url>/dashboard`.
   - Refresh the page inside the browser.
   - Verify that Vercel routes back to `/index.html` rather than throwing a `404 Not Found` error.
3. **Verify Auth Journey**:
   - Register a new account on your live frontend.
   - Confirm you see the welcome empty state dashboard.
   - Upload a test resume to verify parsing, database inserts, and dashboard population.
