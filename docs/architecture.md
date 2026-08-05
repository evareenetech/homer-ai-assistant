# Homer — Architecture & Design Decisions

## Overview

Homer is a locally-run AI assistant built around a RAG (Retrieval-Augmented 
Generation) pipeline. Every component was chosen deliberately with three goals 
in mind: privacy, accuracy, and portfolio demonstrability.

---

## Architecture Diagram
```
User Request
│
▼
FastAPI (api/main.py)
│
├── /chat ──────────────► ChatEngine
│ │
│ ┌─────────┴─────────┐
│ ▼ ▼
│ RAG Pipeline Memory Layer
│ (retriever.py) (in-memory, per session)
│ │
│ VectorStore
│ (ChromaDB local)
│ │
│ Embedder
│ (all-MiniLM-L6-v2)
│ │
│ Ollama LLM
│ (Llama 3 8B)
│
└── /family-tree ──► MythologyGraph (NetworkX)
```

---

## Key Design Decisions

### 1. Why local LLM (Ollama + Llama 3)?

The alternative was a cloud API (OpenAI, Anthropic, Groq). We chose local for 
three reasons:

- **Privacy** — user conversations never leave the machine. No third party 
  ever sees the data.
- **Cost** — completely free, no API keys, no rate limits.
- **Portfolio signal** — running a local LLM demonstrates understanding of 
  the AI stack beyond just calling an API.

Llama 3 8B was chosen over smaller models (Mistral 7B, Phi-2) because it 
produces significantly better prose quality for the Homer persona, handles 
multi-turn conversation well, and fits comfortably in consumer hardware RAM.

### 2. Why RAG instead of fine-tuning?

Fine-tuning would mean retraining Llama 3 on Greek mythology data — an 
expensive, time-consuming process requiring a GPU. RAG achieves the same 
accuracy goal by retrieval: we store our knowledge externally and inject 
relevant passages into the prompt at query time.

RAG has additional advantages for this use case:
- **Updatable** — adding new knowledge means adding JSON chunks, not 
  retraining a model
- **Citable** — we know exactly which source informed each answer
- **Transparent** — the retrieved context is inspectable for debugging

### 3. Why ChromaDB for the vector store?

ChromaDB runs entirely locally (no server needed), has a clean Python API, 
and persists embeddings to disk so the knowledge base only gets embedded once. 
For a local portfolio project it is the right tool — production systems would 
use Pinecone or Weaviate for scale.

### 4. Why sentence-transformers for embeddings?

The `all-MiniLM-L6-v2` model produces 384-dimensional embeddings that are 
fast, accurate for semantic similarity tasks, and small enough (~90MB) to 
run on CPU without a GPU. It consistently scores well on semantic textual 
similarity benchmarks for English text.

Cosine similarity was chosen as the distance metric because it measures the 
angle between vectors rather than their magnitude — better for comparing 
text meaning regardless of passage length.

### 5. Why NetworkX for the family tree?

The Greek mythology family tree is fundamentally a graph problem — figures 
are nodes, relationships are directed edges. NetworkX gives us:
- Shortest path algorithms (find connection between any two figures)
- Traversal (get all descendants of Cronus)
- Easy JSON export for frontend visualisation

The graph is built once at startup and held in memory — at 66 nodes and 104 
edges it is tiny and never needs to be rebuilt.

### 6. Why session-only memory (no persistence)?

Homer has no user accounts and isn't intended to be hosted publicly — it's a 
local portfolio project. Persisting conversations to a database would add 
real complexity (schema, migrations, cleanup) without a real use case: 
there's no login to scope the data to, and no server to keep it safe on.

Instead, `ConversationMemory` holds each session's messages in a plain Python 
list, in RAM, for as long as the chat stays open. Refreshing the page or 
restarting the server clears it. This keeps the privacy story simple — 
nothing is ever written to disk — without building account infrastructure 
this project doesn't need.

### 7. Why FastAPI?

FastAPI was chosen over Flask or Django for three reasons:
- **Performance** — async by default, one of the fastest Python frameworks
- **Auto-documentation** — Swagger UI at /docs with zero extra code
- **Pydantic integration** — request validation is declarative, not manual

The router-per-domain pattern (chat.py, family_tree.py) keeps the codebase 
navigable as it grows and mirrors how production APIs are structured.

---

## Data Flow — Chat Request

1. Client sends `POST /chat/` with `{message, session_id}`
2. FastAPI validates the request against `ChatRequest` schema (Pydantic)
3. `chat.py` retrieves or creates a `ChatEngine` for the session
4. `ChatEngine.chat()` calls `Retriever.retrieve()` with the user message
5. `Retriever` embeds the query using `all-MiniLM-L6-v2`
6. ChromaDB returns the 3 most semantically similar mythology chunks
7. `build_rag_prompt()` injects the chunks into the prompt as context
8. The full message history + RAG prompt is sent to Ollama (Llama 3)
9. Llama 3 generates a response in Homer's voice, citing the sources
10. The exchange is stored in memory for the duration of the session
11. `ChatResponse` is returned with response, citations, and session_id

---

## Data Flow — Family Tree Request

1. Client sends `GET /family-tree/Zeus`
2. FastAPI routes to `family_tree.py`
3. The module-level `MythologyGraph` instance handles the query
4. NetworkX traverses the directed graph to find parents, children, siblings
5. Results are serialised to `FigureDetail` Pydantic model
6. JSON response returned

---

## Project Structure Rationale
```
homer-ai-assistant/
├── api/ # HTTP layer only — no business logic here
├── core/ # Business logic — chat, memory, persona, citations
├── rag/ # AI pipeline — embeddings, vector store, retrieval
├── mythology/ # Domain data — family tree, graph queries
├── data/ # Knowledge base JSON (mythology_chunks.json)
└── tests/ # One test file per module
```

Each layer only depends on layers below it. `api/` calls `core/`, `core/` 
calls `rag/` and `mythology/`, nothing calls `api/`. This prevents circular 
imports and makes each layer independently testable.