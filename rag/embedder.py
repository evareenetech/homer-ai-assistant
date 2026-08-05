"""
embedder.py
Converts text chunks into vector embeddings using a local
sentence-transformers model. No data leaves the machine.
"""

import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class Embedder:
    def __init__(self):
        logger.info("Loading model: %s", EMBEDDING_MODEL)
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        logger.info("Model loaded successfully.")

    def embed(self, text: str) -> list[float]:
        """Convert a single string into a vector embedding."""
        embedding = self.model.encode(text)
        return embedding.tolist()

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        """Convert a list of strings into a list of vector embeddings."""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()