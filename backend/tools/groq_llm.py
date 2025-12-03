"""Groq LLM integration for content generation using LangChain."""

from langchain_groq import ChatGroq
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


def generate_content(
    prompt: str,
    model: str = None,
    temperature: float = 0.7,
    max_tokens: int = 2000
) -> str:
    """
    Generate content using Groq's LLM via LangChain.
    
    Args:
        prompt: The prompt to send to the LLM
        model: Model name (defaults to config.GROQ_MODEL)
        temperature: Creativity level (0.0-2.0)
        max_tokens: Maximum tokens in response
        
    Returns:
        Generated text from the LLM
    """
    try:
        if model is None:
            model = config.GROQ_MODEL
        
        logger.info(f"Generating content with model: {model}")
        
        # Initialize ChatGroq from langchain-groq
        llm = ChatGroq(
            api_key=config.GROQ_API_KEY,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        # Invoke the LLM
        response = llm.invoke(prompt)
        
        # Extract content from response
        content = response.content
        logger.info(f"Generated {len(content)} characters")
        
        return content
        
    except Exception as e:
        logger.error(f"Error generating content with Groq: {str(e)}")
        raise
