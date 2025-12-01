"""Shared state schema for the viral content workflow."""

from typing import TypedDict, List, Dict, Optional


class ContentState(TypedDict):
    """State that flows through the LangGraph workflow."""
    
    # Input
    topic: str
    platform: str  # "twitter" or "linkedin"
    
    # Research phase
    research_angles: List[Dict]
    
    # Drafting phase
    draft_content: str
    
    # Review phase
    virality_score: int
    editor_feedback: str
    
    # Control flow
    iteration_count: int
    final_content: str
    status: str  # "researching", "drafting", "reviewing", "approved", "failed"
    
    # Error handling
    error: Optional[str]
