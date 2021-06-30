from __future__ import annotations

import typing
from unittest import TestCase

import orbital_transfer_pathfinder.lib.shortpathfinding.custom_dijkstras_algorithm as custom_dijkstras_algorithm


# Unit-testing abstract classes isn't standard practice in most test-philosophies
# But in this case, the specific implementations of the Pathfinding classes define much behaviour
# That would benefit from testing, so here are some concrete classes that only extends the abstract
# Classes being tested in only the most elementary way.

class ConcreteNode(custom_dijkstras_algorithm.CDijkstraNode):
    unique_int = 0

    def __init__(self, name: str = None):
        super().__init__()
        self.uid: int = ConcreteNode.unique_int
        ConcreteNode.unique_int += 1
        self.edges: set[ConcreteEdge] = set()
        if name is None:
            self.name = str(self.uid)
        else:
            self.name = name

    def __eq__(self, other) -> bool:
        return self.uid == other.uid

    def __hash__(self) -> int:
        return self.uid

    def __str__(self):
        return f"Node {self.name}"

    def get_all_edges(self) -> typing.Iterable[ConcreteEdge]:
        return self.edges


class ConcreteEdge(custom_dijkstras_algorithm.CDijkstraEdge):
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

class TestCDijkstraNode(TestCase):

    def test_constructor(self):
        test_node = ConcreteNode()

        self.assertEqual(test_node.lowest_distance, float('inf'),
                         msg="CDijkstraNode.lowest_distance should initialize at infinity by default.")

        self.assertEqual(test_node.discovered_through, None,
                         msg="CDijkstraNode.discovered_through should initialize as None by default.")

    def test_greater_then(self):
        test_node_1 = ConcreteNode()
        test_node_2 = ConcreteNode()

        test_node_1.lowest_distance = 100

        test_node_2.lowest_distance = 0

        self.assertTrue(test_node_1 > test_node_2,
                        msg="CDijkstraNode greater_then comparisons should be based on lowest_distance.")


class TestCDijkstraEdge(TestCase):

    def test_virtual_weight(self):
        test_node_1 = ConcreteNode()
        test_node_1.lowest_distance = 5
        test_node_2 = ConcreteNode()
        test_edge = ConcreteEdge(test_node_1, test_node_2, 10)

        self.assertEqual(test_edge.virtual_weight(test_node_1), 20,
                         msg="CDijkstraEdge.virtual_add() should add together edge weight, origin node "
                             "lowest distance and 5 to get virtual weight.")

        self.assertEqual(test_edge.virtual_weight(test_node_1, target_node=test_node_2 ), 20,
                         msg="CDijkstraEdge.virtual_add() should not change result when passed"
                             " 'target_node' keyword-argument.")


class TestCDijkstraGraph(TestCase):

    def test_find_shortest_path(self):
        test_node_start = ConcreteNode("Start")
        test_node_inbetween_1 = ConcreteNode("Inbetween-1")
        test_node_inbetween_2 = ConcreteNode("Inbetween-2")
        test_node_end = ConcreteNode("End")

        edge_long = ConcreteEdge(test_node_start, test_node_end, 99)
        test_node_start.edges.add(edge_long)
        test_node_end.edges.add(edge_long)

        edge_short_1 = ConcreteEdge(test_node_start, test_node_inbetween_1, 33)
        test_node_start.edges.add(edge_short_1)
        test_node_inbetween_1.edges.add(edge_short_1)

        edge_short_2 = ConcreteEdge(test_node_inbetween_1, test_node_inbetween_2, 33)
        test_node_inbetween_1.edges.add(edge_short_2)
        test_node_inbetween_2.edges.add(edge_short_2)

        edge_short_3 = ConcreteEdge(test_node_inbetween_2, test_node_end, 33)
        test_node_inbetween_2.edges.add(edge_short_3)
        test_node_end.edges.add(edge_short_3)

        test_graph = custom_dijkstras_algorithm.CDijkstraGraph([test_node_inbetween_1,
                                                                test_node_inbetween_2,
                                                                test_node_end,
                                                                test_node_start])

        dist, path = test_graph.find_shortest_path(test_node_start, test_node_end)

        self.assertEqual(path, [edge_long],
                         msg="CDijkstraGraph.find_shortest_path() should compute shortest path, favoring paths"
                             "of equal weight that have less nodes.")

        self.assertEqual(dist, 99, msg="CDijkstraGraph.find_shortest_path() should not include custom heuristic weight"
                                       " in final computed weight.")
