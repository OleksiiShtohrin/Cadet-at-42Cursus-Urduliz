from __future__ import annotations

from typing import Any, Dict, List, Tuple


def draw_zones(
    vis: Any,
    screen: Any,
    graph: Any,
    positions: Dict[str, Tuple[int, int]],
    occupancy: Dict[str, int],
    drones: List[Any],
    layout: Any,
) -> None:
    """Draw zone circles, outlines, labels, and occupancy badges.

    Args:
        vis: The visualizer instance providing helpers like `_zone_color`.
        screen: Pygame surface to draw onto.
        graph: Graph containing zones keyed by name.
        positions: Mapping of zone name to pixel (x, y) coordinates.
        occupancy: Mapping of zone name to current occupancy count.
        drones: List of drone objects for end/start zone counting.
        layout: Computed `_Layout` instance for clamping label positions.

    This function uses `vis._zone_color` and `vis._label_color` to determine
    colors and places label/occupancy text clamped inside the board.
    """
    import pygame

    base_radius = vis._node_radius(layout, len(graph.zones))
    label_font = pygame.font.SysFont("DejaVu Sans", max(14, base_radius // 2))
    occupancy_font = pygame.font.SysFont("DejaVu Sans", 14, bold=True)

    for zone in graph.zones.values():
        pos = positions.get(zone.name)
        if pos is None:
            continue

        color = vis._zone_color(zone)
        outline_color = (58, 58, 62)
        radius = vis._zone_radius(zone, base_radius)

        pygame.draw.circle(screen, color, pos, radius)
        pygame.draw.circle(screen, outline_color, pos, radius, 4)

        label_lines = vis._wrap_label(zone.name, radius)
        label_surfaces = [
            label_font.render(line, True, vis._label_color(zone))
            for line in label_lines
        ]

        line_height = label_font.get_height() + 1
        total_height = line_height * len(label_surfaces)
        top = pos[1] - radius - 10 - total_height
        for index, surface in enumerate(label_surfaces):
            line_y = top + (index * line_height)
            safe_x, safe_y = vis._clamp_to_board(
                pos[0], line_y, layout, padding=20
            )
            label_rect = surface.get_rect(
                center=(safe_x, safe_y)
            )
            screen.blit(surface, label_rect)

        used = occupancy.get(zone.name, 0)
        cap = zone.max_drones
        if zone.is_end:
            used = sum(
                1
                for drone in drones
                if drone.current_zone == zone.name or drone.finished
            )
            cap = max(cap, used)
        elif zone.is_start:
            cap = max(cap, used)

        occupancy_text = occupancy_font.render(
            f"{used}/{cap}", True, (0, 0, 0)
        )
        occ_x, occ_y = vis._clamp_to_board(
            pos[0], pos[1] + radius + 16, layout, padding=20
        )
        occupancy_rect = occupancy_text.get_rect(center=(occ_x, occ_y))
        screen.blit(occupancy_text, occupancy_rect)
