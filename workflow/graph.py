"""LangGraph workflow orchestration for viral content generation."""

from typing import Literal
from langgraph.graph import StateGraph, END
from workflow.state import ContentState
from agents.trend_scout import trend_scout_agent
from agents.ghostwriter import ghostwriter_agent
from agents.chief_editor import chief_editor_agent
from utils.logger import setup_logger
import config

logger = setup_logger(__name__)


def should_continue(state: ContentState) -> Literal["revise", "end"]:
    """
    Determine if content needs revision or is approved.
    
    Args:
        state: Current workflow state
        
    Returns:
        "revise" if needs more work, "end" if approved or max iterations reached
    """
    status = state.get('status', '')
    iteration_count = state.get('iteration_count', 0)
    
    # Check if we hit max iterations
    if iteration_count >= config.MAX_ITERATIONS:
        logger.warning(f"⚠️ Max iterations ({config.MAX_ITERATIONS}) reached")
        return "end"
    
    # Check if content is approved
    if status == 'approved':
        return "end"
    
    # Check if we need revision
    if status == 'needs_revision':
        return "revise"
    
    # Check for errors
    if status == 'failed' or 'error' in state:
        return "end"
    
    return "end"


def increment_iteration(state: ContentState) -> ContentState:
    """Increment iteration counter before revision."""
    current = state.get('iteration_count', 0)
    logger.info(f"🔄 Starting iteration {current + 1}/{config.MAX_ITERATIONS}")
    return {
        **state,
        'iteration_count': current + 1
    }


def create_workflow():
    """
    Create and compile the LangGraph workflow.
    
    Returns:
        Compiled workflow graph
    """
    # Initialize the graph
    workflow = StateGraph(ContentState)
    
    # Add nodes
    workflow.add_node("trend_scout", trend_scout_agent)
    workflow.add_node("ghostwriter", ghostwriter_agent)
    workflow.add_node("chief_editor", chief_editor_agent)
    workflow.add_node("increment", increment_iteration)
    
    # Define the flow
    workflow.set_entry_point("trend_scout")
    
    # Sequential flow: research -> draft -> review
    workflow.add_edge("trend_scout", "ghostwriter")
    workflow.add_edge("ghostwriter", "chief_editor")
    
    # Conditional edge: review -> revise or end
    workflow.add_conditional_edges(
        "chief_editor",
        should_continue,
        {
            "revise": "increment",
            "end": END
        }
    )
    
    # After incrementing, go back to ghostwriter
    workflow.add_edge("increment", "ghostwriter")
    
    # Compile the workflow
    app = workflow.compile()
    
    logger.info("✅ Workflow compiled successfully")
    return app


def run_workflow(topic: str, platform: str = "twitter"):
    """
    Run the complete viral content generation workflow.
    
    Args:
        topic: The topic to create content about
        platform: "twitter" or "linkedin"
        
    Returns:
        Final state with generated content
    """
    logger.info(f"🚀 Starting workflow for topic: '{topic}' on {platform}")
    
    # Initialize state
    initial_state: ContentState = {
        'topic': topic,
        'platform': platform.lower(),
        'research_angles': [],
        'draft_content': '',
        'virality_score': 0,
        'editor_feedback': '',
        'iteration_count': 0,
        'final_content': '',
        'status': 'initialized',
        'error': None
    }
    
    # Create and run workflow
    app = create_workflow()
    final_state = app.invoke(initial_state)
    
    logger.info(f"✅ Workflow complete with status: {final_state.get('status')}")
    
    return final_state
