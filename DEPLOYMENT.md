# Deployment Guide

This document provides detailed instructions for deploying WriteSpace to [Vercel](https://vercel.com) with a [Neon PostgreSQL](https://neon.tech) database.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [1. Database Setup (Neon PostgreSQL)](#1-database-setup-neon-postgresql)
- [2. Vercel Project Setup](#2-vercel-project-setup)
- [3. Environment Variables](#3-environment-variables)
- [4. vercel.json Configuration](#4-verceljson-configuration)
- [5. Deploy to Vercel](#5-deploy-to-vercel)
- [6. Run Migrations](#6-run-migrations)
- [7. Create Default Admin User](#7-create-default-admin-user)
- [8. Static Files (Whitenoise)](#8-static-files-whitenoise)
- [9. Custom Domain (Optional)](#9-custom-domain-optional)
- [10. Troubleshooting](#10-troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

- A [Vercel](https://vercel.com) account
- A [Neon](https://neon.tech) account (or another PostgreSQL provider)
- [Vercel CLI](https://vercel.com/docs/cli) installed (`npm i -g vercel`)
- Python 3.12+ installed locally
- Git repository hosted on GitHub, GitLab, or Bitbucket

---

## 1. Database Setup (Neon PostgreSQL)

1. Sign in to [Neon Console](https://console.neon.tech).
2. Create a new project and database.
3. Copy the connection string from the **Connection Details** panel. It will look like:

   ```
   postgres://username:password@ep-example-123456.us-east-2.aws.neon.tech/dbname?sslmode=require
   ```

4. Keep this connection string ready — you will use it as the `DATABASE_URL` environment variable.

> **Note:** Neon provides a serverless PostgreSQL instance that works well with Vercel's serverless functions. The connection string includes SSL by default.

---

## 2. Vercel Project Setup

### Option A: Connect via GitHub (Recommended)

1. Push your code to a GitHub repository.
2. Go to [Vercel Dashboard](https://vercel.com/dashboard) and click **Add New → Project**.
3. Import your GitHub repository.
4. Vercel will auto-detect the project. Set the **Root Directory** to the repository root (where `vercel.json` is located).
5. **Do not** configure a build command or output directory — the `vercel.json` handles routing and build configuration.
6. Click **Deploy**.

### Option B: Deploy via Vercel CLI

```bash
# Login to Vercel
vercel login

# Deploy from the project root (where vercel.json is located)
vercel

# For production deployment
vercel --prod
```

---

## 3. Environment Variables

Set the following environment variables in your Vercel project settings under **Settings → Environment Variables**. Apply them to **Production**, **Preview**, and **Development** environments as needed.

| Variable | Required | Example Value | Description |
|---|---|---|---|
| `SECRET_KEY` | **Yes** | `a-long-random-string-at-least-50-chars` | Django secret key for cryptographic signing. Generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | **Yes** | `False` | **Must be `False` in production.** Enables debug mode when `True`. |
| `DATABASE_URL` | **Yes** | `postgres://user:pass@host/db?sslmode=require` | PostgreSQL connection string from Neon. |
| `ALLOWED_HOSTS` | **Yes** | `your-app.vercel.app,your-domain.com` | Comma-separated list of hostnames the app will respond to. Include your Vercel deployment URL and any custom domains. |
| `CSRF_TRUSTED_ORIGINS` | **Yes** | `https://your-app.vercel.app,https://your-domain.com` | Comma-separated list of trusted origins for CSRF validation. **Must include the scheme (`https://`).** |
| `DEFAULT_ADMIN_USERNAME` | Recommended | `admin` | Username for the default admin superuser. |
| `DEFAULT_ADMIN_PASSWORD` | Recommended | `a-strong-password` | Password for the default admin superuser. **Use a strong password in production.** |
| `DEFAULT_ADMIN_EMAIL` | Recommended | `admin@yourdomain.com` | Email for the default admin superuser. |

### Setting Variables via Vercel CLI

You can also set environment variables from the command line:

```bash
vercel env add SECRET_KEY
vercel env add DEBUG
vercel env add DATABASE_URL
vercel env add ALLOWED_HOSTS
vercel env add CSRF_TRUSTED_ORIGINS
vercel env add DEFAULT_ADMIN_USERNAME
vercel env add DEFAULT_ADMIN_PASSWORD
vercel env add DEFAULT_ADMIN_EMAIL
```

Each command will prompt you for the value and which environments to apply it to.

### Generating a Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

> **Security Warning:** Never reuse the example secret key from `.env.example` in production. Always generate a unique, random secret key.

---

## 4. vercel.json Configuration

The project includes a `vercel.json` at the repository root that configures the deployment:

```json
{
  "builds": [
    {
      "src": "writespace/writespace/wsgi.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb",
        "runtime": "python3.12"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "writespace/writespace/wsgi.py"
    }
  ]
}
```

### Explanation

| Key | Purpose |
|---|---|
| `builds[0].src` | Points to the Django WSGI application entry point at `writespace/writespace/wsgi.py`. |
| `builds[0].use` | Uses the `@vercel/python` builder to package the Python application as a serverless function. |
| `builds[0].config.maxLambdaSize` | Sets the maximum size of the serverless function bundle to 15 MB (accommodates Django + dependencies). |
| `builds[0].config.runtime` | Specifies Python 3.12 as the runtime version. |
| `routes[0]` | Catches all incoming requests (`/(.*)`) and routes them to the WSGI application. |

### How It Works

1. Vercel installs dependencies from `requirements.txt` at the repository root.
2. The `@vercel/python` builder packages the Django application into a serverless function.
3. All HTTP requests are routed through Django's WSGI handler, which processes URL routing, middleware, and views as normal.
4. Static files are served by Whitenoise middleware (see [Static Files](#8-static-files-whitenoise)).

---

## 5. Deploy to Vercel

### First Deployment

After connecting your repository and setting environment variables:

1. Vercel will automatically trigger a deployment when you push to the main branch.
2. Monitor the build logs in the Vercel dashboard for any errors.
3. Once deployed, your app will be available at `https://your-project.vercel.app`.

### Manual Deployment

```bash
# Preview deployment
vercel

# Production deployment
vercel --prod
```

### Redeployment

Any push to the connected Git branch will trigger an automatic redeployment. You can also trigger a manual redeployment from the Vercel dashboard.

---

## 6. Run Migrations

Vercel serverless functions do not run management commands automatically. You must run migrations manually by connecting to your production database from your local machine.

### Option A: Using Environment Variable Inline

```bash
# Navigate to the Django project directory
cd writespace

# Run migrations against the production database
DATABASE_URL="postgres://user:pass@host/db?sslmode=require" python manage.py migrate
```

### Option B: Using an .env File

1. Create a temporary `.env.production` file (do **not** commit this):

   ```
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   DATABASE_URL=postgres://user:pass@host/db?sslmode=require
   ALLOWED_HOSTS=your-app.vercel.app
   CSRF_TRUSTED_ORIGINS=https://your-app.vercel.app
   ```

2. Export the variables and run migrations:

   ```bash
   export $(cat .env.production | xargs)
   cd writespace
   python manage.py migrate
   ```

3. Delete `.env.production` when done.

### Option C: Using a Script

Create a local script for convenience (do **not** commit this):

```bash
#!/bin/bash
# deploy-migrate.sh
export DATABASE_URL="postgres://user:pass@host/db?sslmode=require"
export SECRET_KEY="your-production-secret-key"
cd writespace
python manage.py migrate
python manage.py create_default_admin
```

```bash
chmod +x deploy-migrate.sh
./deploy-migrate.sh
```

> **Important:** Run migrations every time you deploy changes that include new or modified models.

---

## 7. Create Default Admin User

After running migrations, create the default admin superuser:

```bash
cd writespace
DATABASE_URL="postgres://user:pass@host/db?sslmode=require" python manage.py create_default_admin
```

This command reads the following environment variables:

| Variable | Default | Description |
|---|---|---|
| `DEFAULT_ADMIN_USERNAME` | `admin` | The admin username |
| `DEFAULT_ADMIN_PASSWORD` | `admin` | The admin password |
| `DEFAULT_ADMIN_EMAIL` | `admin@example.com` | The admin email |

If the user already exists, the command will skip creation and print a warning.

> **Security Warning:** Change the default admin password immediately after first login in production. Never use `admin`/`admin` as credentials in a production environment.

---

## 8. Static Files (Whitenoise)

WriteSpace uses [Whitenoise](http://whitenoise.evans.io/) to serve static files directly from the Django application without requiring a separate static file server or CDN.

### How It Works

1. **Middleware:** `whitenoise.middleware.WhiteNoiseMiddleware` is included in `MIDDLEWARE` in `settings.py`, positioned directly after `SecurityMiddleware`.
2. **Storage Backend:** The project uses `whitenoise.storage.CompressedManifestStaticFilesStorage`, which:
   - Compresses static files with gzip and Brotli.
   - Appends content hashes to filenames for cache busting.
   - Generates a `staticfiles.json` manifest.
3. **Collection:** During the Vercel build, `collectstatic` is run automatically by the `@vercel/python` builder, gathering all static files into the `staticfiles/` directory.

### Configuration in settings.py

```python
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}
```

### Tailwind CSS

The project uses Tailwind CSS via CDN (`<script src="https://cdn.tailwindcss.com"></script>` in `base.html`), so no build step is required for CSS. This is loaded directly from the CDN on each page request.

> **Note:** For production applications with high traffic, consider switching to a pre-built Tailwind CSS file served as a static asset instead of the CDN script.

---

## 9. Custom Domain (Optional)

1. Go to your Vercel project **Settings → Domains**.
2. Add your custom domain (e.g., `writespace.yourdomain.com`).
3. Follow Vercel's instructions to configure DNS records.
4. **Update environment variables:**
   - Add the custom domain to `ALLOWED_HOSTS`: `your-app.vercel.app,writespace.yourdomain.com`
   - Add the custom domain to `CSRF_TRUSTED_ORIGINS`: `https://your-app.vercel.app,https://writespace.yourdomain.com`
5. Redeploy for the changes to take effect.

---

## 10. Troubleshooting

### Build Fails: "No module named 'django'"

**Cause:** Dependencies are not being installed.

**Fix:** Ensure `requirements.txt` is in the repository root (not inside the `writespace/` directory). Vercel looks for `requirements.txt` at the root level.

### 500 Internal Server Error

**Cause:** Usually a misconfigured environment variable.

**Fix:**
1. Check that `SECRET_KEY` is set and is a non-empty string.
2. Check that `DATABASE_URL` is a valid PostgreSQL connection string.
3. Check that `ALLOWED_HOSTS` includes your Vercel deployment URL.
4. Check that `DEBUG` is set to `False` (not an empty string).
5. Review the Vercel function logs: **Vercel Dashboard → Deployments → (select deployment) → Functions → (select function) → Logs**.

### 400 Bad Request / CSRF Verification Failed

**Cause:** The origin is not listed in `CSRF_TRUSTED_ORIGINS`.

**Fix:** Ensure `CSRF_TRUSTED_ORIGINS` includes the full origin with scheme:
```
https://your-app.vercel.app,https://your-domain.com
```

Common mistakes:
- Missing `https://` prefix (Django requires the scheme).
- Trailing slash (do not include trailing slashes).
- Using `http://` instead of `https://` (Vercel serves over HTTPS).

### DisallowedHost Error

**Cause:** The request's `Host` header is not in `ALLOWED_HOSTS`.

**Fix:** Add the hostname to `ALLOWED_HOSTS`. Remember to include:
- Your Vercel deployment URL (e.g., `your-app.vercel.app`)
- Any Vercel preview URLs (e.g., `your-app-git-branch-username.vercel.app`)
- Any custom domains

### Database Connection Errors

**Cause:** Invalid `DATABASE_URL` or network connectivity issues.

**Fix:**
1. Verify the `DATABASE_URL` connection string is correct.
2. Ensure `?sslmode=require` is appended for Neon connections.
3. Check that the Neon database is active (Neon suspends idle databases on the free tier — accessing the Neon console will wake it up).
4. Test the connection locally:
   ```bash
   DATABASE_URL="your-connection-string" cd writespace && python manage.py dbshell
   ```

### Static Files Not Loading (404 on /static/)

**Cause:** `collectstatic` did not run or Whitenoise is misconfigured.

**Fix:**
1. Ensure `whitenoise.middleware.WhiteNoiseMiddleware` is in `MIDDLEWARE` after `SecurityMiddleware`.
2. Ensure `STATIC_ROOT` is set in `settings.py`.
3. Ensure the `static/` directory exists (even if it only contains `.gitkeep` files).
4. Try running `collectstatic` manually locally to verify:
   ```bash
   cd writespace
   python manage.py collectstatic --noinput
   ```

### "Table does not exist" Errors

**Cause:** Migrations have not been run against the production database.

**Fix:** Run migrations manually as described in [Run Migrations](#6-run-migrations):
```bash
DATABASE_URL="your-connection-string" cd writespace && python manage.py migrate
```

### Lambda Size Exceeded

**Cause:** The serverless function bundle exceeds the configured `maxLambdaSize`.

**Fix:**
1. The current limit is set to `15mb` in `vercel.json`.
2. If you add large dependencies, you may need to increase this value (Vercel's maximum is `50mb`).
3. Review `requirements.txt` and remove unused dependencies.

### Vercel CLI Deployment Issues

If `vercel` CLI commands fail:

```bash
# Ensure you're logged in
vercel login

# Link to existing project
vercel link

# Check project settings
vercel env ls
```

---

## Deployment Checklist

Use this checklist before every production deployment:

- [ ] `SECRET_KEY` is set to a unique, random value (not the default from `.env.example`)
- [ ] `DEBUG` is set to `False`
- [ ] `DATABASE_URL` points to the production PostgreSQL database
- [ ] `ALLOWED_HOSTS` includes all production hostnames
- [ ] `CSRF_TRUSTED_ORIGINS` includes all production origins with `https://` prefix
- [ ] `DEFAULT_ADMIN_PASSWORD` is set to a strong password (not `admin`)
- [ ] Migrations have been run against the production database
- [ ] Default admin user has been created via `create_default_admin`
- [ ] The application loads without errors at the deployment URL
- [ ] Login and registration work correctly
- [ ] Blog post creation, editing, and deletion work correctly
- [ ] Admin dashboard is accessible to staff users only