# Viral Content Agent Team 🚀

Transform boring topics into viral social media content using AI agents!

## Overview

The Viral Content Agent Team is a multi-agent system that automatically creates engaging Twitter threads and LinkedIn posts. It uses three specialized AI agents working together:

- **🕵️ Trend Scout**: Researches viral angles using Tavily API
- **✍️ Ghostwriter**: Creates compelling content using Groq LLM
- **⚖️ Chief Editor**: Reviews and scores content for virality (with feedback loop)

## Features

✨ **Intelligent Research**: Finds trending angles and connections for any topic  
🎯 **Platform-Optimized**: Different formatting for Twitter threads vs LinkedIn posts  
🔄 **Feedback Loop**: Iteratively improves content until it meets virality threshold  
📊 **Virality Scoring**: Evaluates hook strength, emoji usage, structure, and platform optimization  
🎨 **Beautiful UI**: Modern Streamlit interface with real-time progress tracking

## Installation

### 1. Clone or navigate to the project

```bash
cd /Users/admin/Projects/viral-content-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

#### Getting API Keys

- **Groq API**: Sign up at [console.groq.com](https://console.groq.com) (Free tier available)
- **Tavily API**: Sign up at [tavily.com](https://tavily.com) (Free tier: 1000 requests/month)

## Usage

### Run the Streamlit App

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Interface

1. **Enter a topic** (even boring technical topics work great!)
   - Example: "Database Normalization"
   - Example: "Supply Chain Logistics"
   
2. **Select platform**: Twitter or LinkedIn

3. **Click "Generate Viral Content"**

4. **Watch the agents work**:
   - Trend Scout researches angles
   - Ghostwriter creates draft
   - Chief Editor scores and provides feedback
   - Loop repeats until content scores ≥85 or max iterations reached

5. **Download your viral content** ready to post!

## Architecture

```
viral-content-agent/
├── agents/              # Agent implementations
│   ├── trend_scout.py   # Research agent (Tavily)
│   ├── ghostwriter.py   # Content creation (Groq)
│   └── chief_editor.py  # Review & scoring (Groq)
├── tools/               # API integrations
│   ├── tavily_search.py # Tavily wrapper
│   └── groq_llm.py      # Groq wrapper
├── workflow/            # LangGraph orchestration
│   ├── state.py         # Shared state schema
│   └── graph.py         # Workflow definition
├── utils/               # Utilities
│   └── logger.py        # Logging
├── main.py             # Streamlit UI
└── config.py           # Configuration
```

## Configuration

Edit `.env` to customize:

```env
# Model selection
GROQ_MODEL=llama-3.3-70b-versatile

# Workflow settings
MAX_ITERATIONS=3          # Max revision loops
VIRALITY_THRESHOLD=85     # Minimum score to approve
```

## Examples

### Input
- **Topic**: "Database Normalization"
- **Platform**: Twitter

### Output
A 10-tweet thread with:
- Killer hook connecting databases to a trending tech story
- Clear explanation with analogies
- Viral-worthy insights and contrarian takes
- Strategic emoji usage
- Perfect Twitter formatting

## How It Works

1. **Research Phase**: Trend Scout searches Tavily for trending discussions, news, and viral angles related to your topic

2. **Creation Phase**: Ghostwriter uses those angles to craft platform-specific content with attention to hooks, structure, and readability

3. **Review Phase**: Chief Editor scores the content (0-100) based on:
   - Hook Strength (30 pts)
   - Emoji Usage (20 pts)
   - Structure & Rhythm (25 pts)
   - Platform Optimization (25 pts)

4. **Iteration**: If score < 85, specific feedback is sent back to Ghostwriter for revision (max 3 iterations)

5. **Approval**: Once score ≥ 85 or max iterations reached, content is delivered

## Troubleshooting

### "API keys not configured"
- Make sure `.env` file exists and contains valid API keys
- Check that you're in the correct directory

### "Module not found"
- Activate your virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Content not viral enough
- Try a different topic or angle
- Adjust `VIRALITY_THRESHOLD` in `.env` (though this may reduce quality)
- The system learns what works through the feedback loop

## Performance

Target: < 2 minutes per generation (PRD requirement)

Typical performance:
- Research: 5-10 seconds
- First draft: 10-15 seconds
- Review + iterations: 10-30 seconds
- **Total**: 30-60 seconds average

## Tech Stack

- **LangGraph**: Multi-agent workflow orchestration
- **Groq**: High-speed LLM inference (Llama models)
- **Tavily**: AI-optimized search API
- **Streamlit**: Modern web interface
- **Python 3.8+**

## License

This project is for educational and personal use.

## Credits

Built with LangGraph, Groq API, and Tavily API.

---

**Ready to make boring topics go viral?** 🚀
