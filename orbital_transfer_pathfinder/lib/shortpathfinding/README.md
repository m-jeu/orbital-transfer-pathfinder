A package to solve many types of shortest-path problems, from optimization to route-planning.

Currently, there are 3 shortest-path algorithms implemented:
1. Dijkstra's algorithm
2. A*
3. A simple custom heuristic based on Dijkstra's algorithm for the specific use-case of orbital pathfinding

According to the following sources for the corresponding algorithms:
1. Dijkstra, E. W. (1959). A note on two problems in connexion with graphs. Numerische Mathematik,1(1), 269–271.
   https://doi.org/10.1007/bf01386390
2. Hart, P. E.; Nilsson, N. J.; Raphael, B. (1968).
   "A Formal Basis for the Heuristic Determination of Minimum Cost Paths".
   IEEE Transactions on Systems Science and Cybernetics. 4 (2): 100–107. doi:10.1109/TSSC.1968.300136.

These algorithms are implemented in the following files:
1. dijkstras_algorithm.py
2. a_star.py
3. custom_dijkstras_algorithm.py

**How to use:**

Every algorithm is implemented in it's corresponding file using (at least) 3 classes:
1. An abstract node class
2. An abstract edge class
3. A graph class

When applying one of the algorithms to a problem, extend the classes that represent nodes and edges with the
corresponding class in the file belonging to the algorithm, and implement any abstract methods in the algorithm class.

Then store the node instances in an instance of the graph class from the algorithm file, and let the
graph.find_shortest_path() method work it's magic.

**Extra information on algorithm 3:**

The custom heuristic based on Dijkstra's algorithm is quite simple. It works by adding a small cost to every edge during
the pathfinding phase, so that the algorithm will favor paths with fewer edges over ones with more when they
have an equal total weight otherwise.
The extra weights will not be included in the final returned total path weight.

This package is originally designed for orbital manoeuvre pathfinding, where this is quite a common occurrence.
