# Deployment Guide

## Deploying to Vercel + Railway

This guide walks you through deploying the Viral Content Agent with:
- **Frontend**: Vercel (Next.js)
- **Backend**: Railway (FastAPI)

---

## Step 1: Deploy Backend to Railway

### 1.1 Prepare Backend for Railway

Railway will automatically detect and deploy Python applications.

Create `railway.json` in the backend directory:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 1.2 Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your repository
5. Select the `backend` directory
6. Railway will auto-detect Python and deploy

### 1.3 Configure Environment Variables

In Railway dashboard, add these environment variables:

```
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
MAX_ITERATIONS=3
VIRALITY_THRESHOLD=85
```

### 1.4 Get Backend URL

After deployment, Railway will provide a URL like:
```
https://your-app.railway.app
```

Copy this URL - you'll need it for the frontend.

---

## Step 2: Deploy Frontend to Vercel

### 2.1 Prepare Frontend

Make sure `frontend/.env.local` is NOT committed to git (it's in `.gitignore`).

### 2.2 Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### 2.3 Configure Environment Variables

In Vercel dashboard, add:

```
NEXT_PUBLIC_API_URL=https://your-app.railway.app
```

Replace with your actual Railway backend URL.

### 2.4 Deploy

Click "Deploy" and wait for the build to complete.

---

## Step 3: Update Backend CORS

After getting your Vercel URL, update the backend CORS settings.

Edit `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-vercel-app.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push - Railway will auto-deploy the update.

---

## Step 4: Test Your Deployment

1. Visit your Vercel URL
2. Try generating content for a test topic
3. Check that all features work:
   - Content generation
   - Draft history
   - Research angles
   - Editor feedback
   - Download functionality

---

## Alternative: Deploy Backend to Render

### Render Setup

1. Go to [render.com](https://render.com)
2. Create new "Web Service"
3. Connect your repository
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. Add environment variables (same as Railway)

6. Deploy

---

## Monitoring & Logs

### Railway
- View logs in Railway dashboard
- Monitor resource usage
- Set up alerts

### Vercel
- View deployment logs
- Monitor function execution
- Check analytics

---

## Troubleshooting

### Backend not responding
- Check Railway/Render logs
- Verify environment variables are set
- Test API directly: `https://your-backend.railway.app/api/health`

### CORS errors
- Verify Vercel URL is in backend CORS settings
- Check that URL doesn't have trailing slash
- Redeploy backend after CORS changes

### Slow generation
- Check if you're on free tier (may have cold starts)
- Consider upgrading to paid tier for better performance
- Monitor API rate limits

---

## Cost Estimates

### Free Tier
- **Vercel**: Free for personal projects
- **Railway**: $5/month credit (enough for light usage)
- **Render**: Free tier available (with limitations)

### Recommended for Production
- **Vercel Pro**: $20/month
- **Railway**: Pay as you go (~$10-20/month)
- **Total**: ~$30-40/month

---

## Security Best Practices

1. **Never commit `.env` files**
2. **Use environment variables** for all secrets
3. **Enable HTTPS only** in production
4. **Rotate API keys** regularly
5. **Monitor usage** to detect anomalies
6. **Set rate limits** on your backend

---

## Scaling Considerations

As your usage grows:

1. **Backend**: Upgrade Railway/Render plan for more resources
2. **Frontend**: Vercel scales automatically
3. **Caching**: Add Redis for caching research results
4. **Database**: Store generation history in PostgreSQL
5. **Queue**: Use Celery for background processing

---

**Your app is now live! 🚀**
