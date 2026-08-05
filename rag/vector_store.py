"""
vector_store.py
Manages the ChromaDB vector database. Handles storing and
retrieving embedded mythology knowledge chunks.
"""

import chromadb
import json
import os
import logging
from typing import Any
from rag.embedder import Embedder

logger = logging.getLogger(__name__)

COLLECTION_NAME = "greek_mythology"
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "mythology_chunks.json")


class VectorStore:
    def __init__(self, persist_directory: str = "./data/chroma_db"):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedder = Embedder()
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("Collection '%s' ready. Documents stored: %d",
                    COLLECTION_NAME, self.collection.count())

    def is_populated(self) -> bool:
        """Check if the vector store already has data."""
        return self.collection.count() > 0

    def load_and_embed_knowledge(self):
        """
        Read mythology_chunks.json, embed each chunk, and store in ChromaDB.
        Only runs if the collection is empty to avoid duplicates.
        """
        if self.is_populated():
            logger.info("Knowledge base already populated. Skipping.")
            return

        logger.info("Loading mythology knowledge base...")
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        ids = [chunk["id"] for chunk in chunks]
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [
            {
                "source": chunk["source"],
                "category": chunk["category"],
                "tags": ", ".join(chunk["tags"])
            }
            for chunk in chunks
        ]

        logger.info("Embedding %d chunks...", len(texts))
        embeddings = self.embedder.embed_many(texts)

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )
        logger.info("%d chunks embedded and stored.", len(texts))

    def query(self, query_text: str, n_results: int = 3) -> list[dict[str, Any]]:
        """
        Find the most semantically similar chunks to the user's query.
        Returns a list of results with text, source, and similarity score.
        """
        query_embedding = self.embedder.embed(query_text)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

        formatted = []
        for i in range(len(results["documents"][0])):
            formatted.append({
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "category": results["metadatas"][0][i]["category"],
                "score": round(1 - results["distances"][0][i], 4)
            })

        return formatted