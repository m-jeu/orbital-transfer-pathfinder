import shortpathfinding.pathfinding
from shortpathfinding.pathfinding import PathFindingNode

import heapq


class DijkstraGraph(shortpathfinding.pathfinding.PathFindingGraph):
    def find_shortest_path(self, start: PathFindingNode,
                           target: PathFindingNode) -> tuple[float, list[PathFindingNode or object]]:
        start.lowest_distance = 0
        priority_queue = heapq.heapify(self.nodes)
        while len(priority_queue) != 0:
            node = heapq.heappop(priority_queue)
            