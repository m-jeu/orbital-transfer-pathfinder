from __future__ import annotations

import abc


class PathFindingNode(metaclass=abc.ABCMeta):
    def __init__(self):
        self.completed: bool = False
        self.lowest_distance: float = float('inf')
        self.discovered_by: PathFindingNode = self

    def __gt__(self, other: PathFindingNode):
        return self.lowest_distance > other.lowest_distance

    @abc.abstractmethod
    def get_all_connected(self) -> list[tuple[PathFindingNode, float] or tuple[PathFindingNode, float, object]]:
        pass


class PathFindingGraph(metaclass=abc.ABCMeta):
    def __init__(self, nodes: list[PathFindingNode]):
        self.nodes: list[PathFindingNode] = nodes

    @abc.abstractmethod
    def find_shortest_path(self, start: PathFindingNode,
                           target: PathFindingNode) -> tuple[float, list[PathFindingNode or object]]:
        pass
