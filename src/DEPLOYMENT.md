# Frontend Deployment Guide (Production Readiness)

This guide outlines the steps to build and deploy the TalentIQ-AI React SPA frontend.

## 1. Environment Variable Setup

Before building the production assets, create a `.env.production` file in the project root:

```env
VITE_API_BASE_URL=https://api.talentiq-ai.com/api
```

Replace `https://api.talentiq-ai.com/api` with your actual production backend URL.

---

## 2. Production Asset Build

Run the following command to compile code, resolve imports, optimize assets, and bundle the client-side files:

```bash
npm run build
```

This creates a optimized production bundle in the [dist](file:///c:/Users/K%20SHREYAS%20BHAT/Downloads/TalentIQ-AI/dist) directory.

---

## 3. Hosting Options

Since the output consists of static HTML, JS, and CSS files, you can deploy them to any high-performance static hosting platform:
- **Netlify / Vercel**: Connect your git repository and set build command to `npm run build` and publish directory to `dist`.
- **AWS S3 + CloudFront**: Upload the `dist/` contents to an S3 bucket configured for static web hosting and front it with a CloudFront CDN.
- **Nginx**: Host the static assets on a Linux server by pointing Nginx root to the `dist/` folder.

### Nginx Routing Fallback Configuration
Since this is a Single Page Application (SPA) using client-side routing, Nginx must be configured to route all deep links to `index.html`:
```nginx
server {
    listen 80;
    server_name talentiq-ai.com;

    location / {
        root /var/www/talentiq-ai/dist;
        try_files $uri $uri/ /index.html;
    }
}
```
