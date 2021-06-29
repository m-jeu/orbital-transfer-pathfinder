from __future__ import annotations

import abc

import orbital_transfer_pathfinder.lib.shortpathfinding.dijkstras_algorithm as dijkstras_algorithm


class CDijkstraNode(dijkstras_algorithm.DijkstraNode, metaclass=abc.ABCMeta):
    """Abstract node in graph for pathfinding with the Custom heuristic for Dijkstra's algorithm.

    Can be used for many optimization / pathfinding problems by extending
    a concrete class (that's supposed to function as a node) with this one.

    Currently, this class doesn't add much in terms of functionality over it's parent.
    For consistency's sake, it's still a class."""
    pass


class CDijkstraEdge(dijkstras_algorithm.DijkstraEdge, metaclass=abc.ABCMeta):
    """Abstract edge in graph for pathfinding with the Custom heuristic for Dijkstra's algorithm.

    Can be used for many optimization / pathfinding problems by extending
    a concrete class (that's supposed to function as an edge) with this one."""

    def virtual_weight(self, origin_node: CDijkstraNode, **kwargs) -> float:
        """Determine what total distance should be calculated for a certain node from another connected node +
        the edge during the PathFinding algorithm execution phase. Doesn't hold any sway over the actual distance found.

        In the Custom heuristic for Dijkstra's algorithm, this is the distance it would be in Dijkstra's algorithm + 5.
        This causes the algorithm to prefer taking short paths over long ones, when they are equal in weight otherwise.

        Args:
            origin_node: node from which target node was reached.
            **kwargs:
                any additional information used by subclasses of DijkstraNode used to compute virtual weight.
                not used by CDijkstra, but used by (for instance) A*..

        Returns:
            'virtual' weight."""
        return super().virtual_weight(origin_node) + 5


class CDijkstraGraph(dijkstras_algorithm.DijkstraGraph, metaclass=abc.ABCMeta):
    """Graph for pathfinding purposes with Custom heuristic for Dijkstra's algorithm.

    Currently, this class doesn't add much in terms of functionality over it's parent.
    For consistency's sake, it's still a class."""
    pass
