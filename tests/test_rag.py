"""
test_rag.py
Tests for the RAG pipeline: embedder, vector store, and retriever.
"""

import pytest
from rag.embedder import Embedder
from rag.vector_store import VectorStore
from rag.retriever import Retriever


def test_embedder_single():
    embedder = Embedder()
    result = embedder.embed("Who is Zeus?")
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], float)
    print(f"\n✅ Embedder: generated vector of length {len(result)}")


def test_embedder_many():
    embedder = Embedder()
    results = embedder.embed_many(["Zeus is king", "Poseidon rules the sea"])
    assert len(results) == 2
    print("✅ Embedder: embed_many working")


def test_vector_store_populates():
    store = VectorStore(persist_directory="./data/test_chroma_db")
    store.load_and_embed_knowledge()
    assert store.is_populated()
    print(f"✅ VectorStore: populated with {store.collection.count()} chunks")


def test_vector_store_query():
    store = VectorStore(persist_directory="./data/test_chroma_db")
    store.load_and_embed_knowledge()
    results = store.query("Who is the king of the gods?", n_results=3)
    assert len(results) > 0
    assert "text" in results[0]
    assert "source" in results[0]
    assert "score" in results[0]
    print(f"✅ VectorStore: query returned {len(results)} results")
    print(f"   Top result score: {results[0]['score']}")
    print(f"   Top result source: {results[0]['source']}")


def test_retriever_full_pipeline():
    store = VectorStore(persist_directory="./data/test_chroma_db")
    store.load_and_embed_knowledge()
    retriever = Retriever(store)

    results = retriever.retrieve("Tell me about Athena")
    context = retriever.format_context(results)
    citations = retriever.get_citations(results)

    assert len(context) > 0
    assert len(citations) > 0
    print(f"\n✅ Retriever: full pipeline working")
    print(f"   Citations: {citations}")
    print(f"   Context preview: {context[:200]}...")
