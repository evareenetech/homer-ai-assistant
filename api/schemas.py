"""
schemas.py
Pydantic models that define the shape of every API request and response.
These act as contracts — FastAPI validates all incoming data against them
automatically, rejecting malformed requests before they reach our code.
"""

from pydantic import BaseModel, Field


# ── Chat schemas ──────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    """What the client sends when starting or continuing a conversation."""
    message: str = Field(..., min_length=1, max_length=2000,
                         description="The user's message to Homer")
    session_id: str | None = Field(None,
                         description="Session ID for conversation continuity")


class ChatResponse(BaseModel):
    """What Homer sends back after processing a message."""
    response: str           = Field(..., description="Homer's response")
    citations: list[str]    = Field(..., description="Classical sources cited")
    session_id: str         = Field(..., description="Session ID for follow-up messages")


class MessageItem(BaseModel):
    """A single message in a conversation history."""
    role: str               = Field(..., description="user or assistant")
    content: str            = Field(..., description="Message content")


class HistoryResponse(BaseModel):
    """A full conversation history."""
    messages: list[MessageItem] = Field(..., description="Conversation messages")


# ── Family tree schemas ───────────────────────────────────────────────────────

class FigureInfo(BaseModel):
    """Basic info about a mythological figure."""
    name: str               = Field(..., description="Name of the figure")
    category: str           = Field(..., description="olympian, titan, hero, etc.")
    description: str        = Field(..., description="Brief description")
    source: str             = Field(..., description="Classical source")


class FigureDetail(BaseModel):
    """Full detail about a figure including all relationships."""
    name: str
    category: str
    description: str
    source: str
    parents:     list[FigureInfo] = []
    children:    list[FigureInfo] = []
    siblings:    list[FigureInfo] = []
    spouses:     list[FigureInfo] = []
    ancestors:   list[FigureInfo] = []
    descendants: list[FigureInfo] = []


class PathResponse(BaseModel):
    """The relationship path between two figures."""
    from_figure: str        = Field(..., description="Starting figure")
    to_figure:   str        = Field(..., description="Target figure")
    path:        list[str]  = Field(..., description="Steps in the path")
    found:       bool       = Field(..., description="Whether a path was found")


class TreeData(BaseModel):
    """Full graph data for frontend visualisation."""
    nodes: list             = Field(..., description="All mythology figures")
    edges: list             = Field(..., description="All relationships")


# ── General schemas ───────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    """Standard error response shape."""
    error:   str            = Field(..., description="Error message")
    detail:  str | None     = Field(None, description="Additional detail")


class HealthResponse(BaseModel):
    """API health check response."""
    status:  str            = Field(..., description="ok or degraded")
    version: str            = Field(..., description="API version")
    message: str            = Field(..., description="Status message")