from __future__ import annotations

import typing
import abc


class PathFindingNode(metaclass=abc.ABCMeta):
    """Abstract node in a graph for pathfinding."""

    @abc.abstractmethod
    def get_all_edges(self) -> typing.Iterable[PathFindingEdge]:
        """Get all edges connected to this node.

        Returns:
            all edges connected to this node."""
        pass


class PathFindingEdge(metaclass=abc.ABCMeta):
    """"Abstract node in a graph for pathfinding."""

    @abc.abstractmethod
    def get_weight(self) -> float:
        """Get the weight of this edge.

        Returns:
            float: the weight of this connection."""
        pass

    @abc.abstractmethod
    def get_other(self, origin: PathFindingNode) -> PathFindingNode:
        """Get the node on the other side of this edge from one side.

        Args:
            origin: the node from which the other side need to be fetched.

        Returns:
            node on the other side."""
        pass


class PathFindingGraph(metaclass=abc.ABCMeta):
    """Abstract graph for pathfinding purposes.

    Attributes:
        nodes: all nodes apart of this graph."""

    def __init__(self, nodes: list[PathFindingNode]):
        """Initialize instance with nodes."""
        self.nodes: list[PathFindingNode] = nodes

    @abc.abstractmethod
    def find_shortest_path(self, start: PathFindingNode,
                           target: PathFindingNode,
                           visualize: bool = False) -> tuple[float, list[PathFindingEdge]]:
        """Find the shortest path through the graph.

        Args:
            start: the node from which the shortest path needs to be searched.
            target: the node to which the shortest path needs to be searched.
            visualize: whether the progress should be visualised by loadingbar.LoadingBar.

        Returns:
            tuple that contains:
                0: the total weight of the shortest path.
                1: list containing every step of the shortest path, in order."""
        pass
