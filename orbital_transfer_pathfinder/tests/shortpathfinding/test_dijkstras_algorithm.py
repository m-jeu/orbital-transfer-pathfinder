from __future__ import annotations

import typing
from unittest import TestCase

import orbital_transfer_pathfinder.lib.shortpathfinding.dijkstras_algorithm as dijkstras_algorithm


# Unit-testing abstract classes isn't standard practice in most test-philosophies
# But in this case, the specific implementations of the Pathfinding classes define much behaviour
# That would benefit from testing, so here are some concrete classes that only extends the abstract
# Classes being tested in only the most elementary way.

class ConcreteNode(dijkstras_algorithm.DijkstraNode):
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


class ConcreteEdge(dijkstras_algorithm.DijkstraEdge):
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

class TestDijkstraNode(TestCase):

    def test_constructor(self):
        test_node = ConcreteNode()

        self.assertEqual(test_node.lowest_distance, float('inf'),
                         msg="DijkstraNode.lowest_distance should initialize at infinity by default.")

        self.assertEqual(test_node.discovered_through, None,
                         msg="DijkstraNode.discovered_through should initialize as None by default.")

    def test_greater_then(self):
        test_node_1 = ConcreteNode()
        test_node_2 = ConcreteNode()

        test_node_1.lowest_distance = 100

        test_node_2.lowest_distance = 0

        self.assertTrue(test_node_1 > test_node_2,
                        msg="DijkstraNode greater_then comparisons should be based on lowest_distance.")


class TestDijkstraEdge(TestCase):

    def test_virtual_weight(self):
        test_node_1 = ConcreteNode()
        test_node_1.lowest_distance = 5
        test_node_2 = ConcreteNode()
        test_edge = ConcreteEdge(test_node_1, test_node_2, 10)

        self.assertEqual(test_edge.virtual_weight(test_node_1), 15,
                         msg="DijkstraEdge.virtual_add() should add together edge weight and origin node "
                             "lowest distance to get virtual weight.")

        self.assertEqual(test_edge.virtual_weight(test_node_1, target_node=test_node_2 ), 15,
                         msg="DijkstraEdge.virtual_add() should not change result when passed"
                             " 'target_node' keyword-argument.")


class TestDijkstraGraph(TestCase):

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

        test_graph = dijkstras_algorithm.DijkstraGraph([test_node_inbetween_1,
                                                        test_node_inbetween_2,
                                                        test_node_end,
                                                        test_node_start])

        dist, edges, nodes = test_graph.find_shortest_path(test_node_start, test_node_end)

        self.assertEqual(dist, 9, msg="DijkstraGraph.find_shortest_path() should always converge on shortest path.")

        self.assertEqual(edges, [edge_short_1, edge_short_2, edge_short_3],
                         msg="DijkstraGraph.find_shortest_path() should always converge on shortest path and return"
                             " traversed edges in returned tuple at index 1.")

        self.assertEqual(nodes, [test_node_start, test_node_inbetween_1, test_node_inbetween_2, test_node_end],
                         msg="DijkstraGraph.find_shortest_path() should always converge on shortest path and return"
                             " traversed nodes in returned tuple at index 2.")
