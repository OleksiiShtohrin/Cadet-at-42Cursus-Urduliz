from __future__ import annotations

"""Data models for Fly-in: Zone, Connection, Drone and Graph.

These lightweight dataclasses represent the parsed map structure and the
mutable drone state used during simulation and visualization.

Example:
    graph = Graph()
    graph.add_zone(Zone(name="A", x=0, y=0, is_start=True))
    graph.add_zone(Zone(name="B", x=1, y=0, is_end=True))
    graph.add_connection(Connection(zone_a="A", zone_b="B"))
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Zone:
    """Represents a zone in the map.

    Attributes:
        name: Unique zone identifier.
        x: X coordinate in map units.
        y: Y coordinate in map units.
        zone_type: One of 'normal', 'blocked', 'restricted', 'priority'.
        color: Optional color metadata string from the map.
        max_drones: Maximum concurrent drones allowed in this zone.
        is_start: True for the start hub.
        is_end: True for the end hub.
        drones_inside: Current count of drones (managed by the simulator).
    """

    name: str
    x: int
    y: int
    zone_type: str = "normal"
    color: Optional[str] = None
    max_drones: int = 1
    is_start: bool = False
    is_end: bool = False
    drones_inside: int = 0


@dataclass
class Connection:
    """Represents a connection between two zones.

    Attributes:
        zone_a: Name of the first zone.
        zone_b: Name of the second zone.
        max_link_capacity: Maximum concurrent uses of this link per turn.
    """

    zone_a: str
    zone_b: str
    max_link_capacity: int = 1


@dataclass
class Drone:
    """Represents one drone in the simulation.

    Attributes:
        drone_id: Numeric ID of the drone.
        current_zone: Current zone name where the drone resides.
        path: Assigned path as a list of zone names.
        path_index: Current index in `path`.
        finished: Whether the drone reached its goal.
        in_transit: True when the drone is moving through a restricted link.
        transit_target: Target zone when in transit.
        transit_remaining: Remaining ticks for current transit.
    """

    drone_id: int
    current_zone: str
    path: List[str] = field(default_factory=list)
    path_index: int = 0
    finished: bool = False
    in_transit: bool = False
    transit_target: str | None = None
    transit_remaining: int = 0


class Graph:
    """Stores all zones and connections of the map.

    The `adjacency` mapping is maintained for quick neighbor lookup.
    """

    def __init__(self) -> None:
        """Initialize an empty Graph.

        Attributes:
            zones: Mapping of zone name to `Zone` instances.
            connections: List of `Connection` objects in the graph.
            adjacency: Neighbor mapping for quick lookups.
        """
        self.zones: Dict[str, Zone] = {}
        self.connections: List[Connection] = []
        self.adjacency: Dict[str, List[str]] = {}

    def add_zone(self, zone: Zone) -> None:
        """Add a zone to the graph.

        Args:
            zone: Zone instance to add.
        """
        self.zones[zone.name] = zone
        self.adjacency.setdefault(zone.name, [])

    def add_connection(self, connection: Connection) -> None:
        """Add a bidirectional connection to the graph.

        Args:
            connection: Connection instance describing the link.
        """
        self.connections.append(connection)
        self.adjacency.setdefault(connection.zone_a, [])
        self.adjacency.setdefault(connection.zone_b, [])
        self.adjacency[connection.zone_a].append(connection.zone_b)
        self.adjacency[connection.zone_b].append(connection.zone_a)
