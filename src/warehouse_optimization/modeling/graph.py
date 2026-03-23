from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(slots=True)
class Node:
    node_id: str
    kind: str
    x: float
    y: float


@dataclass(slots=True)
class Edge:
    source_id: str
    target_id: str
    cost: float
    bidirectional: bool = True


@dataclass(slots=True)
class WarehouseGraph:
    nodes: Dict[str, Node] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)
