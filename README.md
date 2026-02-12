# My pet chatbot

Using AI(Claude), and RAG, MCP and Memory to communication

## Quick Start

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Set your Claude API Key

You should have Claude account

```bash
# Claude
export ANTHROPIC_API_KEY=xxxx
```

### Or setup Gemini api

#### Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key
5. Set it as an environment variable:

#### Change agent model
```python
from pydantic_ai import Agent

agent = Agent(
    model='anthropic:claude-sonnet-4-5',
    instructions='Your insructions here',
)
```

```bash
# Gemini
export GEMINI_API_KEY=xxxx
```

### Run project

```bash
# Sync dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate

# Run mcp service
mcp dev mcp_service.py

# Run project
uv run python run.py

```

## License

This project is open source and available under the [MIT License](LICENSE).
