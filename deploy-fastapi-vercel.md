# Deploying FastAPI + Next.js to Vercel (Monorepo Setup)

This guide documents the working solution for deploying a FastAPI backend and Next.js frontend together on Vercel, when they're in separate directories (monorepo structure).

## Problem

When deploying a monorepo with:
- Next.js app in `frontend/` directory
- FastAPI backend in `backend/` directory
- Python serverless functions in `api/` directory

Vercel throws: **"No Next.js version detected"** error because it looks for `package.json` with `next` in the root directory.

## Solution Overview

The key is to create a **root `package.json`** that Vercel can detect, while keeping the actual Next.js app in a subdirectory. The install command must install dependencies in the correct order.

## Step-by-Step Setup

### 1. Project Structure

```
your-project/
├── api/
│   └── index.py              # Vercel Python serverless function
├── backend/                   # FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   └── ...
├── frontend/                  # Next.js frontend
│   ├── package.json
│   └── ...
├── package.json              # ⭐ Root package.json (for Vercel detection)
├── requirements.txt          # Root Python deps (references backend/requirements.txt)
└── vercel.json               # Vercel configuration
```

### 2. Create Root `package.json`

Create a `package.json` in the **root directory** with Next.js dependencies:

```json
{
  "name": "your-project",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "build": "cd frontend && npm run build",
    "dev": "cd frontend && npm run dev",
    "start": "cd frontend && npm start"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

**Why this works**: Vercel checks the root directory for `next` in `dependencies` or `devDependencies`. Having it here allows Vercel to detect Next.js, even though the actual app is in `frontend/`.

### 3. Create Root `requirements.txt`

Create a `requirements.txt` in the **root directory**:

```txt
# Root requirements.txt for Vercel deployment
# This file is used by Vercel to install Python dependencies
-r backend/requirements.txt
```

This references your backend requirements file. Make sure `backend/requirements.txt` includes `mangum`:

```txt
fastapi==0.115.0
mangum==0.18.0
# ... other dependencies
```

### 4. Create Vercel Serverless Function Wrapper

Create `api/index.py` (Vercel automatically detects Python functions in `api/` directory):

```python
"""Vercel serverless function wrapper for FastAPI backend."""

import sys
import os
from pathlib import Path

# Get the project root directory (one level up from api/)
project_root = Path(__file__).parent.parent
backend_path = project_root / "backend"

# Add backend directory to Python path
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

# Set working directory to backend for relative imports
original_cwd = os.getcwd()
try:
    os.chdir(backend_path)
    
    # Import FastAPI app from backend
    from main import app
    from mangum import Mangum
    
    # Create ASGI handler for Vercel
    handler = Mangum(app, lifespan="off")
finally:
    os.chdir(original_cwd)

# Export handler for Vercel (required)
# Vercel will call this function for each request
```

### 5. Configure `vercel.json`

Create `vercel.json` in the root:

```json
{
    "buildCommand": "cd frontend && npm run build",
    "devCommand": "cd frontend && npm run dev",
    "installCommand": "npm install && cd frontend && npm install && cd .. && pip install -r requirements.txt",
    "framework": "nextjs",
    "outputDirectory": "frontend/.next",
    "rewrites": [
        {
            "source": "/api/:path*",
            "destination": "/api/index.py"
        }
    ]
}
```

**Critical points**:

1. **`installCommand` order matters**:
   - `npm install` - Installs root dependencies (next, react, react-dom) so Vercel can detect Next.js
   - `cd frontend && npm install` - Installs actual frontend dependencies
   - `cd .. && pip install -r requirements.txt` - Installs Python dependencies

2. **No explicit Python runtime**: Vercel auto-detects Python functions in `api/` directory. Don't specify `runtime` in `functions` config.

3. **Rewrites**: Routes `/api/*` to your Python serverless function.

### 6. Vercel Dashboard Settings

When deploying via Vercel dashboard:

1. **Root Directory**: Set to `.` (root, NOT `frontend`)
2. **Framework Preset**: Next.js (should auto-detect from root package.json)
3. **Build Command**: `cd frontend && npm run build` (or leave default, vercel.json handles it)
4. **Output Directory**: `frontend/.next` (or leave default, vercel.json handles it)
5. **Install Command**: Leave default (vercel.json handles it)

### 7. Environment Variables

Add in Vercel dashboard → Settings → Environment Variables:

```
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
# ... other env vars
```

**Important**: Add for all environments (Production, Preview, Development).

## Why This Works

1. **Root `package.json`**: Vercel checks root for `next` dependency. Having it there allows detection even though the app is in `frontend/`.

2. **Install order**: Installing root deps first ensures Vercel detects Next.js before the build phase.

3. **Mangum adapter**: Converts FastAPI (ASGI) to AWS Lambda/Vercel format.

4. **Auto-detection**: Vercel automatically detects:
   - Next.js from root `package.json`
   - Python functions from `api/` directory
   - No need for explicit runtime configuration

## Common Issues & Solutions

### Issue: "No Next.js version detected"

**Solution**: 
- Ensure root `package.json` has `next` in `dependencies`
- Check that `installCommand` installs root deps first: `npm install && cd frontend && npm install ...`
- Verify Root Directory in Vercel dashboard is `.` (not `frontend`)

### Issue: "Could not open requirements file"

**Solution**: 
- Ensure `installCommand` changes back to root before pip install: `cd .. && pip install -r requirements.txt`
- Check that `requirements.txt` exists in root directory

### Issue: Python function not found

**Solution**:
- Ensure `api/index.py` exists
- Check `vercel.json` rewrites are correct
- Don't specify `runtime` in `functions` config (Vercel auto-detects)

### Issue: Module not found in Python function

**Solution**:
- Check that `api/index.py` correctly adds backend to `sys.path`
- Verify `backend/requirements.txt` includes all dependencies
- Check that working directory is set correctly in `api/index.py`

## Quick Checklist

Before deploying, verify:

- [ ] Root `package.json` exists with `next`, `react`, `react-dom` in dependencies
- [ ] Root `requirements.txt` exists and references `backend/requirements.txt`
- [ ] `backend/requirements.txt` includes `mangum`
- [ ] `api/index.py` exists and properly imports FastAPI app
- [ ] `vercel.json` has correct `installCommand` order
- [ ] Root Directory in Vercel dashboard is `.` (root)
- [ ] Environment variables are set in Vercel dashboard

## Alternative: Separate Deployments

If you continue having issues, consider:

1. **Frontend only on Vercel**: Deploy `frontend/` directory separately
2. **Backend on Railway/Render**: Deploy `backend/` separately
3. **Connect via environment variable**: Set `NEXT_PUBLIC_API_URL` in Vercel

This approach is simpler but requires managing two deployments.

## Summary

The key insight: **Vercel needs to detect Next.js in the root directory**, even if your actual Next.js app is in a subdirectory. By creating a root `package.json` with Next.js dependencies and installing them first, Vercel can detect the framework while still building from the `frontend/` directory.

---

**Last Updated**: Based on working deployment of viral-content-agent
**Tested**: Vercel deployment with Next.js 14 + FastAPI + Python serverless functions

