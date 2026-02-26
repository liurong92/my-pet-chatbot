# My Pet Chatbot

Using AI (Claude), RAG, MCP, and Memory to answer questions about your pets.

## Features

**Multi-Format Document Support**
- PDF files — extracts text from PDF documents
- TXT files — reads plain text files
- Automatic loading on startup

**Smart Memory System**
- Conversation history stored in vector database
- Semantic search for relevant context
- Separate collections for system resources and conversations

**AI-Powered Chatbot**
- Claude Sonnet for intelligent responses
- MCP (Model Context Protocol) for tool integration
- RAG (Retrieval-Augmented Generation) for accurate answers

**Web Interface**
- React chat UI served at `http://localhost:8000`
- REST API for frontend/backend communication
- Session-based conversation history

**Vector Database**
- Qdrant for fast similarity search
- Docker-based deployment

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Web Browser (React UI)                      │
│               http://localhost:8000                      │
└───────────────────┬─────────────────────────────────────┘
                    │  HTTP (JSON)
                    ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Server (api_server.py)              │
│  POST /api/chat     POST /api/reset    GET /api/health   │
│  - Session history management                            │
│  - Serves React production build                         │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              Pet System Agent (pet_system_agent.py)      │
│  - Claude Sonnet model                                   │
│  - Orchestrates queries                                  │
│  - Responds in Chinese                                   │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │    MCP Service       │
         │  (mcp_service.py)    │
         │  - search_memory     │
         │  - get_pet_info      │
         └──────────┬───────────┘
                    │
                    ▼
         ┌──────────────────────────────┐
         │    Qdrant Vector Database    │
         │  ┌────────────────────────┐  │
         │  │  system-resource       │  │
         │  │  (PDF/TXT content)     │  │
         │  └────────────────────────┘  │
         │  ┌────────────────────────┐  │
         │  │  ai-collection         │  │
         │  │  (Conversation history)│  │
         │  └────────────────────────┘  │
         └──────────────────────────────┘
```

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) — for Qdrant
- [uv](https://github.com/astral-sh/uv) — Python package manager
- [Node.js](https://nodejs.org/) (v18+) — for building the React frontend
- An Anthropic API key

---

## Step-by-Step Setup

### Step 1 — Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2 — Set your API key

```bash
export ANTHROPIC_API_KEY=your_key_here
```

> To use Gemini instead, set `GOOGLE_API_KEY` and change `MODEL_NAME` in `pet_system_agent.py`.

### Step 3 — Install Python dependencies

```bash
uv sync
```

### Step 4 — Start Qdrant (vector database)

```bash
docker-compose up -d
```

Verify it is running:
```bash
curl -s http://localhost:6333/health
```

Expected:
```json
{"title":"qdrant - vector search engine","version":"..."}
```

### Step 5 — Build the React frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

This produces `frontend/dist/`, which the FastAPI server will serve automatically.

### Step 6 — Start the web server

```bash
uv run python api_server.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
[API]: Loading pet data into vector store...
[SYSTEM]: Loading PDF file: Global-State-of-Pet-Health-Draft.pdf
[SYSTEM]: Upserting 26 points to collection 'system-resource'
[SYSTEM]: Loading TXT file: pet_information.txt
[SYSTEM]: Upserting 2 points to collection 'system-resource'
[API]: Pet data loaded. Server is ready.
```

### Step 7 — Open the chat UI

Visit **http://localhost:8000** in your browser.

---

## API Reference

The FastAPI server exposes three endpoints:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/chat` | Send a message and receive a response |
| `POST` | `/api/reset` | Clear a session's conversation history |

### POST /api/chat

Request:
```json
{
  "message": "What is Rong's pet name?",
  "session_id": "optional-uuid-to-continue-a-conversation"
}
```

Response:
```json
{
  "response": "Rong 的宠物名字是 April 🐱",
  "session_id": "df1b9aa7-6ca8-4e86-91ca-fb59a40765f7"
}
```

Pass the returned `session_id` in subsequent requests to maintain conversation context.

### POST /api/reset

Request:
```json
{
  "session_id": "df1b9aa7-6ca8-4e86-91ca-fb59a40765f7"
}
```

Response:
```json
{
  "message": "Session reset successfully.",
  "session_id": "df1b9aa7-6ca8-4e86-91ca-fb59a40765f7"
}
```

---

## CLI Mode (no web UI)

If you prefer the terminal interface:

```bash
uv run python run.py
```

```
********** Please ask any question about pet. **********

> April 是谁？

======================== Answer =======================
April 是 Rong 的宠物猫！...
==========================End==========================

> exit
```

---

## Frontend Development

To run the React app with hot-reload during development:

```bash
# Terminal 1 — backend
uv run python api_server.py

# Terminal 2 — frontend dev server
cd frontend
npm run dev
```

Open **http://localhost:5173** — the dev server proxies `/api/*` to `localhost:8000` automatically.

---

## Run Tests

```bash
uv run python test_run.py
```

Tests verify pet information queries using the RAG pipeline.

---

## Adding Pet Data

Put `.txt` or `.pdf` files in the `resource/` directory. They are loaded automatically into the `system-resource` Qdrant collection every time the server starts.

---

> References: [qdrant-client](https://python-client.qdrant.tech/) · [FastMCP](https://modelcontextprotocol.io/docs/develop/build-server) · [pydantic-ai](https://ai.pydantic.dev/)

## License

This project is open source and available under the [MIT License](LICENSE).
