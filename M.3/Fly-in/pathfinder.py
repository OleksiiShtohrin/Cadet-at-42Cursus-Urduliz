from __future__ import annotations

"""Path finding utilities.

Provides a `PathFinder` class that implements BFS-based shortest-path and
alternative path searches used by the planner.
"""

from collections import deque
from typing import Optional, Set, Tuple

from errors import PathFinderError
from models import Graph


class PathFinder:
    """Finds paths through the graph using breadth-first search.

    The class exposes `find_shortest_path` and `find_alternative_path` which
    return lists of zone names or raise `PathFinderError` when no route is
    available.
    """

    def find_shortest_path(
        self,
        graph: Graph,
        start: str,
        goal: str
    ) -> list[str]:
        """
        Find a shortest path with BFS.

        Args:
            graph: Graph of the map.
            start: Start zone name.
            goal: Goal zone name.

        Returns:
            List of zone names from start to goal.
        """
        if start not in graph.zones:
            raise PathFinderError(f"Unknown start zone: {start}")
        if goal not in graph.zones:
            raise PathFinderError(f"Unknown goal zone: {goal}")

        queue: deque[list[str]] = deque([[start]])
        visited: Set[str] = {start}

        while queue:
            path = queue.popleft()
            current = path[-1]

            if current == goal:
                return path

            for neighbor in graph.adjacency.get(current, []):
                zone = graph.zones.get(neighbor)
                if zone is None:
                    continue
                if zone.zone_type == "blocked":
                    continue
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                queue.append(path + [neighbor])

        raise PathFinderError(f"No path found between '{start}' and '{goal}'")

    def find_alternative_path(
        self,
        graph: Graph,
        start: str,
        goal: str,
        banned_edges: Optional[Set[Tuple[str, str]]] = None,
    ) -> list[str]:
        """
        Find an alternative path while avoiding banned edges.

        Args:
            graph: Graph of the map.
            start: Start zone name.
            goal: Goal zone name.
            banned_edges: Edges to avoid, stored as sorted zone-name tuples.

        Returns:
            A list of zone names representing the path.
        """
        if start not in graph.zones:
            raise PathFinderError(f"Unknown start zone: {start}")
        if goal not in graph.zones:
            raise PathFinderError(f"Unknown goal zone: {goal}")

        forbidden = banned_edges or set()
        queue: deque[list[str]] = deque([[start]])
        visited: Set[str] = {start}

        while queue:
            path = queue.popleft()
            current = path[-1]

            if current == goal:
                return path

            for neighbor in graph.adjacency.get(current, []):
                edge = self._edge_key(current, neighbor)
                zone = graph.zones.get(neighbor)

                if zone is None:
                    continue
                if zone.zone_type == "blocked":
                    continue
                if edge in forbidden:
                    continue
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                queue.append(path + [neighbor])

        raise PathFinderError("No alternative path found")

    def _edge_key(self, zone_a: str, zone_b: str) -> tuple[str, str]:
        """Return a canonical undirected edge key for two zone names.

        This orders the two zone names so the pair can be used as a
        dictionary/set key for undirected edges.

        Args:
            zone_a: First zone name.
            zone_b: Second zone name.

        Returns:
            A 2-tuple (min_name, max_name).
        """
        if zone_a <= zone_b:
            return zone_a, zone_b
        return zone_b, zone_a
