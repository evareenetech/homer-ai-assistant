"""
test_graph.py
Tests for the mythology graph engine.
"""

import pytest
from mythology.graph_engine import MythologyGraph


@pytest.fixture(scope="module")
def graph():
    return MythologyGraph()


def test_graph_builds(graph):
    assert graph.graph.number_of_nodes() > 0
    assert graph.graph.number_of_edges() > 0
    print(f"\n✅ Graph built: {graph.graph.number_of_nodes()} nodes, "
          f"{graph.graph.number_of_edges()} edges")


def test_get_children_zeus(graph):
    children = graph.get_children("Zeus")
    names = [c["name"] for c in children]
    assert "Athena" in names
    assert "Apollo" in names
    assert "Hermes" in names
    print(f"✅ Zeus's children: {names}")


def test_get_parents_athena(graph):
    parents = graph.get_parents("Athena")
    names = [p["name"] for p in parents]
    assert "Zeus" in names
    assert "Metis" in names
    print(f"✅ Athena's parents: {names}")


def test_get_siblings_zeus(graph):
    siblings = graph.get_siblings("Zeus")
    names = [s["name"] for s in siblings]
    assert "Hera" in names
    assert "Poseidon" in names
    assert "Hades" in names
    print(f"✅ Zeus's siblings: {names}")


def test_get_ancestors_achilles(graph):
    ancestors = graph.get_ancestors("Achilles", max_depth=4)
    names = [a["name"] for a in ancestors]
    print(f"✅ Achilles's ancestors: {names}")
    assert len(ancestors) > 0


def test_get_descendants_cronus(graph):
    descendants = graph.get_descendants("Cronus", max_depth=3)
    names = [d["name"] for d in descendants]
    assert "Zeus" in names
    assert "Apollo" in names
    print(f"✅ Cronus's descendants: {names}")


def test_get_figure_info(graph):
    info = graph.get_figure_info("Zeus")
    assert info is not None
    assert info["category"] == "olympian"
    assert len(info["children"]) > 0
    assert len(info["parents"]) > 0
    print(f"✅ Zeus full info retrieved")
    print(f"   Category: {info['category']}")
    print(f"   Children count: {len(info['children'])}")
    print(f"   Parents: {[p['name'] for p in info['parents']]}")


def test_get_by_category(graph):
    olympians = graph.get_by_category("olympian")
    names = [o["name"] for o in olympians]
    assert "Zeus" in names
    assert "Athena" in names
    assert "Apollo" in names
    print(f"✅ Olympians: {names}")


def test_find_connection(graph):
    path = graph.find_connection("Chaos", "Achilles")
    assert path is not None
    assert path[0] == "Chaos"
    assert path[-1] == "Achilles"
    print(f"✅ Path from Chaos to Achilles: {' → '.join(path)}")


def test_full_tree_export(graph):
    data = graph.get_full_tree_data()
    assert "nodes" in data
    assert "edges" in data
    assert len(data["nodes"]) > 0
    assert len(data["edges"]) > 0
    print(f"✅ Full tree export: {len(data['nodes'])} nodes, "
          f"{len(data['edges'])} edges")