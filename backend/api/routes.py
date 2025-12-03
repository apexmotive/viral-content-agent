"""API routes for the Viral Content Agent."""

import time
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json

from api.models import (
    GenerateRequest,
    GenerateResponse,
    HealthResponse,
    ModelsResponse,
    ResearchAngle
)
from workflow.graph import run_workflow
import config

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Validate config
        config.validate_config()
        return HealthResponse(
            status="healthy",
            message="Viral Content Agent API is running"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models", response_model=ModelsResponse)
async def get_models():
    """Get available Groq models."""
    models = [
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "meta-llama/llama-4-maverick-17b-128e-instruct",
        "openai/gpt-oss-120b",
        "llama-3.3-70b-versatile"
    ]
    return ModelsResponse(models=models)


@router.post("/generate", response_model=GenerateResponse)
async def generate_content(request: GenerateRequest):
    """
    Generate viral content for a given topic.
    
    This endpoint runs the complete multi-agent workflow:
    1. Trend Scout researches viral angles
    2. Ghostwriter creates content
    3. Chief Editor reviews and scores
    4. Loop until approved or max iterations
    """
    try:
        # Validate config
        config.validate_config()
        
        # Track time
        start_time = time.time()
        
        # Run workflow
        final_state = run_workflow(
            request.topic, 
            request.platform,
            request.settings.max_iterations,
            request.settings.virality_threshold
        )
        
        elapsed_time = time.time() - start_time
        
        # Extract research angles
        research_angles = []
        for angle in final_state.get('research_angles', []):
            research_angles.append(
                ResearchAngle(
                    title=angle.get('title', 'Untitled'),
                    why_viral=angle.get('why_viral', 'N/A'),
                    summary=angle.get('summary', 'N/A'),
                    sources=angle.get('sources', [])
                )
            )
        
        # Build response
        response = GenerateResponse(
            final_content=final_state.get('final_content', '') or final_state.get('draft_content', ''),
            virality_score=final_state.get('virality_score', 0),
            iterations=final_state.get('iteration_count', 0),
            elapsed_time=elapsed_time,
            drafts=final_state.get('drafts', []),
            scores=final_state.get('scores', []),
            research_angles=research_angles,
            feedbacks=final_state.get('feedbacks', []),
            status=final_state.get('status', 'unknown')
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


async def generate_content_stream(request: GenerateRequest) -> AsyncGenerator[str, None]:
    """
    Stream content generation progress using Server-Sent Events.
    
    This is an alternative endpoint for real-time updates.
    """
    try:
        # Update config (only model needs global update if used by tools directly)
        config.GROQ_MODEL = request.settings.model
        
        # Send initial event
        yield f"data: {json.dumps({'type': 'status', 'message': 'Starting workflow...'})}\n\n"
        
        start_time = time.time()
        
        # Run workflow (in future, this could be modified to yield progress)
        final_state = run_workflow(
            request.topic, 
            request.platform,
            request.settings.max_iterations,
            request.settings.virality_threshold
        )
        
        elapsed_time = time.time() - start_time
        
        # Extract research angles
        research_angles = []
        for angle in final_state.get('research_angles', []):
            research_angles.append({
                'title': angle.get('title', 'Untitled'),
                'why_viral': angle.get('why_viral', 'N/A'),
                'summary': angle.get('summary', 'N/A'),
                'sources': angle.get('sources', [])
            })
        
        # Send final result
        result = {
            'type': 'complete',
            'data': {
                'final_content': final_state.get('final_content', '') or final_state.get('draft_content', ''),
                'virality_score': final_state.get('virality_score', 0),
                'iterations': final_state.get('iteration_count', 0),
                'elapsed_time': elapsed_time,
                'drafts': final_state.get('drafts', []),
                'scores': final_state.get('scores', []),
                'research_angles': research_angles,
                'feedbacks': final_state.get('feedbacks', []),
                'status': final_state.get('status', 'unknown')
            }
        }
        
        yield f"data: {json.dumps(result)}\n\n"
        
    except Exception as e:
        error_data = {
            'type': 'error',
            'message': str(e)
        }
        yield f"data: {json.dumps(error_data)}\n\n"


@router.post("/generate/stream")
async def generate_content_streaming(request: GenerateRequest):
    """
    Stream content generation with real-time updates.
    Uses Server-Sent Events (SSE) for progress updates.
    """
    return StreamingResponse(
        generate_content_stream(request),
        media_type="text/event-stream"
    )
