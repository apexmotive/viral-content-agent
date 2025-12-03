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
        if isinstance(event, dict):
            # Log event for debugging
            print(f"Handler called - Event keys: {list(event.keys())}", flush=True)
            print(f"Path: {event.get('path')}", flush=True)
            print(f"Method: {event.get('httpMethod')}", flush=True)
            print(f"Query params: {event.get('queryStringParameters')}", flush=True)
            print(f"Headers: {event.get('headers')}", flush=True)
            
            # If path is /api/index, try to get the original path from query or headers
            current_path = event.get('path', '')
            if current_path == '/api/index' or current_path.endswith('/api/index'):
                # Try to get original path from query parameter (if rewrite passed it)
                query_params = event.get('queryStringParameters') or {}
                if query_params and 'path' in query_params:
                    original_path = f"/api/{query_params['path']}"
                    print(f"Reconstructing path from query: {original_path}", flush=True)
                    event['path'] = original_path
                else:
                    # Try headers
                    headers = event.get('headers') or {}
                    if isinstance(headers, dict):
                        original = (headers.get('x-vercel-original-path') or 
                                  headers.get('x-original-path') or
                                  headers.get('x-invoke-path'))
                        if original:
                            print(f"Using original path from headers: {original}", flush=True)
                            event['path'] = original
        
        # Pass event to Mangum
        response = mangum_handler(event, context)
        
        print(f"Response status: {response.get('statusCode') if isinstance(response, dict) else 'N/A'}", flush=True)
        return response
    except Exception as e:
        # Log error for debugging
        print(f"Error in handler: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        raise

