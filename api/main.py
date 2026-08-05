import logging
from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, family_tree
from api.schemas import HealthResponse

API_VERSION = "1.0.0"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("homer.api")


# ── Lifespan ──────────────────────────────────────────────────────────────────
# Define lifespan BEFORE app = FastAPI(...) so it exists when referenced
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run startup and shutdown logging for the API lifecycle."""
    logger.info("Starting Homer API...")
    logger.info("Homer API ready.")
    yield


# ── App definition ────────────────────────────────────────────────────────────
app = FastAPI(
    lifespan=lifespan,
    title="Homer — Greek Mythology AI Assistant",
    description="""
An AI-powered assistant that acts as Homer, guiding users through Greek Mythology.

## Features
- **Homer Persona** — Converse with Homer, the ancient Greek poet
- **RAG Knowledge Base** — Answers grounded in classical sources
- **Family Tree** — Explore relationships between gods, titans, and heroes
- **Privacy First** — Conversations run in-memory by default; nothing is written to disk
- **Citations** — Every answer references classical texts

## Classical Sources
Iliad, Odyssey, Theogony, Homeric Hymns, Apollodorus's Library
    """,
    version=API_VERSION,
    contact={
        "name": "Homer Project",
    }
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(chat.router)
app.include_router(family_tree.router)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/", response_model=HealthResponse, tags=["Health"])
async def root():
    """API health check — confirms Homer is running."""
    return HealthResponse(
        status="ok",
        version=API_VERSION,
        message="Homer is ready to guide you through Greek Mythology."
    )