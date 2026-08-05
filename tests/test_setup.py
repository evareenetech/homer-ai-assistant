def test_ollama_connection():
    import ollama
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": "Say: Setup complete."}]
    )
    assert response["message"]["content"] is not None
    print("\n✅ Ollama connected:", response["message"]["content"])


def test_chromadb():
    import chromadb
    client = chromadb.Client()
    col = client.create_collection("test")
    assert col is not None
    print("✅ ChromaDB working")


def test_networkx():
    import networkx as nx
    G = nx.DiGraph()
    G.add_edge("Zeus", "Athena")
    assert "Athena" in G.nodes
    print("✅ NetworkX working")
