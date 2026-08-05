"""
graph_engine.py
NetworkX-powered graph engine for querying Greek mythology
family relationships. Powers the family tree feature.
"""

import logging
import networkx as nx
from typing import Any
from mythology.family_tree import get_figures, get_relationships

logger = logging.getLogger(__name__)


class MythologyGraph:
    """
    A directed graph of Greek mythology family relationships.
    Nodes = mythological figures, Edges = relationships.
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_graph()
        logger.info("Built graph with %d nodes and %d edges.",
                    self.graph.number_of_nodes(), self.graph.number_of_edges())

    def _build_graph(self):
        """Build the NetworkX graph from family tree data."""
        figures = get_figures()
        relationships = get_relationships()

        # Add nodes with attributes
        for name, attrs in figures.items():
            self.graph.add_node(name, **attrs)

        # Add edges with relationship type
        for parent, child, rel_type in relationships:
            self.graph.add_edge(parent, child, relationship=rel_type)

    # ── Query methods ─────────────────────────────────────────────────────────

    def get_children(self, name: str) -> list[dict[str, Any]]:
        """Return all children of a given figure."""
        if name not in self.graph:
            return []
        children = []
        for _, child, data in self.graph.out_edges(name, data=True):
            if data.get("relationship") == "parent":
                attrs = self.graph.nodes[child]
                children.append({"name": child, **attrs})
        return children

    def get_parents(self, name: str) -> list[dict[str, Any]]:
        """Return all parents of a given figure."""
        if name not in self.graph:
            return []
        parents = []
        for parent, _, data in self.graph.in_edges(name, data=True):
            if data.get("relationship") == "parent":
                attrs = self.graph.nodes[parent]
                parents.append({"name": parent, **attrs})
        return parents

    def get_siblings(self, name: str) -> list[dict[str, Any]]:
        """Return all siblings of a given figure (share at least one parent)."""
        if name not in self.graph:
            return []
        parents = [p for p, _, d in self.graph.in_edges(name, data=True)
                   if d.get("relationship") == "parent"]
        siblings = set()
        for parent in parents:
            for _, child, data in self.graph.out_edges(parent, data=True):
                if data.get("relationship") == "parent" and child != name:
                    siblings.add(child)
        result = []
        for sibling in siblings:
            attrs = self.graph.nodes[sibling]
            result.append({"name": sibling, **attrs})
        return result

    def get_spouse(self, name: str) -> list[dict[str, Any]]:
        """Return the spouse(s) of a given figure."""
        if name not in self.graph:
            return []
        spouses = []
        for _, other, data in self.graph.out_edges(name, data=True):
            if data.get("relationship") == "spouse":
                attrs = self.graph.nodes[other]
                spouses.append({"name": other, **attrs})
        return spouses

    def get_ancestors(self, name: str, max_depth: int = 4) -> list[dict[str, Any]]:
        """Return all ancestors of a figure up to max_depth generations."""
        if name not in self.graph:
            return []
        ancestors = []
        visited = set()

        def recurse(node, depth):
            if depth > max_depth:
                return
            for parent, _, data in self.graph.in_edges(node, data=True):
                if data.get("relationship") == "parent" and parent not in visited:
                    visited.add(parent)
                    attrs = self.graph.nodes[parent]
                    ancestors.append({"name": parent, **attrs})
                    recurse(parent, depth + 1)

        recurse(name, 0)
        return ancestors

    def get_descendants(self, name: str, max_depth: int = 3) -> list[dict[str, Any]]:
        """Return all descendants of a figure up to max_depth generations."""
        if name not in self.graph:
            return []
        descendants = []
        visited = set()

        def recurse(node, depth):
            if depth > max_depth:
                return
            for _, child, data in self.graph.out_edges(node, data=True):
                if data.get("relationship") == "parent" and child not in visited:
                    visited.add(child)
                    attrs = self.graph.nodes[child]
                    descendants.append({"name": child, **attrs})
                    recurse(child, depth + 1)

        recurse(name, 0)
        return descendants

    def get_figure_info(self, name: str) -> dict[str, Any] | None:
        """Return full info about a figure including all relationships."""
        if name not in self.graph:
            return None
        attrs = dict(self.graph.nodes[name])
        return {
            "name": name,
            **attrs,
            "parents":     self.get_parents(name),
            "children":    self.get_children(name),
            "siblings":    self.get_siblings(name),
            "spouses":     self.get_spouse(name),
            "ancestors":   self.get_ancestors(name, max_depth=2),
            "descendants": self.get_descendants(name, max_depth=2),
        }

    def get_by_category(self, category: str) -> list[dict[str, Any]]:
        """Return all figures of a given category (olympian, titan, hero, etc.)."""
        result = []
        for node, attrs in self.graph.nodes(data=True):
            if attrs.get("category") == category:
                result.append({"name": node, **attrs})
        return result

    def find_connection(self, name1: str, name2: str) -> list[str] | None:
        """
        Find the shortest relationship path between two figures.
        Uses an undirected version of the graph for pathfinding.
        """
        undirected = self.graph.to_undirected()
        try:
            path = nx.shortest_path(undirected, name1, name2)
            return path
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def get_full_tree_data(self) -> dict[str, Any]:
        """
        Export the full graph as JSON-serializable data
        for the frontend family tree visualisation.
        """
        nodes = []
        for node, attrs in self.graph.nodes(data=True):
            nodes.append({
                "id": node,
                "label": node,
                "category": attrs.get("category", "unknown"),
                "description": attrs.get("description", ""),
                "source": attrs.get("source", ""),
            })

        edges = []
        for parent, child, data in self.graph.edges(data=True):
            edges.append({
                "source": parent,
                "target": child,
                "relationship": data.get("relationship", "unknown"),
            })

        return {"nodes": nodes, "edges": edges}