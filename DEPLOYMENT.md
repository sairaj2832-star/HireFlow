# HireFlow — Deployment Guide

## Overview

HireFlow is a single-instance AI candidate screening and interview intelligence system. This guide covers deployment to Railway (backend) and Vercel (frontend).

## Architecture

```
Frontend (Vercel)          Backend (Railway)         SQLite (Railway)
   React/Vite                FastAPI/Python           File-based DB
      |                          |                        |
      +-- /api/* -------------> :8000 -------------------> hireflow.db
```

## Prerequisites

- GitHub account
- Railway account (railway.app) — free tier available
- Vercel account (vercel.com) — free tier available
- Node.js 18+ and Python 3.11+

## Backend Deployment (Railway)

### Option 1: Docker (Recommended)

1. **Create a new project** on Railway
2. **Select "Dockerfile"** as the build source
3. **Set environment variables** (see below)
4. **Deploy**

Railway will:
- Build the Docker image
- Run it on their platform
- Provide a public URL

### Option 2: Python Build

1. **Create a new project** on Railway
2. **Select "Python"** as the build source
3. **Set the start command** to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Set environment variables**
5. **Deploy**

### Backend Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PORT` | Auto | Port Railway assigns (default 8000) |
| `TYPESAFE_API_KEY` | No | Jev classifier API key (enables Jev primary) |
| `GEMINI_API_KEY` | No | Google Gemini API key (LLM fallback) |
| `OPENROUTER_API_KEY` | No | OpenRouter API key (LLM fallback) |
| `APP_ENV` | No | Set to `production` |

**Note:** If no API keys are set, the system uses a deterministic seeded fallback. The demo never blocks on network issues.

### Verify Backend Deployment

```bash
curl https://your-backend.railway.app/health
# Expected: {"status":"ok","version":"0.1.0"}
```

## Frontend Deployment (Vercel)

### Option 1: Vercel CLI (Recommended)

```bash
cd frontend
npm install
npm run build
vercel --prod
```

### Option 2: Vercel Web UI

1. **Import project** from GitHub
2. **Set Framework Preset** to `Vite`
3. **Set Environment Variables:**
   - `VITE_API_BASE_URL` = `https://your-backend.railway.app`
4. **Deploy**

### Frontend Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_BASE_URL` | Yes | Backend API base URL |

**Important:** Never expose `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, or `TYPESAFE_API_KEY` to the frontend. These are server-only.

### Verify Frontend Deployment

Open the deployed URL in a browser. You should see the HireFlow dashboard.

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
python -m app.db.migrate
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Opens http://localhost:5173 with proxy to backend
```

## Verification

### Pre-deployment

```bash
powershell -ExecutionPolicy Bypass -File scripts/verify.ps1
```

### Post-deployment

```bash
bash scripts/smoke-test.sh https://your-backend.railway.app
```

## Environment Configuration

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your keys
```

**Never commit `.env` to version control.**

## Known Limitations

- **SQLite:** Single-instance only. Not suitable for horizontal scaling.
- **Seeded Fallback:** Without API keys, classification uses deterministic seeded fallback (not ML).
- **No PDF Export:** Reports are JSON only.
- **No BRAKE3:** Human approval queue not implemented.
- **Single Region:** Deployed to a single Railway region.

## Support

For issues, see `AGENTS.md` or the architecture docs in `docs/`.