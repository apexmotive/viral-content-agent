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
        # Preserve the original path from the rewrite
        # Vercel rewrites /api/generate to /api/index, but we need the original path
        original_path = event.get('path', '')
        
        # If the path is /api/index (from rewrite), get the original from query or headers
        if original_path == '/api/index' or original_path.endswith('/api/index'):
            # Try to get original path from Vercel's rewrite info
            # The original path should be in the request
            request_path = event.get('rawPath', '') or event.get('requestContext', {}).get('http', {}).get('path', '')
            if request_path and request_path != original_path:
                # Update the path in the event
                event['path'] = request_path
            else:
                # Try to reconstruct from the rewrite pattern
                # Vercel passes the original path in the event
                # Check if there's a way to get it from headers or query
                headers = event.get('headers', {}) or {}
                # Some Vercel setups pass x-vercel-original-path
                original = headers.get('x-vercel-original-path') or headers.get('x-original-path')
                if original:
                    event['path'] = original
        
        # Debug logging
        print(f"Handler called - path: {event.get('path')}, method: {event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method')}", flush=True)
        
        return mangum_handler(event, context)
    except Exception as e:
        # Log error for debugging
        print(f"Error in handler: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        raise

