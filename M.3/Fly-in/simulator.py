from __future__ import annotations

"""Simulation engine for Fly-in.

Provides a `Simulator` that executes turns, tracking drone positions,
link usage and zone occupancy. The simulator produces `TurnSnapshot`
instances suitable for rendering or text output.
"""

from dataclasses import dataclass
from typing import Dict, List

from errors import SimulationError
from models import Connection, Drone, Graph


def _edge_key(zone_a: str, zone_b: str) -> tuple[str, str]:
    """Return a normalized undirected edge key.

    The function orders the pair so edge-based dictionaries can be used
    for undirected link accounting.
    """
    if zone_a <= zone_b:
        return zone_a, zone_b
    return zone_b, zone_a


@dataclass
class PlannedMove:
    """Represents a planned move for one drone in one turn.

    Attributes:
        drone_id: Numeric drone identifier.
        from_zone: Origin zone name.
        to_zone: Destination zone name.
        is_transit: True when the move is a restricted transit.
    """

    drone_id: int
    from_zone: str
    to_zone: str
    is_transit: bool = False

    @property
    def output_target(self) -> str:
        """Return the token used in textual move output.

        For transit moves the token is "from-to"; otherwise it is the
        destination zone name.
        """
        if self.is_transit:
            return f"{self.from_zone}-{self.to_zone}"
        return self.to_zone


@dataclass
class TurnSnapshot:
    """Represents the complete simulation state for one turn.

    Attributes:
        turn_index: Turn number starting at 1.
        moves: List of textual move descriptions for the turn.
        drones: Snapshot copy of drone states.
        zone_occupancy: Mapping of zone name to occupancy counts.
    """

    turn_index: int
    moves: List[str]
    drones: List[Drone]
    zone_occupancy: Dict[str, int]


class Simulator:
    """Runs the drone simulation turn by turn.

    The simulator exposes `run` and `run_with_snapshots` which return a list
    of `TurnSnapshot` objects representing the simulation history.
    """

    def __init__(self, graph: Graph, nb_drones: int) -> None:
        """Create a new Simulator for a graph and a number of drones.

        Args:
            graph: The map `Graph` the simulator will operate on.
            nb_drones: Total number of drones to simulate.
        """
        self.graph = graph
        self.nb_drones = nb_drones
        self.drones: List[Drone] = []
        self.drones_by_id: Dict[int, Drone] = {}
        self.zone_occupancy: Dict[str, int] = {}
        self.link_usage: Dict[tuple[str, str], int] = {}
        self.assignments: Dict[int, List[str]] = {}
        self.start_zone_name: str | None = None
        self.goal_zone_name: str | None = None

    def initialize_drones(self, start_zone: str, goal_zone: str) -> None:
        """Create and place `nb_drones` drones at the start zone.

        Args:
            start_zone: Name of the start zone present in `graph`.
            goal_zone: Name of the goal zone present in `graph`.

        Raises:
            SimulationError: If either zone name is unknown.
        """
        if start_zone not in self.graph.zones:
            raise SimulationError(f"Unknown start zone: {start_zone}")
        if goal_zone not in self.graph.zones:
            raise SimulationError(f"Unknown goal zone: {goal_zone}")

        self.start_zone_name = start_zone
        self.goal_zone_name = goal_zone

        self.drones = [
            Drone(drone_id=i + 1, current_zone=start_zone)
            for i in range(self.nb_drones)
        ]
        self.drones_by_id = {drone.drone_id: drone for drone in self.drones}

        self.zone_occupancy = {zone_name: 0 for zone_name in self.graph.zones}
        self.zone_occupancy[start_zone] = self.nb_drones
        self.link_usage = {}

    def set_assignments(self, assignments: Dict[int, List[str]]) -> None:
        """Assign paths to drones.

        Args:
            assignments: Mapping from drone_id to a list of zone names.
        """
        self.assignments = assignments

        for drone in self.drones:
            path = self.assignments.get(drone.drone_id)
            if path is not None:
                drone.path = path
                drone.path_index = 0

    def run(
        self,
        start_zone: str,
        goal_zone: str,
    ) -> List[TurnSnapshot]:
        """Run the simulation and return a list of `TurnSnapshot`.

        This is a thin wrapper around the internal `_run_internal` loop that
        performs the actual turn-by-turn execution.

        Example:
            sim = Simulator(graph, nb_drones)
            sim.initialize_drones(start, goal)
            sim.set_assignments(assignments)
            snapshots = sim.run_with_snapshots(start, goal)
        """
        return self._run_internal(start_zone, goal_zone)

    def run_with_snapshots(
        self,
        start_zone: str,
        goal_zone: str,
    ) -> List[TurnSnapshot]:
        """Compatibility wrapper that delegates to `_run_internal`.

        Kept for backward compatibility with older caller code.
        """
        return self._run_internal(start_zone, goal_zone)

    def _run_internal(
        self,
        start_zone: str,
        goal_zone: str,
    ) -> List[TurnSnapshot]:
        """Internal simulation loop producing TurnSnapshot objects.

        The loop continues until all drones have finished or a deadlock
        condition is detected and `SimulationError` is raised.
        """
        if not self.drones:
            self.initialize_drones(start_zone, goal_zone)

        snapshots: List[TurnSnapshot] = []
        turn_index = 1

        while not self._all_finished(goal_zone):
            arrived_moves = self._advance_transit_drones()
            arrived_ids = {move.drone_id for move in arrived_moves}
            planned_moves = self._plan_turn(goal_zone, arrived_ids)

            if (
                not planned_moves
                and not self._any_drone_in_transit()
                and not arrived_moves
            ):
                if self._all_finished(goal_zone):
                    break
                raise SimulationError(
                    "Deadlock detected: no valid moves available"
                )

            self._apply_turn(planned_moves)

            turn_moves = arrived_moves + planned_moves

            if turn_moves:
                move_text = " ".join(
                    f"D{move.drone_id}-{move.output_target}"
                    for move in turn_moves
                )
                snapshots.append(
                    TurnSnapshot(
                        turn_index=turn_index,
                        moves=[move_text],
                        drones=self._clone_drones(),
                        zone_occupancy=self.zone_occupancy.copy(),
                    )
                )
                turn_index += 1

        return snapshots

    def _clone_drones(self) -> List[Drone]:
        """Create a deep-ish copy of current drone states for snapshots.

        Returns:
            List[Drone]: New list containing copies of `Drone` dataclasses.
        """
        cloned: List[Drone] = []
        for drone in self.drones:
            cloned.append(
                Drone(
                    drone_id=drone.drone_id,
                    current_zone=drone.current_zone,
                    path=list(drone.path),
                    path_index=drone.path_index,
                    finished=drone.finished,
                    in_transit=drone.in_transit,
                    transit_target=drone.transit_target,
                    transit_remaining=drone.transit_remaining,
                )
            )
        return cloned

    def _all_finished(self, goal_zone: str) -> bool:
        """Return True when all drones have reached `goal_zone`.

        Args:
            goal_zone: Name of the goal zone.
        """
        return all(drone.current_zone == goal_zone for drone in self.drones)

    def _plan_turn(
        self,
        goal_zone: str,
        blocked_drone_ids: set[int],
    ) -> List[PlannedMove]:
        """Plan moves for a single turn.

        Args:
            goal_zone: Name of the goal zone used to detect completion.
            blocked_drone_ids: Drone ids that are temporarily blocked.

        Returns:
            List[PlannedMove]: Moves planned for this turn.
        """
        planned_moves: List[PlannedMove] = []
        temp_occupancy = self.zone_occupancy.copy()

        for drone in self.drones:
            if drone.finished:
                continue

            if drone.drone_id in blocked_drone_ids:
                continue

            if drone.current_zone == goal_zone:
                drone.finished = True
                continue

            if drone.in_transit:
                continue

            if not drone.path:
                continue

            next_zone = self._next_zone_on_path(drone)
            if next_zone is None:
                continue

            if not self._can_move_with_occupancy(
                drone.current_zone,
                next_zone,
                temp_occupancy,
            ):
                continue

            zone = self.graph.zones.get(next_zone)
            if zone is None:
                continue

            if zone.zone_type == "restricted":
                if not self._reserve_move(drone.current_zone, next_zone):
                    continue

                temp_occupancy[drone.current_zone] -= 1

                drone.in_transit = True
                drone.transit_target = next_zone
                drone.transit_remaining = 1

                planned_moves.append(
                    PlannedMove(
                        drone_id=drone.drone_id,
                        from_zone=drone.current_zone,
                        to_zone=next_zone,
                        is_transit=True,
                    )
                )
            else:
                if not self._reserve_move(drone.current_zone, next_zone):
                    continue

                temp_occupancy[drone.current_zone] -= 1

                if next_zone != self.goal_zone_name:
                    temp_occupancy[next_zone] += 1

                planned_moves.append(
                    PlannedMove(
                        drone_id=drone.drone_id,
                        from_zone=drone.current_zone,
                        to_zone=next_zone,
                    )
                )

        return planned_moves

    def _advance_transit_drones(self) -> List[PlannedMove]:
        """Advance drones that are currently in restricted transit.

        Returns:
            List[PlannedMove]: Arrival moves for drones that reached targets.
        """
        arrivals: List[PlannedMove] = []

        for drone in self.drones:
            if not drone.in_transit:
                continue

            if drone.transit_remaining > 0:
                drone.transit_remaining -= 1

            if drone.transit_remaining != 0:
                continue

            if drone.transit_target is None:
                continue

            target = drone.transit_target
            zone = self.graph.zones.get(target)
            if zone is None:
                raise SimulationError(
                    f"Unknown transit target zone: {target}"
                )

            if target != self.goal_zone_name:
                current = self.zone_occupancy.get(target, 0)
                if current >= zone.max_drones:
                    raise SimulationError(
                        f"Transit capacity exceeded for zone: {target}"
                    )
                self.zone_occupancy[target] = current + 1

            drone.current_zone = target
            drone.path_index += 1
            drone.in_transit = False
            drone.transit_target = None
            arrivals.append(
                PlannedMove(
                    drone_id=drone.drone_id,
                    from_zone=target,
                    to_zone=target,
                )
            )

            if target == self.goal_zone_name:
                drone.finished = True

        return arrivals

    def _any_drone_in_transit(self) -> bool:
        """Return whether any drone is currently in transit.

        Returns:
            True when at least one drone has `in_transit == True`.
        """
        return any(drone.in_transit for drone in self.drones)

    def _next_zone_on_path(self, drone: Drone) -> str | None:
        """Return the next zone on the drone's assigned path.

        Args:
            drone: Drone whose path is inspected.

        Returns:
            The name of the next zone or `None` when the drone is at the
            end of its path.
        """
        next_index = drone.path_index + 1
        if next_index >= len(drone.path):
            return None
        return drone.path[next_index]

    def _can_move_with_occupancy(
        self,
        from_zone: str,
        to_zone: str,
        temp_occupancy: Dict[str, int],
    ) -> bool:
        """Check whether a drone can move using temporary turn occupancy."""
        zone = self.graph.zones.get(to_zone)
        if zone is None:
            return False

        if zone.zone_type == "blocked":
            return False

        if not self._has_connection(from_zone, to_zone):
            return False

        if not self._can_use_link(from_zone, to_zone):
            return False

        if zone.is_end:
            return True

        return temp_occupancy.get(to_zone, 0) < zone.max_drones

    def _has_connection(self, zone_a: str, zone_b: str) -> bool:
        """Check whether there exists an explicit connection between two
        zones.

        Args:
            zone_a: Name of the first zone.
            zone_b: Name of the second zone.

        Returns:
            True when `zone_b` appears in the adjacency list of `zone_a`.
        """
        neighbors = self.graph.adjacency.get(zone_a, [])
        return zone_b in neighbors

    def _get_connection(self, zone_a: str, zone_b: str) -> Connection | None:
        """Return the connection object between two zones if it exists."""
        target_key = _edge_key(zone_a, zone_b)

        for connection in self.graph.connections:
            connection_key = _edge_key(connection.zone_a, connection.zone_b)
            if connection_key == target_key:
                return connection

        return None

    def _can_use_link(self, zone_a: str, zone_b: str) -> bool:
        """Return whether the undirected link between two zones has free
        capacity for another concurrent use in this turn.

        Args:
            zone_a: One endpoint of the link.
            zone_b: The other endpoint of the link.

        Returns:
            True if the connection exists and its current usage is below
            `max_link_capacity`.
        """
        connection = self._get_connection(zone_a, zone_b)
        if connection is None:
            return False

        edge_key = _edge_key(zone_a, zone_b)
        used = self.link_usage.get(edge_key, 0)
        return used < connection.max_link_capacity

    def _reserve_move(self, zone_a: str, zone_b: str) -> bool:
        """Reserve one usage unit on the link between `zone_a` and
        `zone_b` for the current turn.

        Args:
            zone_a: Origin zone name.
            zone_b: Destination zone name.

        Returns:
            True when the reservation succeeded, False when the link is
            at capacity.
        """
        if not self._can_use_link(zone_a, zone_b):
            return False

        edge_key = _edge_key(zone_a, zone_b)
        self.link_usage[edge_key] = self.link_usage.get(edge_key, 0) + 1
        return True

    def _apply_turn(self, planned_moves: List[PlannedMove]) -> None:
        """Apply planned moves by updating drone and occupancy state.

        Args:
            planned_moves: Moves to apply this turn.
        """
        for move in planned_moves:
            drone = self.drones_by_id[move.drone_id]

            if move.is_transit:
                self.zone_occupancy[move.from_zone] = max(
                    0, self.zone_occupancy.get(move.from_zone, 0) - 1
                )
                continue

            if drone.current_zone == move.to_zone:
                continue

            self.zone_occupancy[move.from_zone] -= 1

            if move.to_zone != self.goal_zone_name:
                self.zone_occupancy[move.to_zone] += 1

            drone.current_zone = move.to_zone
            drone.path_index += 1

            if move.to_zone == self.goal_zone_name:
                drone.finished = True

        self.link_usage = {}

    def _is_goal(self, zone_name: str) -> bool:
        """Return whether the given zone name equals the configured goal
        zone.

        Args:
            zone_name: Zone name to compare with the simulator's goal.

        Returns:
            True when `zone_name` is the simulation goal.
        """
        return self.goal_zone_name == zone_name
