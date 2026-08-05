"""
api/routes/chat.py
Chat endpoints with streaming support.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from api.schemas import ChatRequest, ChatResponse, HistoryResponse, MessageItem
from core.chat_engine import ChatEngine
import uuid
import json

router    = APIRouter(prefix="/chat", tags=["Chat"])
_sessions: dict = {}


def _get_or_create_engine(session_id: str) -> ChatEngine:
    """Return the existing session's engine, or create a new one."""
    if session_id not in _sessions:
        _sessions[session_id] = ChatEngine()
    return _sessions[session_id]


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """Send a message to Homer and stream the response token by token."""
    session_id = request.session_id or str(uuid.uuid4())
    engine     = _get_or_create_engine(session_id)

    def generate():
        try:
            for item in engine.chat_stream(request.message):
                if isinstance(item, dict) and item.get("done"):
                    # Final chunk of the stream — includes citations for this response
                    done_data = json.dumps({
                        "done":       True,
                        "citations":  item["citations"],
                        "session_id": session_id
                    })
                    yield f"data: {done_data}\n\n"
                else:
                    # Regular token
                    yield f"data: {json.dumps({'token': item})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control":               "no-cache",
            "X-Accel-Buffering":           "no",
            "Access-Control-Allow-Origin": "*",
        }
    )


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to Homer and get back a complete (non-streamed) response."""
    session_id = request.session_id or str(uuid.uuid4())
    try:
        engine               = _get_or_create_engine(session_id)
        response, citations  = engine.chat(request.message)
        return ChatResponse(
            response=response,
            citations=citations,
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=HistoryResponse)
async def get_history(session_id: str):
    """Return the full conversation history for a given session."""
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found.")
    history  = _sessions[session_id].get_history()
    messages = [MessageItem(role=m["role"], content=m["content"])
                for m in history]
    return HistoryResponse(messages=messages)


@router.delete("/reset/{session_id}")
async def reset_session(session_id: str):
    """Clear a session's memory and remove it from the active session store."""
    if session_id in _sessions:
        _sessions[session_id].reset()
        del _sessions[session_id]
        return {"message": f"Session {session_id} reset successfully."}
    raise HTTPException(status_code=404, detail="Session not found.")