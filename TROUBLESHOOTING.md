# Troubleshooting: "No response from server" on Vercel

## Issue
Getting "No response from server" error when trying to use the API on Vercel deployment.

## Quick Checks

### 1. Check Vercel Function Logs

1. Go to Vercel Dashboard → Your Project
2. Click on the latest deployment
3. Go to **Functions** tab
4. Click on `api/index.py`
5. Check the logs for errors

Common errors you might see:
- `ModuleNotFoundError` - Missing Python dependencies
- `ImportError` - Path issues
- `AttributeError` - Handler export issues

### 2. Test the API Endpoint Directly

Try accessing the health endpoint directly in your browser:
```
https://your-app.vercel.app/api/health
```

Or use curl:
```bash
curl https://your-app.vercel.app/api/health
```

### 3. Verify Environment Variables

1. Go to Vercel Dashboard → Settings → Environment Variables
2. Ensure these are set:
   - `GROQ_API_KEY`
   - `TAVILY_API_KEY`
3. Make sure they're set for **all environments** (Production, Preview, Development)

### 4. Check Function Timeout

Vercel free tier has a **10-second timeout**. If your function takes longer:
- Upgrade to Vercel Pro (60-second timeout)
- Or optimize your code to run faster

## Common Solutions

### Solution 1: Fix Handler Export

If the function isn't being called, check `api/index.py`:

```python
# Make sure handler is properly exported
def handler(event, context):
    return mangum_handler(event, context)
```

### Solution 2: Check Rewrites Configuration

In `vercel.json`, the rewrite should be:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "/api/index.py"
    }
  ]
}
```

**Note**: Some Vercel setups require the destination to be `/api/index` (without `.py`). Try both.

### Solution 3: Verify Python Dependencies

Check that `requirements.txt` includes all dependencies:

```bash
# In your local environment, test:
pip install -r requirements.txt
python -c "from mangum import Mangum; print('OK')"
```

### Solution 4: Check CORS Configuration

If you see CORS errors, update `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
        "https://your-custom-domain.com"  # Add your domain
    ],
    # ...
)
```

### Solution 5: Test Locally First

Before deploying, test the serverless function locally:

```bash
# Install Vercel CLI
npm i -g vercel

# Run local dev server
vercel dev
```

Then test: `http://localhost:3000/api/health`

## Debugging Steps

### Step 1: Add Logging

Add logging to `api/index.py`:

```python
def handler(event, context):
    print(f"Handler called with event: {event}", flush=True)
    try:
        result = mangum_handler(event, context)
        print(f"Handler returned: {result}", flush=True)
        return result
    except Exception as e:
        print(f"Error: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        raise
```

### Step 2: Check Function Invocation

In Vercel logs, you should see:
- Function invocation logs
- Any print statements
- Error stack traces

### Step 3: Verify Path Resolution

Add this to `api/index.py` to debug paths:

```python
print(f"Current directory: {os.getcwd()}", flush=True)
print(f"Backend path: {backend_path}", flush=True)
print(f"Backend path exists: {backend_path.exists()}", flush=True)
```

## Alternative: Use Next.js API Routes

If Python functions continue to have issues, consider using Next.js API routes as a proxy:

Create `frontend/src/app/api/[...path]/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest, { params }: { params: { path: string[] } }) {
  const path = params.path.join('/');
  const response = await fetch(`https://your-backend-url.com/api/${path}`);
  return NextResponse.json(await response.json());
}

export async function POST(request: NextRequest, { params }: { params: { path: string[] } }) {
  const path = params.path.join('/');
  const body = await request.json();
  const response = await fetch(`https://your-backend-url.com/api/${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return NextResponse.json(await response.json());
}
```

Then deploy backend separately (Railway, Render, etc.) and proxy through Next.js.

## Still Not Working?

1. **Check Vercel Status**: [status.vercel.com](https://status.vercel.com)
2. **Review Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
3. **Check Function Logs**: Look for specific error messages
4. **Test with Minimal Example**: Create a simple Python function to test

Create `api/test.py`:

```python
def handler(event, context):
    return {
        'statusCode': 200,
        'body': '{"message": "Hello from Vercel!"}',
        'headers': {'Content-Type': 'application/json'}
    }
```

Test: `https://your-app.vercel.app/api/test`

If this works, the issue is with the FastAPI/Mangum setup.

