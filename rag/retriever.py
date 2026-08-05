"""
retriever.py
The retriever is the public interface for the RAG pipeline.
It takes a user question and returns relevant mythology knowledge
chunks along with their sources for citation.
"""

import logging
from typing import Any
from rag.vector_store import VectorStore

logger = logging.getLogger(__name__)

# Minimum similarity score to include a result (0 to 1)
SIMILARITY_THRESHOLD = 0.3


class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve(self, query: str, n_results: int = 3) -> list[dict[str, Any]]:
        """
        Retrieve the most relevant mythology knowledge for a given query.
        Filters out results below the similarity threshold.
        """
        results = self.vector_store.query(query, n_results=n_results)

        # Filter by similarity threshold
        filtered = [r for r in results if r["score"] >= SIMILARITY_THRESHOLD]

        if not filtered:
            logger.info("No relevant chunks found for query: '%s'", query)
        else:
            logger.info("Found %d relevant chunks.", len(filtered))
            for r in filtered:
                logger.info("  - Score: %s | Source: %s", r['score'], r['source'])

        return filtered

    def format_context(self, results: list[dict[str, Any]]) -> str:
        """Format retrieved results into a single context string for the LLM prompt."""
        if not results:
            return "No specific mythology knowledge found for this query."

        context_parts = []
        for result in results:
            context_parts.append(
                f"[{result['source']}]\n{result['text']}"
            )

        return "\n\n".join(context_parts)

    def get_citations(self, results: list[dict[str, Any]]) -> list[str]:
        """
        Extract unique source citations from results.
        """
        seen = set()
        citations = []
        for result in results:
            source = result["source"]
            if source not in seen:
                seen.add(source)
                citations.append(source)
        return citations