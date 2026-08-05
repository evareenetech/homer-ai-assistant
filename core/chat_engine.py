"""
chat_engine.py
Core chat engine with streaming support — yields tokens from Ollama
as they're generated for real-time UI updates.
"""

import ollama
import os
import logging
from collections.abc import Generator

from core.persona import get_system_prompt, build_rag_prompt
from core.memory import ConversationMemory
from core.citations import CitationManager
from rag.vector_store import VectorStore
from rag.retriever import Retriever

logger = logging.getLogger(__name__)

OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL",    "llama3")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


class ChatEngine:
    def __init__(self):
        logger.info("Initializing ChatEngine...")
        self.memory           = ConversationMemory()
        self.vector_store     = VectorStore()
        self.vector_store.load_and_embed_knowledge()
        self.retriever        = Retriever(self.vector_store)
        self.citation_manager = CitationManager()
        self.system_prompt    = get_system_prompt()
        logger.info("Homer is ready.")

    def _retrieve(self, user_message: str):
        """
        Run RAG retrieval and return context string and
        deduplicated citations for this specific message.
        """
        rag_results = self.retriever.retrieve(user_message, n_results=3)
        context     = self.retriever.format_context(rag_results)

        # citations here are per-message (this retrieval only) — kept separate
        # from citation_manager, which tracks sources across the whole session
        citations = self.retriever.get_citations(rag_results)

        self.citation_manager.add_citations(citations)
        return context, citations

    def _build_messages(self, rag_prompt: str) -> list:
        """
        Build the full message list for Ollama including
        system prompt and recent conversation history.
        Including history lets Homer remember what was
        already discussed in the current session.
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        messages += self.memory.get_recent(n=10)
        messages.append({"role": "user", "content": rag_prompt})
        return messages

    def chat(self, user_message: str) -> tuple:
        """
        Non-streaming chat.
        Returns a tuple of (response_text, citations).
        Used as a fallback when streaming is not available.
        """
        logger.info("User: %s", user_message)

        context, citations = self._retrieve(user_message)
        rag_prompt         = build_rag_prompt(user_message, context)
        messages           = self._build_messages(rag_prompt)

        response          = ollama.chat(model=OLLAMA_MODEL, messages=messages)
        assistant_message = response["message"]["content"]

        self.memory.add_message("user",      user_message)
        self.memory.add_message("assistant", assistant_message)

        logger.info("Homer responded (%d chars)", len(assistant_message))
        return assistant_message, citations

    def chat_stream(self, user_message: str) -> Generator:
        """
        Streaming chat — yields tokens one at a time as Ollama
        generates them, then yields a final done dict with citations.

        Yield types:
          - str: a single token to append to the UI
          - dict: {"done": True, "citations": [...]} signals end of stream

        Why yield a dict at the end instead of a separate method?
        It keeps the entire message lifecycle — tokens + citations —
        in a single generator that the API route can iterate over cleanly.
        """
        logger.info("Streaming: %s", user_message)

        context, citations = self._retrieve(user_message)
        rag_prompt         = build_rag_prompt(user_message, context)
        messages           = self._build_messages(rag_prompt)

        # Store user message before streaming starts so the history
        # is correct even if the stream is interrupted
        self.memory.add_message("user", user_message)

        full_response = ""
        stream = ollama.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            token          = chunk["message"]["content"]
            full_response += token
            yield token

        # Store the complete response once streaming finishes
        self.memory.add_message("assistant", full_response)
        logger.info("Stream complete (%d chars)", len(full_response))

        # Final signal for this stream — citations are already deduplicated by _retrieve()
        yield {"done": True, "citations": citations}

    def get_history(self) -> list:
        """Return the full conversation history for display."""
        return self.memory.get_history()

    def get_citations(self) -> list:
        """Return all citations used across the entire session."""
        return self.citation_manager.get_all()

    def reset(self):
        """Clear conversation memory and citations for this session."""
        self.memory.clear()
        self.citation_manager.clear()
        logger.info("Session reset.")