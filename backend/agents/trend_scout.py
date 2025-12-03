"""Trend Scout Agent - The Angle Hunter."""

from typing import Dict, List
from tools.tavily_search import search_trending_content
from tools.groq_llm import generate_content
from utils.logger import setup_logger

logger = setup_logger(__name__)


def trend_scout_agent(state: Dict) -> Dict:
    """
    Research trending angles for a topic using Tavily.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with research_angles populated
    """
    topic = state['topic']
    logger.info(f"🕵️ Trend Scout researching: {topic}")
    
    try:
        # Search for trending content
        search_results = search_trending_content(topic, max_results=5)
        
        # Use LLM to analyze and identify the best angles
        analysis_prompt = f"""You are a viral content researcher. Analyze these search results about "{topic}" and identify 3-5 unique angles that could make this topic go viral on social media.

Search Results:
{format_search_results(search_results)}

For each angle, provide:
1. A catchy title
2. Why it's viral-worthy (connection to trends, controversy, universal pain point, etc.)
3. A brief summary

Focus on angles that are:
- Surprising or contrarian
- Connected to current events or trends
- Emotionally resonant
- Universally relatable

Format as:
ANGLE 1: [Title]
WHY VIRAL: [Reason]
SUMMARY: [Brief summary]

ANGLE 2: ...
"""
        
        analysis = generate_content(analysis_prompt, temperature=0.8)
        
        # Parse the angles
        angles = parse_angles(analysis, search_results)
        
        logger.info(f"✅ Found {len(angles)} viral angles")
        
        return {
            **state,
            'research_angles': angles,
            'status': 'researching_complete'
        }
        
    except Exception as e:
        logger.error(f"❌ Trend Scout error: {str(e)}")
        return {
            **state,
            'error': str(e),
            'status': 'failed'
        }


def format_search_results(results: List[Dict]) -> str:
    """Format search results for LLM analysis."""
    formatted = []
    for i, result in enumerate(results, 1):
        formatted.append(f"""
Result {i}:
Title: {result['title']}
Content: {result['content'][:300]}...
URL: {result['url']}
""")
    return "\n".join(formatted)


def parse_angles(analysis: str, search_results: List[Dict]) -> List[Dict]:
    """Parse the LLM analysis into structured angles."""
    angles = []
    
    # Split by "ANGLE" keyword
    parts = analysis.split('ANGLE ')[1:]  # Skip first empty part
    
    for part in parts:
        lines = part.strip().split('\n')
        if len(lines) >= 3:
            angle = {
                'title': lines[0].split(':', 1)[-1].strip() if ':' in lines[0] else lines[0].strip(),
                'why_viral': extract_field(part, 'WHY VIRAL'),
                'summary': extract_field(part, 'SUMMARY'),
                'sources': [r['url'] for r in search_results[:2]]  # Include top sources
            }
            angles.append(angle)
    
    # Fallback: If parsing fails, create basic angles from search results
    if not angles and search_results:
        for result in search_results[:3]:
            angles.append({
                'title': result['title'],
                'why_viral': 'Trending topic with high engagement',
                'summary': result['content'][:200],
                'sources': [result['url']]
            })
    
    return angles


def extract_field(text: str, field_name: str) -> str:
    """Extract a field value from formatted text."""
    for line in text.split('\n'):
        if field_name in line:
            return line.split(':', 1)[-1].strip()
    return ''
