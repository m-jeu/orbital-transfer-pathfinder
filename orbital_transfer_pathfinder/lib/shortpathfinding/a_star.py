from __future__ import annotations

import abc

import orbital_transfer_pathfinder.lib.shortpathfinding.dijkstras_algorithm as dijkstras_algorithm


class AStarNode(dijkstras_algorithm.DijkstraNode, metaclass=abc.ABCMeta):
    """Abstract node in graph for pathfinding with the A* algorithm.

    Can be used for many optimization / pathfinding problems by extending
    a concrete class (that's supposed to function as a node) with this one.
    Currently, this class doesn't add much in terms of functionality over it's parent.
    For consistency's sake, it's still a class."""
    pass


class AStarEdge(dijkstras_algorithm.DijkstraEdge, metaclass=abc.ABCMeta):
    """Abstract edge in graph for pathfinding with the A* algorithm.

    Can be used for many optimization / pathfinding problems by extending
    a concrete class (that's supposed to function as an edge) with this one."""

    @abc.abstractmethod
    def a_star_difference_heuristic(self) -> float:
        """Abstract method that calculates a heuristic cost for this edge.

        Returns:
            weight to add to edge weight."""
        pass

    def virtual_weight(self, origin_node: AStarNode) -> float:
        """Determine what total distance should be calculated for a certain node from another connected node +
        the edge during the PathFinding algorithm execution phase. Doesn't hold any sway over the actual distance found.

        In the A* algorithm, this is the distance it would be in Dijkstra's algorithm + whatever
        a_star_difference_heuristic() finds the additional weight should be.

        Args:
            origin_node: node from which target node was reached.

        Returns:
            'virtual' weight."""
        return super().virtual_weight(origin_node) + self.a_star_difference_heuristic()


class AStarGraph(dijkstras_algorithm.DijkstraGraph, metaclass=abc.ABCMeta):
    """Graph for pathfinding purposes with the A* algorithm.

    Currently, this class doesn't add much in terms of functionality over it's parent.
    For consistency's sake, it's still a class."""
    pass
