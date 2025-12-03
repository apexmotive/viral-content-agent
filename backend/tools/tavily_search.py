"""Tavily API integration for trend research."""

from typing import List, Dict
from tavily import TavilyClient
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


def search_trending_content(topic: str, max_results: int = 5) -> List[Dict]:
    """
    Search for trending content, news, and angles related to a topic.
    
    Args:
        topic: The topic to research
        max_results: Maximum number of results to return
        
    Returns:
        List of search results with title, url, and content
    """
    try:
        client = TavilyClient(api_key=config.TAVILY_API_KEY)
        
        # Search for trending and recent content
        query = f"{topic} trending news viral discussions latest"
        
        logger.info(f"Searching Tavily for: {query}")
        
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_answer=True
        )
        
        results = []
        for item in response.get('results', []):
            results.append({
                'title': item.get('title', ''),
                'url': item.get('url', ''),
                'content': item.get('content', ''),
                'score': item.get('score', 0)
            })
        
        # Add the AI-generated answer if available
        if response.get('answer'):
            logger.info(f"Tavily answer: {response['answer'][:100]}...")
        
        logger.info(f"Found {len(results)} results for topic: {topic}")
        return results
        
    except Exception as e:
        logger.error(f"Error searching Tavily: {str(e)}")
        raise
