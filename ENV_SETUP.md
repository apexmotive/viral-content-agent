# Environment Variable Setup for Vercel

## For the API to work correctly:

### Option 1: Use Relative Paths (Recommended)

**Don't set `NEXT_PUBLIC_API_URL` at all** - leave it unset. The frontend will automatically use relative paths in production.

The API client will:
- Use `http://localhost:8000` in development (when running on localhost)
- Use relative paths (same domain) in production on Vercel

### Option 2: Set Base URL Only (If Option 1 doesn't work)

If you need to set `NEXT_PUBLIC_API_URL`, set it to the **base URL WITHOUT `/api`**:

```
NEXT_PUBLIC_API_URL=https://viral-content-agent-s6tp.vercel.app
```

**NOT:**
```
NEXT_PUBLIC_API_URL=https://viral-content-agent-s6tp.vercel.app/api  ❌ Wrong!
```

The frontend automatically adds `/api/` to all API calls, so if you include `/api` in the environment variable, it will create double paths like `/api/api/generate`.

## Required Environment Variables

Set these in Vercel Dashboard → Settings → Environment Variables:

```
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
GROQ_MODEL=llama-3.3-70b-versatile (optional)
MAX_ITERATIONS=3 (optional)
VIRALITY_THRESHOLD=85 (optional)
```

**Do NOT set `NEXT_PUBLIC_API_URL` unless absolutely necessary.**

