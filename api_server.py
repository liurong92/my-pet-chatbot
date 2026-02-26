"""
Pet Chatbot API Server

FastAPI server that exposes the pet chatbot as an HTTP API for the React frontend.
"""

from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from init import load_pet_data, create_and_update_memory, DataType
from pet_system_agent import pet_system_agent

# ---------------------------------------------------------------------------
# Lifespan (startup)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[API]: Loading pet data into vector store...")
    load_pet_data()
    print("[API]: Pet data loaded. Server is ready.")
    yield


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(title="Pet Chatbot API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store: session_id -> list of pydantic-ai messages
_sessions: dict[str, list] = {}


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


class ResetResponse(BaseModel):
    message: str
    session_id: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # Resolve or create session
    session_id = req.session_id or str(uuid.uuid4())
    history = _sessions.get(session_id, [])

    try:
        result = await pet_system_agent.run(req.message, message_history=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")

    # Persist updated history
    _sessions[session_id] = result.all_messages()

    # Save interaction to Qdrant memory
    try:
        create_and_update_memory(
            collection_name="ai-collection",
            update_data=[f"Question: {req.message}, Answer: {result.output}"],
            data_type=DataType.AI,
        )
    except Exception:
        pass  # memory persistence failure should not break the API response

    return ChatResponse(response=result.output, session_id=session_id)


@app.post("/api/reset", response_model=ResetResponse)
async def reset(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    _sessions.pop(session_id, None)
    return ResetResponse(message="Session reset successfully.", session_id=session_id)


# ---------------------------------------------------------------------------
# Serve React frontend (production build)
# ---------------------------------------------------------------------------

import os

FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "frontend", "dist")

if os.path.isdir(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

    @app.get("/", include_in_schema=False)
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend(full_path: str = ""):
        index = os.path.join(FRONTEND_DIST, "index.html")
        if os.path.isfile(index):
            return FileResponse(index)
        raise HTTPException(status_code=404, detail="Frontend not built yet. Run: cd frontend && npm run build")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
