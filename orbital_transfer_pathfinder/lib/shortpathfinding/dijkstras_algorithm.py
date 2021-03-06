from __future__ import annotations

import abc
import heapq

from ..shortpathfinding import pathfinding
from ..loadingbar import loadingbar


class DijkstraNode(pathfinding.PathFindingNode, metaclass=abc.ABCMeta):
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
    def __eq__(self, other) -> bool:
        """Determine equality of 2 nodes.

        Must be implemented by subclass so that every node in graph is unique.

        Args:
            other: object to compare to."""
        pass

    @abc.abstractmethod
    def __hash__(self) -> int:
        """Hash so that nodes have unique hash-id.

        Returns:
            hash."""
        pass


class DijkstraEdge(pathfinding.PathFindingEdge, metaclass=abc.ABCMeta):
    """Abstract edge in graph for pathfinding with Dijkstra's algorithm.

    Can be used for many optimization / pathfinding problems by extending
    a concrete class (that's supposed to function as an edge) with this one."""

    def virtual_weight(self, origin_node: DijkstraNode, **kwargs) -> float:
        """Determine what total distance should be calculated for a certain node from another connected node +
        the edge during the PathFinding algorithm execution phase. Doesn't hold any sway over the actual distance found.

        In Dijkstra's algorithm, this is just the origin node's lowest distance + the edge distance.

        Args:
            origin_node: node from which target node was reached.
            **kwargs:
                any additional information used by subclasses used to compute virtual weight.
                not used by Dijkstra, but used by (for instance) A*.

        Returns:
            'virtual' weight."""
        return origin_node.lowest_distance + self.get_weight()


class DijkstraGraph(pathfinding.PathFindingGraph):
    """Graph for pathfinding purposes with Dijkstra's algorithm."""

    def _reset_nodes(self):
        """Reset lowest_distance and discovered_by for all nodes"""
        for node in self.nodes:
            node.lowest_distance = float('inf')
            node.discovered_through = None

    def find_shortest_path(self, start: DijkstraNode,
                           target: DijkstraNode,
                           visualize: bool = False) -> tuple[float, list[DijkstraEdge]]:
        """Find the shortest path through the graph using Dijkstra's algorithm.

        Args:
            start: the node from which the shortest path needs to be searched.
            target: the node to which the shortest path needs to be searched.
            virtual_cost_per_edge:
                a virtual cost that should should be added per traversed edge when comparing possible routes to
                each other, to combat the algorithm taking lots of small edges that have the same effect as 1 big edge.
                won't be included in final cost calculation of the method.
            visualize: whether the progress should be visualised by loadingbar.LoadingBar.

        Returns:
            tuple that contains:
                0: the total weight of the shortest path.
                1: list containing every step of the shortest path, in order.
                2: list containing every node traversed in the order they were traversed in"""

        # Setup
        lb = loadingbar.LoadingBar(len(self.nodes)) if visualize else None

        start.lowest_distance = 0
        completed_nodes = set()

        priority_queue = self.nodes.copy()  # heapq doesn't support OOP-like heap implementation, but treats
        heapq.heapify(priority_queue)  # list like heap. Only heapq operations should be used on priority_queue.

        # Algorithm
        while (node := heapq.heappop(priority_queue)) != target:
            if node not in completed_nodes:
                for edge in node.get_all_edges():
                    other_node = edge.get_other(node)
                    if other_node not in completed_nodes:
                        discovered_distance = edge.virtual_weight(node, target_node=target)  # Target node used by A*
                        if discovered_distance < other_node.lowest_distance:                 # and not bij Dijkstra.
                            other_node.lowest_distance, other_node.discovered_through = discovered_distance, edge
                            heapq.heappush(priority_queue, other_node)
                completed_nodes.add(node)
                if visualize: lb.increment()

        node = target
        traversed_nodes = [target]
        traversed_edges = [target.discovered_through]
        result_weight = target.discovered_through.get_weight()
        while (node := node.discovered_through.get_other(node)) != start:
            traversed_nodes.append(node)
            traversed_edges.append(node.discovered_through)
            result_weight += node.discovered_through.get_weight()
        traversed_nodes.append(start)
        self._reset_nodes()
        return result_weight, traversed_edges[::-1], traversed_nodes[::-1]

