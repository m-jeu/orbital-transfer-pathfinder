from __future__ import annotations
import abc
import heapq

import shortpathfinding.pathfinding


class DijkstraNode(shortpathfinding.pathfinding.PathFindingNode, metaclass=abc.ABCMeta):
    """Abstract node in graph for pathfinding with Dijkstra's algorithm.

    Can be used for many optimization / pathfinding problems by extending
    a concrete class (that's supposed to function as a node) with this one.

    Attributes:
        lowest_distance:
            the lowest known distance to this node (from the start as set by DijkstraGraph.find_shortest_path()).
        discovered_through: through what edge the lowest_distance was discovered."""

    def __init__(self, init_at_infinity: bool = True):
        """Initialize class instance with discovered_through = None, and lowest_distance at either 0 or infinity
        based on passed parameters."""
        self.lowest_distance: float = float('inf') if init_at_infinity else 0
        self.discovered_through: DijkstraEdge or None = None

    def __gt__(self, other: DijkstraNode) -> bool:
        """Do greater-then comparison based on lowest_distance.

        Args:
            other: Node to compare to.

        Returns:
            whether left item is greater then right item."""
        return self.lowest_distance > other.lowest_distance

    @abc.abstractmethod
    def __hash__(self) -> int:
        """Hash so that nodes have unique hash-id.

        Returns:
            hash."""
        pass


class DijkstraEdge(shortpathfinding.pathfinding.PathFindingEdge, metaclass=abc.ABCMeta):
    """Abstract edge in graph for pathfinding with Dijkstra's algorithm.

    Can be used for many optimization / pathfinding problems by extending
    a concrete class (that's supposed to function as an edge) with this one.

    Currently, this class doesn't do much. For consistency's sake and typing in other Dijkstra's-algorithm, it's still
    a class."""
    pass


class DijkstraGraph(shortpathfinding.pathfinding.PathFindingGraph):
    """Graph for pathfinding purposes with Dijkstra's algorithm."""

    def find_shortest_path(self, start: DijkstraNode,
                           target: DijkstraNode) -> tuple[float, list[DijkstraEdge]]:
        """Find the shortest path through the graph using Dijkstra's algorithm.

        Args:
            start: the node from which the shortest path needs to be searched.
            target: the node to which the shortest path needs to be searched.

        Returns:
            tuple that contains:
                0: the total weight of the shortest path.
                1: list containing every step of the shortest path, in order."""

        # Setup
        start.lowest_distance = 0
        completed_nodes = set()

        priority_queue = self.nodes.copy()  # heapq doesn't support OOP-like heap implementation, but treats
        heapq.heapify(priority_queue)  # list like heap. Only heapq operations should be used on priority_queue.

        # Algorithm
        while len(priority_queue) != 0:
            node = heapq.heappop(priority_queue)
            for edge in node.get_all_edges():
                other_node = edge.get_other(node)
                if other_node not in completed_nodes:
                    discovered_distance = node.lowest_distance + edge.get_weight()
                    if discovered_distance < other_node.lowest_distance:
                        other_node.lowest_distance, other_node.discovered_through = discovered_distance, edge
                        heapq.heappush(priority_queue, other_node)
            completed_nodes.add(node)

        # Go backwards from target to collect shortest path
        node, result = target, []
        while (node := node.discovered_through.get_other(node)) != start:
            result.append(node.discovered_through)
        return target.lowest_distance, result[::-1]  # TODO: Reset nodes for later use.
