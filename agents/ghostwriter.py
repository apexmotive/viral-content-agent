"""Ghostwriter Agent - The Hook Master."""

from typing import Dict
from tools.groq_llm import generate_content
from utils.logger import setup_logger

logger = setup_logger(__name__)


def ghostwriter_agent(state: Dict) -> Dict:
    """
    Create viral content based on research angles.
    
    Args:
        state: Current workflow state with research_angles
        
    Returns:
        Updated state with draft_content
    """
    topic = state['topic']
    platform = state['platform']
    angles = state['research_angles']
    feedback = state.get('editor_feedback', '')
    
    logger.info(f"✍️ Ghostwriter crafting {platform} content for: {topic}")
    
    try:
        # Build the prompt based on platform
        if platform.lower() == 'twitter':
            prompt = build_twitter_prompt(topic, angles, feedback)
        else:
            prompt = build_linkedin_prompt(topic, angles, feedback)
        
        # Generate content with higher temperature for creativity
        draft = generate_content(prompt, temperature=0.9, max_tokens=1500)
        
        logger.info(f"✅ Draft created ({len(draft)} chars)")
        
        # Update drafts history
        current_drafts = state.get('drafts', [])
        new_drafts = current_drafts + [draft]
        
        return {
            **state,
            'draft_content': draft,
            'drafts': new_drafts,
            'status': 'drafting_complete'
        }
        
    except Exception as e:
        logger.error(f"❌ Ghostwriter error: {str(e)}")
        return {
            **state,
            'error': str(e),
            'status': 'failed'
        }


def build_twitter_prompt(topic: str, angles: list, feedback: str = '') -> str:
    """Build prompt for Twitter thread generation."""
    
    # Format angles
    angles_text = "\n".join([
        f"- {angle['title']}: {angle['summary']}" 
        for angle in angles[:3]
    ])
    
    feedback_section = f"\n\nIMPORTANT FEEDBACK TO ADDRESS:\n{feedback}" if feedback else ""
    
    return f"""You are a viral Twitter ghostwriter. Create a compelling Twitter thread about "{topic}".

RESEARCH ANGLES TO USE:
{angles_text}

TWITTER THREAD REQUIREMENTS:
1. Start with a KILLER HOOK - make them stop scrolling
   - Use a shocking statistic, question, or contrarian take
   - First tweet must be punchy (under 280 chars)

2. Thread Structure (8-12 tweets):
   - Hook (tweet 1)
   - Context/problem (tweets 2-3)
   - Main insights using the angles above (tweets 4-8)
   - Actionable takeaway or call-to-action (tweet 9-10)
   - Closing hook/summary (final tweet)

3. Formatting:
   - Short sentences (under 20 words)
   - Use line breaks for readability (like a poem)
   - Strategic emoji use (2-3 per tweet max, meaningful only)
   - Number the tweets (1/10, 2/10, etc.)
   - NO bolding or markdown headers (no # or **)

4. Writing Style:
   - Poetic but professional
   - Short, punchy lines
   - Friendly, slightly humorous tone
   - Balance casual and professional
   - Use "you" to speak directly to reader

5. Virality Elements:
   - Controversial or surprising angles
   - Relatable examples
   - Quotable one-liners
   - Emotional resonance{feedback_section}

Write the complete thread now. Each tweet should be separated by a line that says "---"
"""


def build_linkedin_prompt(topic: str, angles: list, feedback: str = '') -> str:
    """Build prompt for LinkedIn post generation."""
    
    # Format angles
    angles_text = "\n".join([
        f"- {angle['title']}: {angle['summary']}" 
        for angle in angles[:3]
    ])
    
    feedback_section = f"\n\nIMPORTANT FEEDBACK TO ADDRESS:\n{feedback}" if feedback else ""
    
    return f"""You are a viral LinkedIn ghostwriter. Create an engaging LinkedIn post about "{topic}".

RESEARCH ANGLES TO USE:
{angles_text}

LINKEDIN POST REQUIREMENTS:
1. POWERFUL OPENING (First 2 lines):
   - Hook them before "see more" cut-off
   - Use a bold statement, question, or story opening
   - Make it personal or provocative

2. Post Structure:
   - Hook (2 lines)
   - Story or context (1 paragraph)
   - Main insights using angles (3-4 short paragraphs)
   - Actionable takeaway
   - Call-to-action or thought-provoking question

3. Formatting:
   - Single-line paragraphs for scannability
   - White space is your friend (like a poem)
   - NO titles or headers (no # or ##)
   - NO bolding (**text**) - plain text only
   - Strategic use of emojis (3-5 total)

4. Writing Style:
   - Short, punchy lines
   - Friendly, realistic humor
   - Balance casual and professional
   - Transitions must be smooth and natural
   - No "Here is a post" or meta-commentary

5. Virality Elements:
   - Counter-intuitive insights
   - Relatable professional scenarios
   - Quotable wisdom
   - Spark conversation in comments{feedback_section}

Write the complete LinkedIn post now.
"""
