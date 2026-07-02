from __future__ import annotations

import math
import os
import textwrap
from typing import Dict, List, Tuple

from models import Drone, Graph, Zone
from simulator import TurnSnapshot

from .layout import _Layout
from .board import draw_board_background, draw_grid, draw_edges
from .zones import draw_zones
from .drones import draw_drones
from .sidebar import draw_sidebar


class PygameVisualizer:
    """Render simulation snapshots in a simple pygame window.

    This class manages a pygame window and renders `TurnSnapshot` frames
    using helper drawing functions split across the `pygame_visualizer`
    package.

    Example:
        vis = PygameVisualizer(fps=2.0)
        vis.run(graph, snapshots, map_title="My Map", map_path=map_file)
    """

    def __init__(self, fps: float = 1.6) -> None:
        """Initialize the visualizer and set the target FPS.

        Args:
            fps: Target playback frames per second (clamped to >= 0.5).
        """
        self.fps = max(0.5, float(fps))
        self._challenge_mode = False

    def run(
        self,
        graph: Graph,
        snapshots: List[TurnSnapshot],
        map_title: str | None = None,
        map_path: str | None = None,
    ) -> None:
        """Start the pygame visualization loop and handle events.

        Args:
            graph: Graph object containing zones and connections.
            snapshots: Sequence of `TurnSnapshot` frames to render.
            map_title: Optional title used for the window caption.
            map_path: Optional map file path; used to detect challenge mode.

        Raises:
            RuntimeError: If `pygame` is not importable.
        """
        try:
            import pygame
        except ModuleNotFoundError as error:
            raise RuntimeError(
                "pygame is not installed. Run 'make install' "
                "or 'pip install pygame'."
            ) from error

        pygame.init()
        display_title = map_title.strip() if map_title else "Fly-in simulation"
        pygame.display.set_caption(
            f"Fly-in pygame visualization - {display_title}"
        )

        self._challenge_mode = bool(
            map_path and "challenger" in map_path.split("/")
        )

        layout = self._build_layout(graph)
        screen = pygame.display.set_mode((layout.width, layout.height))
        clock = pygame.time.Clock()

        title_font = pygame.font.SysFont("DejaVu Sans", 28, bold=True)
        body_font = pygame.font.SysFont("DejaVu Sans", 18)
        small_font = pygame.font.SysFont("DejaVu Sans", 15)

        snapshots = self._prepend_turn_zero_snapshot(graph, snapshots)
        positions = self._compute_positions(graph, layout)

        if not snapshots:
            snapshots = [
                TurnSnapshot(
                    turn_index=0,
                    moves=["No moves"],
                    drones=[],
                    zone_occupancy={name: 0 for name in graph.zones},
                )
            ]

        frame_index = 0
        elapsed = 0.0
        frame_duration = 1.0 / self.fps
        headless_mode = os.environ.get("SDL_VIDEODRIVER") == "dummy"
        running = True
        paused = False

        while running:
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        running = False
                    elif event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key == pygame.K_RIGHT:
                        frame_index = min(frame_index + 1, len(snapshots) - 1)
                        elapsed = 0.0
                    elif event.key == pygame.K_LEFT:
                        frame_index = max(frame_index - 1, 0)
                        elapsed = 0.0

            if not paused and frame_index < len(snapshots) - 1:
                elapsed += dt
                if elapsed >= frame_duration:
                    frame_index += 1
                    elapsed = 0.0

            snapshot = snapshots[frame_index]

            screen.fill((240, 242, 245))
            draw_board_background(self, screen, layout)
            draw_grid(self, screen, graph, positions, layout)
            draw_edges(self, screen, graph, positions, layout)
            draw_zones(
                self,
                screen,
                graph,
                positions,
                snapshot.zone_occupancy,
                snapshot.drones,
                layout,
            )
            draw_drones(
                self,
                screen,
                graph,
                positions,
                snapshot.drones,
                layout,
            )
            draw_sidebar(
                self,
                screen,
                graph,
                snapshot,
                layout,
                paused,
                title_font,
                body_font,
                small_font,
            )

            pygame.display.flip()

            if headless_mode and frame_index >= len(snapshots) - 1:
                running = False

        pygame.quit()
        self._challenge_mode = False

    def _build_layout(self, graph: Graph) -> _Layout:
        """Compute window and panel geometry for the given graph.

        Args:
            graph: Graph used to compute spatial extents.

        Returns:
            _Layout: Computed layout with board and sidebar rectangles.
        """
        x_values = [zone.x for zone in graph.zones.values()]
        y_values = [zone.y for zone in graph.zones.values()]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)

        x_span = max(1, max_x - min_x)
        y_span = max(1, max_y - min_y)

        if self._challenge_mode:
            board_width = max(1900, min(3400, 480 + (x_span * 290)))
            board_height = max(900, min(1240, 360 + (y_span * 210)))
            board_padding = 64
        else:
            board_width = max(1600, min(2800, 440 + (x_span * 250)))
            board_height = max(900, min(1180, 380 + (y_span * 220)))
            board_padding = 72

        sidebar_width = 360
        gap = 24
        outer_padding = 24

        width = board_width + sidebar_width + gap + (outer_padding * 2)
        height = max(board_height + (outer_padding * 2), 1000)

        board_x = outer_padding
        board_y = outer_padding
        sidebar_x = board_x + board_width + gap
        sidebar_y = board_y

        return _Layout(
            width=width,
            height=height,
            board_x=board_x,
            board_y=board_y,
            board_width=board_width,
            board_height=board_height,
            sidebar_x=sidebar_x,
            sidebar_y=sidebar_y,
            sidebar_width=sidebar_width,
            sidebar_height=board_height,
            board_padding=board_padding,
        )

    def _compute_positions(
        self,
        graph: Graph,
        layout: _Layout,
    ) -> Dict[str, Tuple[int, int]]:
        """Map graph coordinates into screen pixel coordinates.

        Args:
            graph: Graph containing zone coordinates.
            layout: Computed `_Layout` instance for board geometry.

        Returns:
            Dict[str, Tuple[int, int]]: Mapping of zone name to (x, y).
        """
        x_values = [zone.x for zone in graph.zones.values()]
        y_values = [zone.y for zone in graph.zones.values()]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)

        range_x = max(1, max_x - min_x)
        range_y = max(1, max_y - min_y)

        draw_w = layout.board_width - (2 * layout.board_padding)
        draw_h = layout.board_height - (2 * layout.board_padding)

        positions: Dict[str, Tuple[int, int]] = {}
        for zone in graph.zones.values():
            norm_x = (zone.x - min_x) / range_x
            norm_y = (zone.y - min_y) / range_y

            px = int(
                layout.board_x
                + layout.board_padding
                + (norm_x * draw_w)
            )
            py = int(
                layout.board_y
                + layout.board_padding
                + (norm_y * draw_h)
            )
            positions[zone.name] = (px, py)

        return positions

    pass

    def _node_radius(self, layout: _Layout, zone_count: int) -> int:
        """Estimate a node radius that scales with the available board size.

        Args:
            layout: Computed `_Layout` instance.
            zone_count: Number of zones to render (affects density scaling).

        Returns:
            int: Radius in pixels to use for zone circles.
        """
        usable_w = max(1, layout.board_width - (2 * layout.board_padding))
        usable_h = max(1, layout.board_height - (2 * layout.board_padding))
        scale = min(usable_w, usable_h)
        density_factor = 1.0
        if self._challenge_mode:
            density_factor *= 0.82
        if zone_count >= 24:
            density_factor *= 0.76
        elif zone_count >= 16:
            density_factor *= 0.88
        return max(18, min(44, int(scale * 0.13 * density_factor)))

    def _zone_radius(self, zone: Zone, base_radius: int) -> int:
        """Adjust base node radius for a specific zone role.

        Args:
            zone: Zone object with role flags.
            base_radius: Base radius computed for the board size.

        Returns:
            int: Adjusted radius for the zone.
        """
        radius = base_radius
        if zone.is_start or zone.is_end:
            radius += 8
        if self._challenge_mode:
            radius -= 3
        if self._is_dead_zone(zone):
            radius -= 4
        return max(16, radius)

    def _prepend_turn_zero_snapshot(
        self,
        graph: Graph,
        snapshots: List[TurnSnapshot],
    ) -> List[TurnSnapshot]:
        """Ensure snapshots start at turn index zero by prepending a frame.

        If the first snapshot already has `turn_index == 0` this returns the
        original list. Otherwise a synthetic TurnSnapshot is created that
        places drones at the start zone.

        Args:
            graph: Graph used to locate the start zone.
            snapshots: Original list of snapshots.

        Returns:
            List[TurnSnapshot]: Possibly-extended list beginning at turn 0.
        """
        if not snapshots:
            return [
                TurnSnapshot(
                    turn_index=0,
                    moves=["Turn 0"],
                    drones=[],
                    zone_occupancy={name: 0 for name in graph.zones},
                )
            ]

        if snapshots[0].turn_index == 0:
            return snapshots

        try:
            start_zone = next(
                zone.name for zone in graph.zones.values() if zone.is_start
            )
        except StopIteration:
            return snapshots

        initial_drones = [
            Drone(drone_id=drone.drone_id, current_zone=start_zone)
            for drone in snapshots[0].drones
        ]

        return [
            TurnSnapshot(
                turn_index=0,
                moves=["Turn 0"],
                drones=initial_drones,
                zone_occupancy={
                    name: (len(initial_drones) if name == start_zone else 0)
                    for name in graph.zones
                },
            ),
            *snapshots,
        ]

    def _is_dead_zone(self, zone: Zone) -> bool:
        """Return True if zone name suggests a dead-end or trap.

        This looks for common substrings like "dead" or "trap" in the name.
        """
        lowered = zone.name.lower()
        return "dead" in lowered or "trap" in lowered

    def _clamp_to_board(
        self,
        x: int,
        y: int,
        layout: _Layout,
        padding: int,
    ) -> Tuple[int, int]:
        """Clamp drawing coordinates into the board rectangle.

        Args:
            x: Desired x-coordinate.
            y: Desired y-coordinate.
            layout: Computed `_Layout` instance.
            padding: Extra padding to respect from the board edges.

        Returns:
            Tuple[int, int]: Clamped (x, y) coordinates inside the board.
        """
        min_x = layout.board_x + padding
        max_x = layout.board_x + layout.board_width - padding
        min_y = layout.board_y + padding
        max_y = layout.board_y + layout.board_height - padding
        clamped_x = max(min_x, min(max_x, x))
        clamped_y = max(min_y, min(max_y, y))
        return clamped_x, clamped_y

    def _transit_drone_position(
        self,
        drone: Drone,
        graph: Graph,
        positions: Dict[str, Tuple[int, int]],
        layout: _Layout,
    ) -> Tuple[int, int]:
        """Compute a pixel position for a drone in transit between zones.

        Args:
            drone: Drone object containing `current_zone` and `transit_target`.
            graph: Graph used to look up zone metadata.
            positions: Mapping of zone name to screen coordinates.
            layout: Computed `_Layout` instance.

        Returns:
            Tuple[int, int]: Pixel coordinates (x, y) or (0, 0) if unknown.
        """
        from_name = drone.current_zone
        to_name = drone.transit_target
        if from_name is None or to_name is None:
            return 0, 0

        pos_a = positions.get(from_name)
        pos_b = positions.get(to_name)
        zone_a = graph.zones.get(from_name)
        zone_b = graph.zones.get(to_name)
        if pos_a is None or pos_b is None or zone_a is None or zone_b is None:
            return 0, 0

        dx = pos_b[0] - pos_a[0]
        dy = pos_b[1] - pos_a[1]
        length = math.hypot(dx, dy)
        if length < 1:
            return int(pos_a[0]), int(pos_a[1])

        unit_x = dx / length
        unit_y = dy / length
        base_radius = self._node_radius(layout, len(graph.zones))
        radius_a = self._zone_radius(zone_a, base_radius)
        radius_b = self._zone_radius(zone_b, base_radius)
        start_x = pos_a[0] + (unit_x * (radius_a + 2))
        start_y = pos_a[1] + (unit_y * (radius_a + 2))
        end_x = pos_b[0] - (unit_x * (radius_b + 2))
        end_y = pos_b[1] - (unit_y * (radius_b + 2))

        progress = 0.68
        cx = start_x + ((end_x - start_x) * progress)
        cy = start_y + ((end_y - start_y) * progress)
        return int(cx), int(cy)

    def _wrap_label(self, label: str, radius: int) -> List[str]:
        """Wrap a zone label into up to two compact lines.

        Args:
            label: Original zone label.
            radius: Zone radius used to estimate wrap width.

        Returns:
            List[str]: One or two lines suitable for rendering as a label.
        """
        width = max(8, int(radius / 2.5))
        lines = textwrap.wrap(
            label,
            width=width,
            break_long_words=True,
            break_on_hyphens=False,
        )
        if not lines:
            return [label]
        if len(lines) > 2:
            return [lines[0], "".join(lines[1:])]
        return lines

    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Wrap sidebar text preserving readability and hyphenation.

        Args:
            text: Text to wrap.
            width: Column width to wrap to.

        Returns:
            List[str]: Wrapped lines or a single-item list with original text.
        """
        return textwrap.wrap(
            text,
            width=width,
            break_long_words=True,
            break_on_hyphens=False,
        ) or [text]

    def _label_color(self, zone: Zone) -> Tuple[int, int, int]:
        """Return RGB color used for zone labels.

        Args:
            zone: Zone instance (provided for future customization).

        Returns:
            Tuple[int, int, int]: RGB triple.
        """
        return (0, 0, 0)

    def _zone_color(self, zone: Zone) -> Tuple[int, int, int]:
        """Return RGB color for a zone, preferring metadata values.

        The function first checks `zone.color` (map metadata) and attempts to
        parse it. If parsing fails or no color is supplied, role/type-based
        defaults are returned.

        Args:
            zone: Zone instance with metadata fields like `color`.

        Returns:
            Tuple[int, int, int]: RGB triple.
        """
        # If an explicit color is provided in the map metadata, prefer it.
        if zone.color:
            mapped = self._color_name_to_rgb(zone.color)
            if mapped is not None:
                return mapped

        # Fallback to role/type-based defaults when no explicit color.
        if zone.is_start:
            return (34, 197, 94)
        if zone.is_end:
            return (239, 68, 68)
        if zone.zone_type == "blocked":
            return (75, 85, 99)
        if zone.zone_type == "restricted":
            return (245, 158, 11)
        if zone.zone_type == "priority":
            return (56, 189, 248)

        return (71, 85, 105)

    def _color_name_to_rgb(
        self,
        color_name: str,
    ) -> Tuple[int, int, int] | None:
        """Best-effort color mapping from map metadata.

        Supports named colors, hex codes ("#rrggbb" or "rrggbb"), and
        functional `rgb(r,g,b)` values. Returns None when parsing fails.

        Args:
            color_name: Color string from map metadata.

        Returns:
            Optional[Tuple[int, int, int]]: RGB triple or `None`.
        """
        if not color_name:
            return None

        text = color_name.strip()

        # Accept hex codes: #rrggbb or rrggbb
        if text.startswith("#"):
            text = text[1:]
        if len(text) == 6:
            try:
                r = int(text[0:2], 16)
                g = int(text[2:4], 16)
                b = int(text[4:6], 16)
                return (r, g, b)
            except ValueError:
                pass

        # Accept rgb(r,g,b)
        lower = text.lower()
        if lower.startswith("rgb(") and lower.endswith(")"):
            try:
                parts = lower[4:-1].split(",")
                if len(parts) == 3:
                    r = int(parts[0].strip())
                    g = int(parts[1].strip())
                    b = int(parts[2].strip())
                    return (r, g, b)
            except Exception:
                pass

        mapping = {
            "red": (239, 68, 68),
            "green": (34, 197, 94),
            "blue": (59, 130, 246),
            "yellow": (250, 204, 21),
            "orange": (249, 115, 22),
            "purple": (168, 85, 247),
            "cyan": (34, 211, 238),
            "gray": (107, 114, 128),
            "grey": (107, 114, 128),
            "black": (17, 24, 39),
            "white": (241, 245, 249),
            "brown": (146, 64, 14),
            "gold": (234, 179, 8),
            "maroon": (153, 27, 27),
            "violet": (124, 58, 237),
            "lime": (132, 204, 22),
        }
        return mapping.get(color_name.lower())
