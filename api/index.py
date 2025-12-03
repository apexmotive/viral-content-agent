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
    mangum_handler = Mangum(app, lifespan="off")
finally:
    os.chdir(original_cwd)

# Export handler for Vercel (required)
# Vercel Python functions need a handler function that takes (event, context)
def handler(event, context):
    """Vercel serverless function handler."""
    try:
        return mangum_handler(event, context)
    except Exception as e:
        # Log error for debugging
        print(f"Error in handler: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        raise

