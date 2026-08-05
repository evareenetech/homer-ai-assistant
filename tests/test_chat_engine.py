"""
test_chat_engine.py
Tests for the Homer persona, memory system, and chat engine.
"""

import pytest
from core.persona import get_system_prompt, build_rag_prompt
from core.memory import ConversationMemory
from core.citations import CitationManager
from core.chat_engine import ChatEngine


def test_persona_system_prompt():
    prompt = get_system_prompt()
    assert "Homer" in prompt
    assert "Greek mythology" in prompt
    assert len(prompt) > 100
    print("\n✅ Persona: system prompt loaded correctly")


def test_persona_rag_prompt():
    prompt = build_rag_prompt(
        user_message="Who is Zeus?",
        context="[Source 1: Hesiod - Theogony]\nZeus is the king of the gods..."
    )
    assert "Zeus" in prompt
    assert "Hesiod" in prompt
    print("✅ Persona: RAG prompt built correctly")


def test_memory():
    memory = ConversationMemory()
    memory.add_message("user", "Who is Zeus?")
    memory.add_message("assistant", "Zeus is the king of the gods.")
    assert len(memory.get_history()) == 2
    memory.clear()
    assert memory.is_empty()
    print("✅ Memory: incognito mode working")


def test_citation_manager():
    cm = CitationManager()
    cm.add_citations(["Hesiod - Theogony", "Homer - Iliad"])
    cm.add_citations(["Hesiod - Theogony"])  # duplicate — should not add again
    assert len(cm.get_all()) == 2
    formatted = cm.format_citations()
    assert "Hesiod" in formatted
    cm.clear()
    assert len(cm.get_all()) == 0
    print("✅ Citations: manager working correctly")


def test_chat_engine_full():
    engine = ChatEngine()
    response, citations = engine.chat("Tell me about Zeus, king of the gods.")
    assert len(response) > 50
    assert not engine.memory.is_empty()
    assert len(citations) > 0
    print(f"\n✅ ChatEngine: full pipeline working")
    print(f"   Response preview: {response[:200]}...")
    print(f"   Citations: {citations}")