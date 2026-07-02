from __future__ import annotations

from typing import Dict, Iterable, List

from models import Drone, Graph, Zone


class ANSI:
    """Collection of ANSI escape codes used for terminal coloring.

    These constants are used by the `Visualizer` to produce colored
    terminal output for zones, drones and auxiliary labels. Values include
    both standard and bright 256-color sequences.
    """

    RESET = "\033[0m"
    BOLD = "\033[1m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    YELLOW_256 = "\033[38;5;226m"
    BROWN_256 = "\033[38;5;130m"
    LIME_256 = "\033[38;5;118m"
    MAROON_256 = "\033[38;5;124m"
    PURPLE_256 = "\033[38;5;141m"
    ORANGE = "\033[38;5;208m"
    GOLD = "\033[38;5;220m"


class Visualizer:
    """Render a colored terminal visualization of the map and turns."""

    def __init__(
        self,
        enabled: bool = True,
        total_drones: int | None = None,
    ) -> None:
        """Initialize the terminal visualizer.

        Args:
            enabled: Whether terminal rendering is enabled.
            total_drones: Optional global drone count used to scale start/end
                visual capacities so the display can accommodate all drones.
        """
        self.enabled = enabled
        self.total_drones = total_drones

    def _start_visual_capacity(self, zone: Zone) -> int:
        """Return display capacity for start zone in visual mode.

        Args:
            zone: Zone instance whose capacity is requested.

        Returns:
            int: Display capacity to use for the start hub. If the visualizer
            was constructed with `total_drones` this will be the maximum of
            the zone's `max_drones` and `total_drones` to ensure the display
            can show all drones.
        """
        if self.total_drones is None:
            return zone.max_drones

        return max(zone.max_drones, self.total_drones)

    def _end_visual_capacity(self, zone: Zone) -> int:
        """Return display capacity for end zone in visual mode.

        Args:
            zone: Zone instance whose capacity is requested.

        Returns:
            int: Display capacity to use for the end hub, similar to start
            capacity logic.
        """
        if self.total_drones is None:
            return zone.max_drones

        return max(zone.max_drones, self.total_drones)

    def _ansi_from_name(self, color_name: str) -> str | None:
        """Map a metadata color name to an ANSI escape code.

        Args:
            color_name: Color token from zone metadata (e.g. "red", "lime").

        Returns:
            Optional[str]: ANSI escape code string when the name is known,
            otherwise `None`.
        """
        mapping = {
            "black": ANSI.BLACK,
            "gray": ANSI.BRIGHT_BLACK,
            "grey": ANSI.BRIGHT_BLACK,
            "red": ANSI.RED,
            "green": ANSI.GREEN,
            "yellow": ANSI.YELLOW_256,
            "blue": ANSI.BLUE,
            "magenta": ANSI.MAGENTA,
            "cyan": ANSI.CYAN,
            "white": ANSI.WHITE,
            "orange": ANSI.ORANGE,
            "lime": ANSI.LIME_256,
            "brown": ANSI.BROWN_256,
            "purple": ANSI.PURPLE_256,
            "maroon": ANSI.MAROON_256,
            "gold": ANSI.GOLD,
            "violet": ANSI.BRIGHT_MAGENTA,
            "crimson": ANSI.BRIGHT_RED,
            "darkred": ANSI.RED,
            "rainbow": ANSI.BRIGHT_CYAN,
        }
        return mapping.get(color_name.lower())

    def _zone_color(self, zone: Zone) -> str | None:
        """Determine the ANSI color for a zone.

        The function prefers an explicit `zone.color` metadata mapping and
        otherwise falls back to role/type-based defaults.

        Args:
            zone: Zone instance to inspect.

        Returns:
            Optional[str]: ANSI color code or `None` for default terminal
            coloring.
        """
        if zone.color:
            ansi = self._ansi_from_name(zone.color)
            if ansi is not None:
                return ansi

        if zone.is_start:
            return ANSI.GREEN
        if zone.is_end:
            return ANSI.RED
        if zone.zone_type == "blocked":
            return ANSI.BRIGHT_BLACK
        if zone.zone_type == "restricted":
            return ANSI.YELLOW
        if zone.zone_type == "priority":
            return ANSI.CYAN

        return None

    def _zone_extra_text(self, zone: Zone) -> str:
        """Return human-readable metadata for a zone.

        Args:
            zone: Zone instance to describe.

        Returns:
            str: Concatenated parenthetical metadata items like
            "(start) (zone=restricted) (max_drones=2)".
        """
        extras: List[str] = []

        if zone.is_start:
            extras.append("start")
        if zone.is_end:
            extras.append("goal")

        if zone.zone_type != "normal":
            extras.append(f"zone={zone.zone_type}")

        if zone.is_start:
            extras.append(f"max_drones={self._start_visual_capacity(zone)}")
        elif zone.is_end:
            extras.append(f"max_drones={self._end_visual_capacity(zone)}")
        else:
            extras.append(f"max_drones={zone.max_drones}")

        return " ".join(f"({item})" for item in extras)

    def colorize_zone(self, zone: Zone) -> str:
        """Return a colored zone label for terminal output.

        Args:
            zone: Zone instance to format.

        Returns:
            str: Zone name wrapped in ANSI color codes when appropriate.
        """
        color = self._zone_color(zone)
        label = zone.name

        if color is None:
            return label

        if zone.is_start or zone.is_end:
            return f"{ANSI.BOLD}{color}{label}{ANSI.RESET}"

        return f"{color}{label}{ANSI.RESET}"

    def colorize_drone(self, drone_id: int) -> str:
        """Return a colored drone label.

        Args:
            drone_id: Numeric drone identifier.

        Returns:
            str: Formatted label like "D1" wrapped in bright magenta ANSI.
        """
        return f"{ANSI.BRIGHT_MAGENTA}D{drone_id}{ANSI.RESET}"

    def colorize_turn_header(self, turn_index: int) -> str:
        """Return a colored turn header.

        Args:
            turn_index: Turn number to include in the header.

        Returns:
            str: Bolded "Turn X:" header string.
        """
        return f"{ANSI.BOLD}Turn {turn_index}:{ANSI.RESET}"

    def colorize_capacity(self, capacity: int) -> str:
        """Return a colored capacity label.

        Args:
            capacity: Numeric capacity to format.

        Returns:
            str: Formatted capacity string with subdued color.
        """
        return f"{ANSI.BRIGHT_BLACK}capacity={capacity}{ANSI.RESET}"

    def colorize_connection_line(
        self,
        zone_a: Zone,
        zone_b: Zone,
        capacity: int,
    ) -> str:
        """Return a colored line describing a connection.

        Args:
            zone_a: First zone in the connection.
            zone_b: Second zone in the connection.
            capacity: Link capacity used for display.

        Returns:
            str: Human-readable connection line with colored zone names.
        """
        a = self.colorize_zone(zone_a)
        b = self.colorize_zone(zone_b)
        cap = self.colorize_capacity(capacity)
        return f"  - {a} <-> {b} ({cap})"

    def render_map(self, graph: Graph) -> None:
        """Print a colored list of zones and connections.

        Args:
            graph: Graph containing `zones` and `connections` to render.

        Example:
            visualizer = Visualizer()
            visualizer.render_map(graph)
        """
        if not self.enabled:
            return

        print("\nMap visualization:")
        print("------------------")

        print("Zones:")
        for zone in graph.zones.values():
            zone_label = self.colorize_zone(zone)
            extra_text = self._zone_extra_text(zone)
            print(f"  - {zone_label} {extra_text}")

        print("Connections:")
        for connection in graph.connections:
            zone_a = graph.zones.get(connection.zone_a)
            zone_b = graph.zones.get(connection.zone_b)

            if zone_a is None or zone_b is None:
                print(
                    f"  - {connection.zone_a} <-> {connection.zone_b} "
                    f"({self.colorize_capacity(connection.max_link_capacity)})"
                )
                continue

            print(
                self.colorize_connection_line(
                    zone_a,
                    zone_b,
                    connection.max_link_capacity,
                )
            )

        print()

    def render_turn(
        self,
        turn_index: int,
        moves: List[str],
        graph: Graph,
    ) -> None:
        """Print a colored summary of one simulation turn.

        Args:
            turn_index: Numeric turn index.
            moves: List of move strings for the turn.
            graph: Graph used for move colorization.

        Returns:
            None
        """
        if not self.enabled:
            return

        if not moves:
            print(f"{self.colorize_turn_header(turn_index)} no moves")
            return

        colored_moves = [self._colorize_move(move, graph) for move in moves]
        header = self.colorize_turn_header(turn_index)
        print(f"{header} " + " ".join(colored_moves))

    def render_state(
        self,
        drones: Iterable[Drone],
        graph: Graph,
        occupancy: Dict[str, int],
    ) -> None:
        """Print current drone states and zone occupancy in one row.

        Args:
            drones: Iterable of `Drone` objects to show.
            graph: Graph used to look up zone metadata.
            occupancy: Mapping of zone name to occupancy counts.

        Returns:
            None
        """
        if not self.enabled:
            return

        drones_list = list(drones)

        drone_parts: List[str] = []
        for drone in drones_list:
            drone_parts.append(self._format_drone_state(drone, graph))

        occupancy_parts: List[str] = []
        for zone in graph.zones.values():
            occupancy_parts.append(
                self._format_zone_occupancy(zone, drones_list, occupancy)
            )

        print("State:")
        print("  Drones: " + " | ".join(drone_parts))
        print("  Zone occupancy: " + " | ".join(occupancy_parts))
        print()

    def _format_drone_state(self, drone: Drone, graph: Graph) -> str:
        """Format one drone state with color.

        Args:
            drone: Drone instance to format.
            graph: Graph for zone lookups.

        Returns:
            str: Colored state string for the drone.
        """
        drone_label = self.colorize_drone(drone.drone_id)

        if drone.finished:
            status = f"{ANSI.RED}finished{ANSI.RESET}"
        elif drone.in_transit:
            target = drone.transit_target if drone.transit_target else "?"
            status = (
                f"transit -> {self._colorize_drone_zone(target, graph)} "
                f"[{drone.transit_remaining}]"
            )
        else:
            status = self._colorize_drone_zone(drone.current_zone, graph)

        return f"{drone_label}: {status}"

    def _colorize_drone_zone(self, zone_name: str, graph: Graph) -> str:
        """Colorize a drone's current zone using the zone metadata.

        Args:
            zone_name: Zone name to colorize.
            graph: Graph used to look up the zone.

        Returns:
            str: Colored zone name or a cyan fallback when missing.
        """
        zone = graph.zones.get(zone_name)
        if zone is not None:
            colored = self.colorize_zone(zone)
            if colored:
                return colored

        return f"{ANSI.CYAN}{zone_name}{ANSI.RESET}"

    def _format_zone_occupancy(
        self,
        zone: Zone,
        drones: List[Drone],
        occupancy: Dict[str, int],
    ) -> str:
        """Format one zone occupancy entry.

        Args:
            zone: Zone instance to describe.
            drones: Current drone snapshots for delivered counts.
            occupancy: Mapping of current occupancy counts.

        Returns:
            str: Colored occupancy fragment like "A: 3/5".
        """
        zone_label = self.colorize_zone(zone)
        used = occupancy.get(zone.name, 0)

        if zone.is_start:
            capacity = self._start_visual_capacity(zone)
            return f"{zone_label}: {ANSI.GREEN}{used}/{capacity}{ANSI.RESET}"

        if zone.is_end:
            delivered = sum(1 for drone in drones if drone.finished)
            capacity = self._end_visual_capacity(zone)
            return (
                f"{zone_label}: "
                f"{ANSI.RED}{delivered}/{capacity}{ANSI.RESET}"
            )

        if zone.zone_type == "blocked":
            return f"{zone_label}: {ANSI.BRIGHT_BLACK}blocked{ANSI.RESET}"

        return (
            f"{zone_label}: "
            f"{ANSI.BLUE}{used}/{zone.max_drones}{ANSI.RESET}"
        )

    def _colorize_move(self, move: str, graph: Graph) -> str:
        """Colorize one move string using real zone metadata.

        Args:
            move: Single turn move string containing tokens.
            graph: Graph used to colorize zone names.

        Returns:
            str: Colored version of the move string.
        """
        if not move:
            return move

        parts = move.split()
        colored_parts = [
            self._colorize_move_token(part, graph)
            for part in parts
        ]
        return " ".join(colored_parts)

    def _colorize_move_token(self, token: str, graph: Graph) -> str:
        """Colorize one `D#-zone` token inside a turn line.

        Args:
            token: Token from a turn line (e.g. "D1-A" or "D2-A-B").
            graph: Graph used to colorize destinations.

        Returns:
            str: Colored token with the drone part highlighted.
        """
        if "-" not in token:
            return token

        drone_part, zone_part = token.split("-", 1)
        drone = f"{ANSI.BRIGHT_MAGENTA}{drone_part}{ANSI.RESET}"
        destination = self._colorize_destination(zone_part, graph)
        return f"{drone}-{destination}"

    def _colorize_destination(self, zone_name: str, graph: Graph) -> str:
        """Colorize destination name using the graph zone metadata.

        Args:
            zone_name: Destination token possibly containing an arrow
                (e.g. "A-B").
            graph: Graph used to look up zones.

        Returns:
            str: Colored destination string, with recursive handling of
            compound tokens.
        """
        if "-" in zone_name:
            left, right = zone_name.split("-", 1)
            left_colored = self._colorize_zone_name(left, graph)
            right_colored = self._colorize_zone_name(right, graph)
            return f"{left_colored}-{right_colored}"

        return self._colorize_zone_name(zone_name, graph)

    def _colorize_zone_name(self, zone_name: str, graph: Graph) -> str:
        """Colorize a single zone name using zone metadata or heuristics.

        Args:
            zone_name: Zone name to colorize.
            graph: Graph used to fetch zone metadata.

        Returns:
            str: Colored zone name or unmodified string when no match.
        """
        zone = graph.zones.get(zone_name)
        if zone is not None:
            color = self._zone_color(zone)
            if color is not None:
                return f"{color}{zone_name}{ANSI.RESET}"

        lowered = zone_name.lower()
        if "goal" in lowered or lowered == "end":
            return f"{ANSI.RED}{zone_name}{ANSI.RESET}"
        if "start" in lowered:
            return f"{ANSI.GREEN}{zone_name}{ANSI.RESET}"
        if "priority" in lowered:
            return f"{ANSI.CYAN}{zone_name}{ANSI.RESET}"
        if "restricted" in lowered:
            return f"{ANSI.YELLOW}{zone_name}{ANSI.RESET}"
        if "blocked" in lowered:
            return f"{ANSI.BRIGHT_BLACK}{zone_name}{ANSI.RESET}"

        return zone_name
