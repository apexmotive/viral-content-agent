"""FastAPI backend for Viral Content Agent Team."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
import config

# Initialize FastAPI app
app = FastAPI(
    title="Viral Content Agent API",
    description="Multi-agent system for creating viral social media content",
    version="2.0.0"
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:3001",
        "https://*.vercel.app",   # Vercel preview/production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Viral Content Agent API",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.on_event("startup")
async def startup_event():
    """Validate configuration on startup."""
    try:
        config.validate_config()
        print("✅ Configuration validated successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        raise


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
