"""Configuration management for the Viral Content Agent."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Model Configuration
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Application Settings
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "3"))
VIRALITY_THRESHOLD = int(os.getenv("VIRALITY_THRESHOLD", "85"))

# Validation
def validate_config():
    """Validate that required configuration is present."""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    if not TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY not found in environment variables")
    return True
