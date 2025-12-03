# Deploying to Vercel (Full Stack)

This guide shows you how to deploy the entire Viral Content Agent application (frontend + backend) to Vercel only.

## Overview

Vercel supports both Next.js frontend and Python serverless functions, allowing you to deploy everything in one place:

- **Frontend**: Next.js app (automatically detected)
- **Backend**: FastAPI wrapped as Python serverless function using Mangum

## Prerequisites

1. A Vercel account ([vercel.com](https://vercel.com))
2. GitHub repository with your code
3. API keys:
   - Groq API key ([console.groq.com](https://console.groq.com))
   - Tavily API key ([tavily.com](https://tavily.com))

## Step 1: Prepare Your Repository

Make sure your repository structure looks like this:

```
viral-content-agent/
├── api/
│   └── index.py          # Vercel serverless function wrapper
├── backend/              # FastAPI backend code
│   ├── main.py
│   ├── requirements.txt
│   └── ...
├── frontend/             # Next.js frontend
│   ├── package.json
│   └── ...
├── requirements.txt      # Root requirements (references backend/requirements.txt)
└── vercel.json          # Vercel configuration
```

## Step 2: Deploy to Vercel

### Option A: Via Vercel Dashboard

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Vercel will auto-detect the configuration from `vercel.json`
5. Configure environment variables (see Step 3)
6. Click **"Deploy"**

### Option B: Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - Project name? viral-content-agent
# - Directory? ./
```

## Step 3: Configure Environment Variables

In the Vercel dashboard, go to **Settings → Environment Variables** and add:

### Required Variables

```
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Optional Variables (with defaults)

```
GROQ_MODEL=llama-3.3-70b-versatile
MAX_ITERATIONS=3
VIRALITY_THRESHOLD=85
```

**Important**: 
- Add these for **Production**, **Preview**, and **Development** environments
- After adding variables, **redeploy** your application

## Step 4: Verify Deployment

1. Visit your Vercel deployment URL (e.g., `https://your-app.vercel.app`)
2. Test the health endpoint: `https://your-app.vercel.app/api/health`
3. Try generating content for a test topic
4. Check that all features work:
   - Content generation
   - Draft history
   - Research angles
   - Editor feedback

## How It Works

### Architecture

```
User Request
    ↓
Vercel Edge Network
    ↓
/api/* routes → Python Serverless Function (api/index.py)
    ↓
Mangum Adapter → FastAPI App (backend/main.py)
    ↓
LangGraph Workflow → AI Agents
    ↓
Response → User
```

### File Structure

- **`api/index.py`**: Vercel serverless function entry point
  - Wraps FastAPI app with Mangum (ASGI adapter)
  - Handles routing to backend code

- **`vercel.json`**: Vercel configuration
  - Routes `/api/*` to Python serverless function
  - Configures Next.js frontend build

- **`requirements.txt`**: Root Python dependencies
  - References `backend/requirements.txt`
  - Includes Mangum for serverless adapter

## Troubleshooting

### "Module not found" errors

- Ensure `backend/requirements.txt` includes all dependencies
- Check that `requirements.txt` at root references backend requirements correctly
- Vercel auto-detects Python runtime (no need to specify in vercel.json)

### API routes not working

- Check that `api/index.py` exists and is properly configured
- Verify `vercel.json` rewrites are correct
- Check Vercel function logs in dashboard

### Environment variables not loading

- Ensure variables are set in Vercel dashboard
- Add variables for all environments (Production, Preview, Development)
- Redeploy after adding variables

### CORS errors

- FastAPI CORS is already configured for `*.vercel.app` domains
- If using custom domain, update CORS in `backend/main.py`

### Cold starts

- First request after inactivity may take 5-10 seconds
- Subsequent requests are fast (< 1 second)
- Consider Vercel Pro plan for better performance

## Performance Considerations

### Serverless Function Limits

- **Execution Time**: 10 seconds (Hobby), 60 seconds (Pro)
- **Memory**: 1024 MB default
- **Cold Starts**: ~2-5 seconds for Python functions

### Optimization Tips

1. **Warm Functions**: Use Vercel Pro for better cold start handling
2. **Caching**: Consider caching research results
3. **Streaming**: Use streaming endpoint for long-running generations
4. **Timeout**: Content generation may take 30-60 seconds - ensure Pro plan

## Cost

### Free Tier (Hobby)

- ✅ Unlimited deployments
- ✅ 100GB bandwidth
- ⚠️ 10-second function timeout (may be limiting)
- ⚠️ Cold starts can be slow

### Pro Tier ($20/month)

- ✅ 60-second function timeout
- ✅ Better cold start performance
- ✅ Priority support
- ✅ Team collaboration

**Recommended**: Start with Hobby, upgrade to Pro if you hit timeout limits.

## Local Development

For local development, you still need to run frontend and backend separately:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

The frontend will use `http://localhost:8000` for API calls in development.

## Monitoring

### Vercel Dashboard

- View function logs: **Deployments → [Deployment] → Functions**
- Monitor performance: **Analytics** tab
- Check errors: **Logs** tab

### Function Logs

Access logs via:
1. Vercel Dashboard → Your Project → Deployments
2. Click on a deployment
3. Go to **Functions** tab
4. Click on `api/index.py` to see logs

## Next Steps

- Set up custom domain (optional)
- Configure analytics
- Set up monitoring alerts
- Optimize for production traffic

---

**Your app is now live on Vercel! 🚀**

All in one place - no need for separate backend hosting.

