"""
api/routes/family_tree.py
Family tree endpoints — query the Greek mythology graph.

The graph is initialised once at module level and shared across
all requests. Building a NetworkX graph is fast but we only want
to do it once, not on every request.
"""

from fastapi import APIRouter, HTTPException
from api.schemas import FigureDetail, FigureInfo, PathResponse, TreeData
from mythology.graph_engine import MythologyGraph

router = APIRouter(prefix="/family-tree", tags=["Family Tree"])
_graph = MythologyGraph()


def _validate_figure(name: str) -> str:
    """Normalise a figure name and confirm it exists in the graph."""
    name = name.capitalize()
    if name not in _graph.graph:
        raise HTTPException(status_code=404, detail=f"'{name}' not found.")
    return name


@router.get("/", response_model=TreeData)
async def get_full_tree():
    """
    Return the complete family tree as nodes and edges.
    This is what the frontend uses to render the visual graph.
    """
    return _graph.get_full_tree_data()


@router.get("/{name}", response_model=FigureDetail)
async def get_figure(name: str):
    """
    Get full information about a specific mythological figure,
    including all their family relationships.
    """
    name = name.capitalize()
    info = _graph.get_figure_info(name)
    if not info:
        raise HTTPException(
            status_code=404,
            detail=f"Figure '{name}' not found in the mythology graph."
        )
    return info


@router.get("/{name}/children", response_model=list[FigureInfo])
async def get_children(name: str):
    """Return all children of a mythological figure."""
    name = _validate_figure(name)
    return _graph.get_children(name)


@router.get("/{name}/parents", response_model=list[FigureInfo])
async def get_parents(name: str):
    """Return all parents of a mythological figure."""
    name = _validate_figure(name)
    return _graph.get_parents(name)


@router.get("/{name}/siblings", response_model=list[FigureInfo])
async def get_siblings(name: str):
    """Return all siblings of a mythological figure."""
    name = _validate_figure(name)
    return _graph.get_siblings(name)


@router.get("/{name}/path/{target}", response_model=PathResponse)
async def get_path(name: str, target: str):
    """
    Find the relationship path between two mythological figures.
    Example: /family-tree/chaos/path/achilles
    Returns: Chaos → Gaia → Cronus → Zeus → Aeacus → Peleus → Achilles
    """
    name   = name.capitalize()
    target = target.capitalize()
    path   = _graph.find_connection(name, target)

    return PathResponse(
        from_figure=name,
        to_figure=target,
        path=path if path else [],
        found=path is not None
    )