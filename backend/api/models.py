"""Pydantic models for API request/response validation."""

from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field


class GenerationSettings(BaseModel):
    """Settings for content generation."""
    model: str = Field(default="meta-llama/llama-4-scout-17b-16e-instruct")
    max_iterations: int = Field(default=3, ge=1, le=5)
    virality_threshold: int = Field(default=85, ge=50, le=100)


class GenerateRequest(BaseModel):
    """Request model for content generation."""
    topic: str = Field(..., min_length=1, max_length=500)
    platform: Literal["twitter", "linkedin"] = Field(default="twitter")
    settings: GenerationSettings = Field(default_factory=GenerationSettings)


class ResearchAngle(BaseModel):
    """Research angle from Trend Scout."""
    title: str
    why_viral: str
    summary: str
    sources: List[str] = []


class GenerateResponse(BaseModel):
    """Response model for content generation."""
    final_content: str
    virality_score: int
    iterations: int
    elapsed_time: float
    drafts: List[str]
    scores: List[int]
    research_angles: List[ResearchAngle]
    feedbacks: List[str]
    status: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str


class ModelsResponse(BaseModel):
    """Available models response."""
    models: List[str]
