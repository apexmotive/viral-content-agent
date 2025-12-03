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
# The handler variable is what Vercel will use

