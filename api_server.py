"""
Pet Chatbot API Server

FastAPI server that exposes the pet chatbot as an HTTP API for the React frontend.
"""

from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from init import load_pet_data, create_and_update_memory, DataType
from pet_system_agent import pet_system_agent, create_agent

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


# ---------------------------------------------------------------------------
# Session store
# ---------------------------------------------------------------------------

@dataclass
class SessionData:
    messages: list = field(default_factory=list)
    api_key: Optional[str] = None
    model: Optional[str] = None


# session_id -> SessionData
_sessions: dict[str, SessionData] = {}


def _get_or_create_session(session_id: Optional[str]) -> tuple[str, SessionData]:
    sid = session_id or str(uuid.uuid4())
    if sid not in _sessions:
        _sessions[sid] = SessionData()
    return sid, _sessions[sid]


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class SettingsRequest(BaseModel):
    session_id: Optional[str] = None
    api_key: str
    model: str


class SettingsResponse(BaseModel):
    session_id: str
    model: str


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


@app.post("/api/settings", response_model=SettingsResponse)
async def update_settings(req: SettingsRequest):
    """Store api_key and model server-side; return session_id for future requests."""
    sid, session = _get_or_create_session(req.session_id)
    session.api_key = req.api_key
    session.model = req.model
    return SettingsResponse(session_id=sid, model=req.model)


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    session_id, session = _get_or_create_session(req.session_id)

    try:
        if session.api_key and session.model:
            agent = create_agent(session.model, session.api_key)
        else:
            agent = pet_system_agent
        result = await agent.run(req.message, message_history=session.messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")

    session.messages = result.all_messages()

    try:
        create_and_update_memory(
            collection_name="ai-collection",
            update_data=[f"Question: {req.message}, Answer: {result.output}"],
            data_type=DataType.AI,
        )
    except Exception:
        pass

    return ChatResponse(response=result.output, session_id=session_id)


@app.post("/api/reset", response_model=ResetResponse)
async def reset(req: ChatRequest):
    session_id, session = _get_or_create_session(req.session_id)
    # Clear messages but keep api_key/model settings
    session.messages = []
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
