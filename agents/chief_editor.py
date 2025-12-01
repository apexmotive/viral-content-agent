"""Chief Editor Agent - The Virality Gatekeeper."""

import re
from typing import Dict, Tuple
from tools.groq_llm import generate_content
from utils.logger import setup_logger
import config

logger = setup_logger(__name__)


def chief_editor_agent(state: Dict) -> Dict:
    """
    Review and score content for virality.
    
    Args:
        state: Current workflow state with draft_content
        
    Returns:
        Updated state with virality_score and editor_feedback
    """
    draft = state['draft_content']
    platform = state['platform']
    topic = state['topic']
    
    logger.info(f"⚖️ Chief Editor reviewing {platform} content")
    
    try:
        # Get LLM review
        score, feedback = review_content(draft, platform, topic)
        
        logger.info(f"📊 Virality Score: {score}/100")
        
        # Determine if approved
        threshold = config.VIRALITY_THRESHOLD
        approved = score >= threshold
        
        if approved:
            logger.info(f"✅ Content APPROVED (score {score} >= {threshold})")
            
            # ACTIVE EDITOR: Apply the polish yourself!
            if score < 100:
                logger.info("✨ Applying final polish based on feedback...")
                final_polished = apply_polish(draft, feedback, platform)
            else:
                final_polished = draft
                
            return {
                **state,
                'virality_score': score,
                'editor_feedback': feedback,
                'final_content': final_polished,
                'status': 'approved'
            }
        else:
            logger.info(f"❌ Content NEEDS REVISION (score {score} < {threshold})")
            logger.info(f"Feedback: {feedback[:100]}...")
            return {
                **state,
                'virality_score': score,
                'editor_feedback': feedback,
                'status': 'needs_revision'
            }
        
    except Exception as e:
        logger.error(f"❌ Chief Editor error: {str(e)}")
        return {
            **state,
            'error': str(e),
            'status': 'failed'
        }


def apply_polish(draft: str, feedback: str, platform: str) -> str:
    """Apply specific feedback to polish the content."""
    
    polish_prompt = f"""You are an expert Chief Editor. 
    
    TASK: Polish this social media post based on the feedback below.
    
    CRITICAL RULES:
    1. DO NOT rewrite the whole thing. Only fix what needs fixing.
    2. Maintain the original voice and style (poetic, short lines).
    3. Ensure NO markdown formatting (no #, no **).
    4. Keep it clean and professional.
    
    FEEDBACK TO APPLY:
    {feedback}
    
    ORIGINAL CONTENT:
    {draft}
    
    Output ONLY the polished content.
    """
    
    return generate_content(polish_prompt, temperature=0.3)


def review_content(draft: str, platform: str, topic: str) -> Tuple[int, str]:
    """
    Use LLM to review content and provide virality score + feedback.
    
    Returns:
        Tuple of (score, feedback)
    """
    
    review_prompt = f"""You are a Chief Editor evaluating social media content for virality potential.

PLATFORM: {platform.upper()}
TOPIC: {topic}

CONTENT TO REVIEW:
---
{draft}
---

SCORING CRITERIA (100 points total):

1. HOOK STRENGTH (30 points):
   - Does it stop the scroll?
   - Is it specific, bold, or surprising?
   - Does it promise clear value?
   - Deduct points for generic, boring, or clickbait hooks

2. EMOJI USAGE (20 points):
   - Are emojis used tastefully?
   - Do they add meaning or just clutter?
   - Too few = boring, too many = cringe
   - Deduct for random or excessive emoji use

3. STRUCTURE & RHYTHM (25 points):
   - Is it scannable with white space?
   - Varied sentence/paragraph length?
   - Logical flow and pacing?
   - Deduct for walls of text or choppy rhythm

4. PLATFORM OPTIMIZATION (25 points):
   - Twitter: Thread format, tweet length, numbered properly
   - LinkedIn: Hook before cutoff, professional tone, story-driven
   - Deduct for poor formatting or wrong tone

RESPONSE FORMAT (CRITICAL - FOLLOW EXACTLY):
SCORE: [number 0-100]

FEEDBACK:
[Provide 2-3 SPECIFIC, ACTIONABLE improvements. Be direct.]

Examples of good feedback:
- "Hook is weak. Try starting with: 'Most people think X, but data shows Y...' "
- "Too many emojis in paragraph 2. Remove 🔥 and keep only one relevant icon"
- "Thread tweet 3 is 320 chars - cut by 40 chars. Try: [specific rewrite]"

Now review the content:"""

    response = generate_content(review_prompt, temperature=0.3)
    
    # Parse score and feedback
    score = extract_score(response)
    feedback = extract_feedback(response)
    
    return score, feedback


def extract_score(response: str) -> int:
    """Extract virality score from LLM response."""
    # Look for "SCORE: XX" pattern
    match = re.search(r'SCORE:\s*(\d+)', response, re.IGNORECASE)
    if match:
        score = int(match.group(1))
        return min(100, max(0, score))  # Clamp to 0-100
    
    # Fallback: look for any number near beginning
    match = re.search(r'(\d+)/100', response)
    if match:
        return int(match.group(1))
    
    # Default to neutral score if parsing fails
    logger.warning("Could not parse score, defaulting to 70")
    return 70


def extract_feedback(response: str) -> str:
    """Extract feedback from LLM response."""
    # Look for "FEEDBACK:" section
    parts = response.split('FEEDBACK:', 1)
    if len(parts) > 1:
        return parts[1].strip()
    
    # Fallback: return everything after the score
    parts = re.split(r'SCORE:\s*\d+', response, 1)
    if len(parts) > 1:
        return parts[1].strip()
    
    return response.strip()
