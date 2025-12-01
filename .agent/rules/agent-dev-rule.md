---
trigger: always_on
---

AI Agent Project Structure
When building AI Agent applications (single or multi-agent), always follow this modular structure to ensure clean separation of concerns, scalability, and maintainability.

Core Principles
Separation of Concerns: Never mix agent logic, tool definitions, and application entry points in a single file.
Configuration Management: Always use environment variables for secrets and configuration.
Modularity: Tools and agents should be defined as independent, reusable modules.
Standard Directory Layout
project_root/
├── .env                # Secrets (API keys, etc.) - NEVER commit this
├── .env.example        # Template for secrets
├── requirements.txt    # Dependencies
├── README.md           # Documentation
├── main.py             # Entry point (CLI or Server)
├── config.py           # Configuration loader (optional for simple apps)
├── agents/             # Agent definitions
│   ├── __init__.py
│   ├── base.py         # Shared agent logic (optional)
│   └── research_agent.py
├── tools/              # Tool definitions
│   ├── __init__.py
│   ├── web_search.py
│   └── file_ops.py
└── utils/              # Shared utilities (logging, helpers)
    ├── __init__.py
    └── logger.py

Add a workflow/ directory if we're building multi-agents.

Pls always create a new environment for our app.