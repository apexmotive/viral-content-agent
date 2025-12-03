"""Shared state schema for the viral content workflow."""

from typing import TypedDict, List, Dict, Optional


class ContentState(TypedDict):
    """State that flows through the LangGraph workflow."""
    
    # Input
    topic: str
    platform: str  # "twitter" or "linkedin"
    
    # Configuration
    max_iterations: int
    virality_threshold: int
    
    # Research phase
    research_angles: List[Dict]
    
    # Drafting phase
    draft_content: str
    drafts: List[str]  # History of all drafts created
    
    # Review phase
    virality_score: int
    scores: List[int]  # History of scores
    editor_feedback: str
    feedbacks: List[str]  # History of feedback
    
    # Control flow
    iteration_count: int
    final_content: str
    status: str  # "researching", "drafting", "reviewing", "approved", "failed"
    
    # Error handling
    error: Optional[str]
