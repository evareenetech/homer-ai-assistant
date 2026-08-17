# Homer — Greek Mythology AI Assistant

An AI-powered assistant that embodies Homer, the ancient Greek poet, guiding users through Greek mythology with cited, source-grounded answers. Built on a local RAG pipeline (Ollama + ChromaDB) with an interactive React + D3 family tree.

---

### ✨ Features

- **Homer persona** — conversational AI grounded in classical sources, not generic LLM knowledge
- **RAG knowledge base** — every answer is retrieved from and cited against primary texts (Iliad, Odyssey, Theogony, Homeric Hymns, and more)
- **Interactive family tree** — D3-rendered graph of 66 gods, titans, and heroes across 104 relationships, with 7 curated views
- **Streaming chat** — token-by-token responses
- **Fully local & private** — conversations run in-memory only; nothing is written to disk, no accounts, no external calls beyond the local Ollama server

---

### 📦 Stack

**Backend** — Python · FastAPI · Ollama (Llama 3 8B) · ChromaDB · sentence-transformers · NetworkX  
**Frontend** — React 19 · Vite · Tailwind CSS · D3.js · React Router  
**Testing** — pytest · httpx (35 tests across unit, integration, and API layers)

---

### 🚀 Quick start

**Prerequisites:** Python 3.11+, Node.js 18+, [Ollama](https://ollama.com)

```bash
ollama pull llama3
```

**Backend**
```bash
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn api.main:app --reload
```
API docs available at `http://localhost:8000/docs`.

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

---

### 🤖 How it works

1. User sends a message to `/chat/` or `/chat/stream`
2. The message is embedded (`all-MiniLM-L6-v2`) and matched against a ChromaDB vector store of curated mythology chunks
3. The top 3 relevant chunks are injected into a RAG prompt alongside conversation history
4. Ollama (Llama 3) generates a response in Homer's voice, grounded in the retrieved context
5. The response streams back token by token, along with the sources it drew from

Full design rationale and data flow diagrams: [docs/architecture.md](docs/architecture.md)

---

### 📁 Project structure

```
homer-ai-assistant/
├── api/          # FastAPI routes and request/response schemas
├── core/         # Chat engine, memory, persona, citation tracking
├── rag/          # Embedding, vector store, retrieval pipeline
├── mythology/    # Family tree data (66 figures, 104 relationships) + graph engine
├── data/         # Knowledge base chunks (mythology_chunks.json)
├── frontend/     # React + Vite web app
└── tests/        # 35 tests across unit, integration, and API layers
```

---

### 🔌 API endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/chat/` | Send a message, get a complete response |
| POST | `/chat/stream` | Send a message, stream the response |
| GET | `/chat/history` | Get a session's conversation history |
| DELETE | `/chat/reset/{session_id}` | Clear a session |
| GET | `/family-tree/` | Full graph data |
| GET | `/family-tree/{name}` | Full info on a figure |
| GET | `/family-tree/{name}/children`, `/parents`, `/siblings` | Relationship queries |
| GET | `/family-tree/{name}/path/{target}` | Shortest relationship path between two figures |

---

### 📚 Classical sources

Homer — *Iliad*, *Odyssey*  
Hesiod — *Theogony*  
Homeric Hymns (*Apollo*, *Demeter*, *Hermes*, *Artemis*)  
Apollodorus — *The Library*

---

### 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

### 👤 Author

**Evareene Tech** — [github.com/evareenetech](https://github.com/evareenetech)

---

### 🎞️ Demo

[(https://github.com/user-attachments/assets/b9730be9-deb2-4dc4-9291-ca85a3648722)](https://github.com/user-attachments/assets/b9730be9-deb2-4dc4-9291-ca85a3648722)

---
