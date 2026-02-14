# My pet chatbot

Using AI(Claude), and RAG, MCP and Memory to communication

## Features

✨ **Multi-Format Document Support**
- 📄 PDF files - Extracts text from PDF documents
- 📝 TXT files - Reads plain text files
- 🔄 Automatic loading on startup

🧠 **Smart Memory System**
- 💾 Conversation history stored in vector database
- 🔍 Semantic search for relevant context
- 📚 Separate collections for system resources and conversations

🤖 **AI-Powered Chatbot**
- 🎯 Claude Sonnet 4.5 for intelligent responses
- 🛠️ MCP (Model Context Protocol) for tool integration
- 🔗 RAG (Retrieval-Augmented Generation) for accurate answers

🗄️ **Vector Database**
- ⚡ Qdrant for fast similarity search
- 🌐 RESTful API for easy querying
- 📦 Docker-based deployment

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│                      (run.py)                            │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              Pet System Agent                            │
│           (pet_system_agent.py)                          │
│  - Orchestrates queries                                  │
│  - Manages conversation flow                             │
└───────────────┬─────────────────┬───────────────────────┘
                │                 │
                ▼                 ▼
    ┌──────────────────┐  ┌──────────────────┐
    │   MCP Service    │  │   Pet Agent      │
    │ (mcp_service.py) │  │ (pet_agent.py)   │
    │ - search_memory  │  │ - Get pet info   │
    │ - get_pet_info   │  └──────────────────┘
    └─────────┬────────┘
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

## Step-by-Step Demo

### Step 1: Start Qdrant Database

```bash
docker-compose up -d
```

**Expected Output:**
```
Creating network "my-pet-chatbot_default" with the default driver
Creating volume "my-pet-chatbot_qdrant_storage" with default driver
Creating qdrant ... done
```

Verify Qdrant is running:
```bash
curl -s http://localhost:6333/health
```

**Expected Output:**
```json
{
  "title": "qdrant - vector search engine",
  "version": "1.x.x"
}
```

### Step 2: Install Dependencies

```bash
uv sync
```

**Expected Output:**
```
Resolved 50 packages in 2.5s
Downloaded 10 packages in 1.2s
Installed 50 packages in 1.5s
 + anthropic==0.x.x
 + pydantic-ai==1.56.0
 + qdrant-client==1.16.2
 + fastembed==0.7.4
 + pypdf==6.6.2
 ... (more packages)
```

### Step 3: Run the Chatbot

```bash
uv run python run.py
```

**Expected Output:**
```
[SYSTEM]: Load resource data...
[SYSTEM]: Loading PDF file: Global-State-of-Pet-Health-Draft.pdf
[SYSTEM]: create and update memory...
[SYSTEM]: Upserting 26 points to collection 'system-resource'
[SYSTEM]: Successfully loaded 26 items from Global-State-of-Pet-Health-Draft.pdf
[SYSTEM]: Loading TXT file: pet_information.txt
[SYSTEM]: create and update memory...
[SYSTEM]: Upserting 2 points to collection 'system-resource'
[SYSTEM]: Successfully loaded 2 items from pet_information.txt

********** Please ask any question about pet. **********

>
```

### Step 4: Ask Questions

**Example Conversation:**

```
> April 是谁？

[TOOL]: Start searching memery data...
[SYSTEM]: Search memory from ai-collection...
[TOOL]: Get pet information...
[SYSTEM]: Search memory from system-resource...

======================== Answer =======================
April 是 Rong 的宠物猫！

以下是 April 的信息：
- 类型：猫
- 性别：雌性（母猫）
- 颜色：三花猫 - 橘色、白色和黑色
- 喜好：喜欢睡觉和跑步
- 特点：喜欢找塑料袋！
==========================End==========================

> April 喜欢什么？

[TOOL]: Start searching memery data...
[SYSTEM]: Search memory from ai-collection...

======================== Answer =======================
根据我的记忆，April 喜欢：

🐱 April 的喜好：
- 💤 睡觉
- 🏃 跑步
- 🛍️ 找塑料袋（这是她的特别爱好！）
==========================End==========================

> 有哪些宠物？

[TOOL]: Start searching memery data...
[SYSTEM]: Search memory from ai-collection...
[TOOL]: Get pet information...
[SYSTEM]: Search memory from system-resource...

======================== Answer =======================
根据我的记忆和查询，目前系统中有以下宠物：

🐱 1. April
- 类型：猫
- 性别：雌性（母猫）
- 颜色：三花猫（橘色、白色和黑色）
- 喜好：喜欢睡觉、跑步、找塑料袋

🐱 2. 711
- 主人：Lan
- 类型：猫
- 性别：雄性（公猫）
- 颜色：黑白两色
- 喜好：喜欢抓球
==========================End==========================

> exit
```

### Step 5: Verify Data in Qdrant

Check collections:
```bash
curl -s http://localhost:6333/collections | jq
```

**Expected Output:**
```json
{
  "result": {
    "collections": [
      {
        "name": "system-resource"
      },
      {
        "name": "ai-collection"
      }
    ]
  }
}
```

Check collection info:
```bash
curl -s http://localhost:6333/collections/system-resource | jq
```

**Expected Output:**
```json
{
  "result": {
    "status": "green",
    "vectors_count": 28,
    "points_count": 28,
    "indexed_vectors_count": 28
  }
}
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
