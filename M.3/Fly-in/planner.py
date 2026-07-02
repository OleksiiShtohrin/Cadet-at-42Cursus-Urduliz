from __future__ import annotations

"""Planner module: construct candidate paths and assign drones.

This module contains logic to generate candidate routes, score them and
assign a number of drones across available paths while accounting for
capacities and penalties.
"""

from collections import deque
from dataclasses import dataclass
from typing import Callable, List, Set, Tuple

from errors import PathFinderError
from models import Graph
from pathfinder import PathFinder


def _edge_key(zone_a: str, zone_b: str) -> tuple[str, str]:
    """Return a normalized undirected edge key.

    The ordering is stable so edge sets can be compared in an undirected
    manner.
    """
    if zone_a <= zone_b:
        return zone_a, zone_b
    return zone_b, zone_a


@dataclass
class PathInfo:
    """Stores one candidate path and its score.

    Attributes:
        nodes: Ordered list of zone names forming the path.
        cost: Aggregate traversal cost of the path.
        priority_bonus: Bonus for priority zones.
        bottleneck_penalty: Penalty for low-capacity nodes.
        restricted_penalty: Penalty for restricted zones.
        length: Number of nodes in the path.
        loop_penalty: Penalty for repeated nodes.
        entry_pressure: Estimated congestion at the path entry.
        estimated_capacity: Minimum capacity along the path.
    """
    nodes: List[str]
    cost: int
    priority_bonus: int
    bottleneck_penalty: int
    restricted_penalty: int
    length: int
    loop_penalty: int
    entry_pressure: int
    estimated_capacity: int


class Planner:
    """Builds a movement plan for multiple drones.

    The Planner uses `PathFinder` to generate candidate routes and assigns
    drones across those routes using heuristics that balance throughput and
    congestion.
    """

    def __init__(self, graph: Graph) -> None:
        """Create a Planner for the given graph.

        Args:
            graph: The map `Graph` used to build candidate paths.
        """
        self.graph = graph
        self.path_finder = PathFinder()

    def build_paths(self, start: str, goal: str) -> List[PathInfo]:
        """Build and score multiple candidate paths between start and
        goal.

        This function generates a set of alternative routes using small
        graph perturbations, scores them and returns a sorted list of
        `PathInfo` objects ordered from best to worst according to the
        planner heuristics.

        Args:
            start: Name of the start zone.
            goal: Name of the goal zone.

        Returns:
            Sorted list of `PathInfo` candidate routes.
        """
        raw_paths = self._generate_candidate_paths(start, goal)
        if not raw_paths:
            raise PathFinderError("No candidate paths available")

        scored_paths = [self._score_path(path) for path in raw_paths]
        scored_paths.sort(key=self._path_sort_key)
        return scored_paths

    def assign_paths(
        self,
        nb_drones: int,
        paths: List[PathInfo],
    ) -> List[List[str]]:
        """
        Assign paths to drones using loop-aware distribution.

        Example:
            planner = Planner(graph)
            paths = planner.build_paths(start, goal)
            assignments = planner.assign_paths(10, paths)
        """
        if not paths:
            raise PathFinderError("No candidate paths available")

        # Sort candidate paths by the path sort key (best first)
        ranked_paths = sorted(paths, key=self._path_sort_key)

        # If only one path exists, assign all drones to it
        if len(ranked_paths) == 1:
            return [ranked_paths[0].nodes for _ in range(nb_drones)]

        # Use the classic Lem-in optimal assignment computation:
        # Find minimal total turns T such that
        # sum(max(0, T - cost_i + 1)) >= nb_drones,
        # where cost_i is the path travel time (path.cost already includes
        # restricted-zone and other penalties).

        costs = [p.cost for p in ranked_paths]
        # search for minimal T
        min_cost = min(costs)
        max_cost = min_cost + nb_drones + 5
        best_T = None
        for T in range(min_cost, max_cost + 1):
            total = sum(max(0, T - c + 1) for c in costs)
            if total >= nb_drones:
                best_T = T
                break

        if best_T is None:
            # fallback to greedy assignment
            path_lengths = [p.length for p in ranked_paths]
            assigned_counts = [0 for _ in ranked_paths]
            assignments = []
            for _ in range(nb_drones):
                projected = [
                    (path_lengths[i] + assigned_counts[i])
                    for i in range(len(ranked_paths))
                ]
                best_idx = min(
                    range(len(projected)),
                    key=lambda i: (projected[i], ranked_paths[i].cost),
                )
                assigned_counts[best_idx] += 1
                assignments.append(ranked_paths[best_idx].nodes)
            return assignments

        # Compute assigned counts from best_T
        assigned_counts = [max(0, best_T - c + 1) for c in costs]
        # Trim or distribute if we overshot due to rounding
        total_assigned = sum(assigned_counts)
        # If we assigned more than needed, remove from worst paths first
        while total_assigned > nb_drones:
            # Pick the worst-cost path that still has at least one assignment.
            non_zero_indices = (
                i
                for i in range(len(assigned_counts))
                if assigned_counts[i] > 0
            )
            idx = max(
                non_zero_indices,
                key=lambda i: (costs[i], i),
            )
            assigned_counts[idx] -= 1
            total_assigned -= 1

        # If we assigned fewer (unlikely), assign remaining to best paths
        while total_assigned < nb_drones:
            idx = min(
                range(len(assigned_counts)),
                key=lambda i: (costs[i], -assigned_counts[i]),
            )
            assigned_counts[idx] += 1
            total_assigned += 1

        # Build assignments list in round-robin across paths to avoid bunching
        assignments = []
        remaining = assigned_counts.copy()
        while sum(remaining) > 0:
            for i in range(len(ranked_paths)):
                if remaining[i] > 0:
                    assignments.append(ranked_paths[i].nodes)
                    remaining[i] -= 1

        return assignments

    def _build_quotas(
        self,
        nb_drones: int,
        paths: List[PathInfo],
    ) -> List[int]:
        """
        Build quotas using estimated capacity and entry pressure.

        Lower entry pressure and higher estimated capacity get more drones.
        """
        raw_scores: List[int] = []
        for path in paths:
            score = max(1, path.estimated_capacity)
            score = max(1, score - path.entry_pressure)
            score = max(1, score - path.loop_penalty)
            raw_scores.append(score)

        total = sum(raw_scores)
        if total <= 0:
            return [1 for _ in paths]

        quotas = [
            max(1, (nb_drones * score) // total)
            for score in raw_scores
        ]

        while sum(quotas) < nb_drones:
            best_index = max(
                range(len(paths)),
                key=lambda i: raw_scores[i] - quotas[i],
            )
            quotas[best_index] += 1

        # If we overshot due to max(1,...), trim from weakest paths.
        while sum(quotas) > nb_drones:
            weakest_index = min(
                range(len(paths)),
                key=lambda i: (quotas[i], raw_scores[i]),
            )
            if quotas[weakest_index] > 1:
                quotas[weakest_index] -= 1
            else:
                break

        return quotas

    def _next_available_path_index(
        self,
        quotas: List[int],
        start_index: int,
    ) -> int | None:
        """Find the next index with a positive quota, scanning circularly.

        Args:
            quotas: List of integers representing remaining quota per path.
            start_index: Index to begin the search from.

        Returns:
            Index of the next available path or `None` when none are left.
        """
        if not quotas:
            return None

        idx = start_index
        for _ in range(len(quotas)):
            if quotas[idx] > 0:
                return idx
            idx = (idx + 1) % len(quotas)

        return None

    def _generate_candidate_paths(
        self,
        start: str,
        goal: str,
    ) -> List[List[str]]:
        """Generate a list of candidate simple paths by perturbing the
        graph and computing alternatives.

        The method seeds the candidate set with the shortest path and then
        explores edge- and node-based variations to discover disjoint or
        complementary routes.

        Args:
            start: Start zone name.
            goal: Goal zone name.

        Returns:
            A list of candidate paths; each path is a list of zone names.
        """
        candidates: List[List[str]] = []
        seen: Set[Tuple[str, ...]] = set()

        def add_path(path: List[str]) -> None:
            """Add a candidate path if it has not been seen.

            This small helper normalizes the list into a tuple key and
            appends it to `candidates` only once.

            Args:
                path: Ordered list of zone names forming the candidate.
            """
            key = tuple(path)
            if key not in seen and path:
                seen.add(key)
                candidates.append(path)

        try:
            best_path = self.path_finder.find_shortest_path(
                self.graph,
                start,
                goal,
            )
            add_path(best_path)
        except PathFinderError as error:
            raise PathFinderError(f"Cannot build paths: {error}") from error

        first_path = candidates[0]

        self._try_edge_variants(start, goal, first_path, add_path)
        self._try_node_variants(start, goal, first_path, add_path)

        return candidates

    def _try_edge_variants(
        self,
        start: str,
        goal: str,
        base_path: List[str],
        add_path: Callable[[List[str]], None],
    ) -> None:
        """Attempt to find alternate routes by banning edges from the
        base path and invoking the path finder.

        Args:
            start: Start zone name.
            goal: Goal zone name.
            base_path: The base path used as a source of banned edges.
            add_path: Callback to register discovered candidate paths.
        """
        for i in range(len(base_path) - 1):
            banned_edges = {_edge_key(base_path[i], base_path[i + 1])}
            self._try_add_alternative(start, goal, banned_edges, add_path)

        for i in range(len(base_path) - 2):
            banned_edges = {
                _edge_key(base_path[i], base_path[i + 1]),
                _edge_key(base_path[i + 1], base_path[i + 2]),
            }
            self._try_add_alternative(start, goal, banned_edges, add_path)

        banned_edges = {
            _edge_key(left, right)
            for left, right in zip(base_path, base_path[1:])
        }
        self._try_add_alternative(start, goal, banned_edges, add_path)

    def _try_node_variants(
        self,
        start: str,
        goal: str,
        base_path: List[str],
        add_path: Callable[[List[str]], None],
    ) -> None:
        """Search for alternate paths by avoiding potentially congested
        nodes found on the base path.

        Args:
            start: Start zone name.
            goal: Goal zone name.
            base_path: The original path to analyze for bottlenecks.
            add_path: Callback to register discovered candidate paths.
        """
        for zone_name in base_path[1:-1]:
            zone = self.graph.zones.get(zone_name)
            if zone is None:
                continue

            if zone.max_drones == 1 or zone.zone_type in {"restricted"}:
                self._try_add_node_avoiding_path(
                    start,
                    goal,
                    zone_name,
                    add_path,
                )

    def _try_add_alternative(
        self,
        start: str,
        goal: str,
        banned_edges: Set[Tuple[str, str]],
        add_path: Callable[[List[str]], None],
    ) -> None:
        """Try to compute and register an alternative path avoiding
        `banned_edges`.

        Args:
            start: Start zone name.
            goal: Goal zone name.
            banned_edges: Set of undirected edges to avoid.
            add_path: Callback to append a discovered path to candidates.
        """
        try:
            alt = self.path_finder.find_alternative_path(
                self.graph,
                start,
                goal,
                banned_edges=banned_edges,
            )
            add_path(alt)
        except PathFinderError:
            pass

    def _try_add_node_avoiding_path(
        self,
        start: str,
        goal: str,
        banned_node: str,
        add_path: Callable[[List[str]], None],
    ) -> None:
        """Perform a BFS that avoids a single node and registers the
        discovered path via `add_path`.

        Args:
            start: Start zone name.
            goal: Goal zone name.
            banned_node: Node to avoid when searching.
            add_path: Callback to add found paths to candidates.
        """
        queue: deque[list[str]] = deque([[start]])
        visited: Set[str] = {start}

        while queue:
            path = queue.popleft()
            current = path[-1]

            if current == goal:
                add_path(path)
                return

            for neighbor in self.graph.adjacency.get(current, []):
                if neighbor == banned_node:
                    continue

                zone = self.graph.zones.get(neighbor)
                if zone is None:
                    continue
                if zone.zone_type == "blocked":
                    continue
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                queue.append(path + [neighbor])

    def _score_path(self, path: List[str]) -> PathInfo:
        """Compute heuristic scores for a path and return `PathInfo`.

        The scoring aggregates traversal cost, penalties for bottlenecks,
        restricted zones and loops, and bonuses for priority zones. The
        result includes both a normalized `cost` and auxiliary
        measurements used by the planner.

        Args:
            path: Ordered list of zone names forming a candidate.

        Returns:
            `PathInfo` populated with score components and metadata.
        """
        cost = 0
        priority_bonus = 0
        bottleneck_penalty = 0
        restricted_penalty = 0
        loop_penalty = 0
        entry_pressure = 0
        estimated_capacity = 999999
        length = len(path)

        seen_nodes: Set[str] = set()

        for index, zone_name in enumerate(path):
            zone = self.graph.zones.get(zone_name)
            if zone is None:
                continue

            if zone_name in seen_nodes:
                loop_penalty += 4
            else:
                seen_nodes.add(zone_name)

            if zone.zone_type == "priority":
                priority_bonus += 3
                cost += 1
            elif zone.zone_type == "restricted":
                restricted_penalty += 3
                cost += 2
            elif zone.zone_type == "blocked":
                raise PathFinderError("Blocked zone found in path")
            else:
                cost += 1

            if zone.max_drones == 1 and zone_name not in {"start", "goal"}:
                bottleneck_penalty += 2

            if index == 1:
                entry_pressure = self._estimate_entry_pressure(zone_name)

            if zone_name not in {"start", "goal"}:
                estimated_capacity = min(estimated_capacity, zone.max_drones)

        if estimated_capacity == 999999:
            estimated_capacity = 1

        cost = (
            cost
            + restricted_penalty
            + bottleneck_penalty
            + loop_penalty
            - priority_bonus
        )
        cost = max(1, cost)

        return PathInfo(
            nodes=path,
            cost=cost,
            priority_bonus=priority_bonus,
            bottleneck_penalty=bottleneck_penalty,
            restricted_penalty=restricted_penalty,
            length=length,
            loop_penalty=loop_penalty,
            entry_pressure=entry_pressure,
            estimated_capacity=estimated_capacity,
        )

    def _estimate_entry_pressure(self, zone_name: str) -> int:
        """
        Estimate how congested the first non-start zone is.

        The more neighbors and the lower the capacity, the higher the pressure.
        """
        zone = self.graph.zones.get(zone_name)
        if zone is None:
            return 1

        degree = len(self.graph.adjacency.get(zone_name, []))
        pressure = degree

        if zone.max_drones == 1:
            pressure += 3
        elif zone.max_drones == 2:
            pressure += 1

        if zone.zone_type == "restricted":
            pressure += 2
        if zone.zone_type == "priority":
            pressure -= 1

        return max(1, pressure)

    def _path_sort_key(
        self,
        path_info: PathInfo,
    ) -> tuple[int, int, int, int, int]:
        """Key function to sort `PathInfo` values from best to worst.

        The tuple orders by cost, entry pressure, restricted penalty,
        loop penalty and negated priority bonus so that standard tuple
        sorting yields the desired ranking.
        """
        return (
            path_info.cost,
            path_info.entry_pressure,
            path_info.restricted_penalty,
            path_info.loop_penalty,
            -path_info.priority_bonus,
        )
