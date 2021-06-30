from __future__ import annotations

import typing
from unittest import TestCase

import orbital_transfer_pathfinder.lib.shortpathfinding.a_star as a_star


# Unit-testing abstract classes isn't standard practice in most test-philosophies
# But in this case, the specific implementations of the Pathfinding classes define much behaviour
# That would benefit from testing, so here are some concrete classes that only extends the abstract
# Classes being tested in only the most elementary way.
from orbital_transfer_pathfinder.lib.shortpathfinding.a_star import AStarNode


class ConcreteNode(a_star.AStarNode):
    unique_int = 0

    def __init__(self, name: str = None, heuristic_weight: float = 1.0):
        super().__init__()
        self.uid: int = ConcreteNode.unique_int
        ConcreteNode.unique_int += 1
        self.edges: set[ConcreteEdge] = set()
        if name is None:
            self.name = str(self.uid)
        else:
            self.name = name
        self.heuristic_weight = heuristic_weight

    def __eq__(self, other) -> bool:
        return self.uid == other.uid

    def __hash__(self) -> int:
        return self.uid

    def __str__(self):
        return f"Node {self.name}"

    def get_all_edges(self) -> typing.Iterable[ConcreteEdge]:
        return self.edges

    def a_star_difference_heuristic(self, final_target: AStarNode) -> float:
        return self.heuristic_weight


class ConcreteEdge(a_star.AStarEdge):
    def __init__(self, a: ConcreteNode, b: ConcreteNode, weight: float = 1.0):
        self.a: ConcreteNode = a
        self.b: ConcreteNode = b
        self.weight: float = weight

    def get_weight(self) -> float:
        return self.weight

    def get_other(self, origin: ConcreteNode) -> ConcreteNode:
        if origin == self.a:
            return self.b
        return self.a

    def __str__(self):
        return f"{str(self.a)} <-> {str(self.b)}"

# Actual tests

class TestAStarNode(TestCase):

    def test_constructor(self):
        test_node = ConcreteNode()

        self.assertEqual(test_node.lowest_distance, float('inf'),
                         msg="AStarNode.lowest_distance should initialize at infinity by default.")

        self.assertEqual(test_node.discovered_through, None,
                         msg="AStarNode.discovered_through should initialize as None by default.")

    def test_greater_then(self):
        test_node_1 = ConcreteNode()
        test_node_2 = ConcreteNode()

        test_node_1.lowest_distance = 100

        test_node_2.lowest_distance = 0

        self.assertTrue(test_node_1 > test_node_2,
                        msg="AStarNode greater_then comparisons should be based on lowest_distance.")


class TestAStarEdge(TestCase):

    def test_virtual_weight(self):
        test_node_1 = ConcreteNode()
        test_node_1.lowest_distance = 5
        test_node_2 = ConcreteNode(heuristic_weight=10)
        test_edge = ConcreteEdge(test_node_1, test_node_2, 10)

        self.assertEqual(test_edge.virtual_weight(test_node_1, target_node=test_node_2), 25,
                         msg="AStarEdge.virtual_add() should add together edge weight, origin node "
                             "lowest distance and target_node heuristic weight to get virtual weight.")


class TestAStarGraph(TestCase):

    def test_find_shortest_path(self):
        test_node_start = ConcreteNode("Start")
        test_node_inbetween_1 = ConcreteNode("Inbetween-1")
        test_node_inbetween_2 = ConcreteNode("Inbetween-2")
        test_node_end = ConcreteNode("End")

        edge_long = ConcreteEdge(test_node_start, test_node_end, 10)
        test_node_start.edges.add(edge_long)
        test_node_end.edges.add(edge_long)

        edge_short_1 = ConcreteEdge(test_node_start, test_node_inbetween_1, 3)
        test_node_start.edges.add(edge_short_1)
        test_node_inbetween_1.edges.add(edge_short_1)

        edge_short_2 = ConcreteEdge(test_node_inbetween_1, test_node_inbetween_2, 3)
        test_node_inbetween_1.edges.add(edge_short_2)
        test_node_inbetween_2.edges.add(edge_short_2)

        edge_short_3 = ConcreteEdge(test_node_inbetween_2, test_node_end, 3)
        test_node_inbetween_2.edges.add(edge_short_3)
        test_node_end.edges.add(edge_short_3)

        test_graph = a_star.AStarGraph([test_node_inbetween_1,
                                        test_node_inbetween_2,
                                        test_node_end,
                                        test_node_start])

        dist, path = test_graph.find_shortest_path(test_node_start, test_node_end)

        self.assertEqual(path, [edge_long],
                         msg="AStarGraph.find_shortest_path() should compute shortest path using the actual weights +"
                             " heuristic weights.")

        self.assertEqual(dist, 10, msg="AStarGraph.find_shortest_path() should not include heuristic weights in final"
                                       " path length.")
