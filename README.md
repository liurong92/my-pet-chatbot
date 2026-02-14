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

# Run docker compose for vector db
docker-compose up

# Run project
uv run python run.py

```
Or you can use the personal script to run the project
```bash
# Sync dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate

# Run mcp service
mpet start-mcp

# Run docker compose for vector db
mpet start-db

# Run project
mpet run-project

```

### Run tests

You can run automated tests to verify the chatbot functionality:

```bash
# Run the test script
uv run python test_run.py
```

The test script will:
- Load PDF and TXT files from the `resource/` directory
- Test multiple pet information queries
- Verify RAG and memory functionality
- Display results for each test question

> notes:
> [qdrant-client](https://python-client.qdrant.tech/) /
> [Fast MCP](https://modelcontextprotocol.io/docs/develop/build-server)


## License

This project is open source and available under the [MIT License](LICENSE).
