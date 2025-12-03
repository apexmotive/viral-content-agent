# Viral Content Agent Team 🚀

Transform boring topics into viral social media content using AI agents!

## Overview

The Viral Content Agent Team is a multi-agent system that automatically creates engaging Twitter threads and LinkedIn posts. It uses three specialized AI agents working together:

- **🕵️ Trend Scout**: Researches viral angles using Tavily API
- **✍️ Ghostwriter**: Creates compelling content using Groq LLM
- **⚖️ Chief Editor**: Reviews and scores content for virality (with feedback loop)

## Tech Stack

**Frontend:**
- Next.js 16 (App Router)
- TypeScript
- TailwindCSS with glassmorphism design
- React Markdown for content rendering

**Backend:**
- FastAPI (Python)
- LangGraph for multi-agent orchestration
- Groq API (Llama models)
- Tavily API for research

## Features

✨ **Intelligent Research**: Finds trending angles and connections for any topic  
🎯 **Platform-Optimized**: Different formatting for Twitter threads vs LinkedIn posts  
🔄 **Active Editor**: Chief Editor polishes content directly instead of just critiquing  
📊 **Virality Scoring**: Evaluates hook strength, emoji usage, structure, and platform optimization  
📜 **Draft History**: Track every iteration with scores and feedback  
🎨 **Modern UI**: Vibrant glassmorphism design with real-time updates  
⚙️ **Customizable Settings**: Adjust model, iterations, and threshold on the fly  
🚀 **Vercel Ready**: Optimized for deployment on Vercel

## Installation

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### 1. Clone the repository

```bash
cd /Users/admin/Projects/viral-content-agent
```

### 2. Set up the Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# or
.\venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Set up the Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local if needed (defaults to http://localhost:8000)
```

### 4. Get API Keys

- **Groq API**: Sign up at [console.groq.com](https://console.groq.com) (Free tier available)
- **Tavily API**: Sign up at [tavily.com](https://tavily.com) (Free tier: 1000 requests/month)

Add them to `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
MAX_ITERATIONS=3
VIRALITY_THRESHOLD=85
```

## Usage

### Running Locally

You need two terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python main.py
# or
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

The app will open at `http://localhost:3000`

### Using the Application

1. **Configure Settings** (in sidebar):
   - Select your preferred model
   - Adjust max iterations (1-5)
   - Set virality threshold (50-100)

2. **Enter a topic** (even boring technical topics work great!):
   - Example: "Database Normalization"
   - Example: "Supply Chain Logistics"
   
3. **Select platform**: Twitter or LinkedIn

4. **Click "Generate"**

5. **Watch the agents work**:
   - Trend Scout researches angles
   - Ghostwriter creates drafts
   - Chief Editor scores and provides feedback
   - Loop repeats until content passes threshold
   - Chief Editor applies final polish

6. **Explore Results** in tabs:
   - **Ghostwriter Tab**: View final content and all draft iterations with scores
   - **Trend Scout Tab**: See research angles and sources
   - **Chief Editor Tab**: Review all feedback and scores

7. **Download your viral content** ready to post!

## Deployment to Vercel

### Option 1: Vercel (Frontend Only)

If you want to deploy the frontend to Vercel and run the backend separately:

1. **Deploy Frontend to Vercel:**
   ```bash
   cd frontend
   vercel
   ```

2. **Deploy Backend to Railway/Render/Fly.io:**
   - Push backend to a separate repository
   - Deploy using your preferred platform
   - Get the backend URL

3. **Configure Frontend Environment:**
   - In Vercel dashboard, add environment variable:
   - `NEXT_PUBLIC_API_URL` = your backend URL

### Option 2: Separate Deployment

**Backend (Railway/Render):**
```bash
# Push backend directory to GitHub
# Connect to Railway/Render
# Add environment variables in dashboard
```

**Frontend (Vercel):**
```bash
# Push frontend directory to GitHub
# Connect to Vercel
# Add NEXT_PUBLIC_API_URL environment variable
```

## Project Structure

```
viral-content-agent/
├── backend/                    # FastAPI backend
│   ├── main.py                # FastAPI app entry point
│   ├── api/
│   │   ├── routes.py          # API endpoints
│   │   └── models.py          # Pydantic models
│   ├── agents/                # Agent implementations
│   ├── workflow/              # LangGraph orchestration
│   ├── tools/                 # API integrations
│   ├── utils/                 # Utilities
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Backend secrets
│
├── frontend/                   # Next.js frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx     # Root layout
│   │   │   ├── page.tsx       # Main page
│   │   │   └── globals.css    # Global styles
│   │   └── lib/
│   │       └── api.ts         # API client
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.ts
│   └── .env.local             # Frontend env vars
│
├── vercel.json                # Vercel deployment config
└── README.md                  # This file
```

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/models` - List available models
- `POST /api/generate` - Generate viral content
- `POST /api/generate/stream` - Stream generation with real-time updates (SSE)

## Configuration

### Backend Environment Variables

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
MAX_ITERATIONS=3
VIRALITY_THRESHOLD=85
```

### Frontend Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Troubleshooting

### "API keys not configured"
- Make sure `backend/.env` file exists and contains valid API keys
- Check that you're in the correct directory

### "No response from server"
- Make sure the backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`

### "Module not found" (Backend)
- Activate your virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### "Module not found" (Frontend)
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

### CORS errors
- Make sure backend CORS is configured for your frontend URL
- Check `backend/main.py` CORS settings

## Performance

Target: < 2 minutes per generation (PRD requirement)

Typical performance:
- Research: 5-10 seconds
- First draft: 10-15 seconds
- Review + iterations: 10-30 seconds
- **Total**: 30-60 seconds average

## License

This project is for educational and personal use.

## Credits

Built with LangGraph, Groq API, Tavily API, Next.js, and FastAPI.

---

**Ready to make boring topics go viral?** 🚀
