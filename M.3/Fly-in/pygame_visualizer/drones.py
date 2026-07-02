from __future__ import annotations

from typing import Any, Dict, List, Tuple


def draw_drones(
    vis: Any,
    screen: Any,
    graph: Any,
    positions: Dict[str, Tuple[int, int]],
    drones: List[Any],
    layout: Any,
) -> None:
    """Render drone badges both inside zones and while in transit.

    Args:
        vis: The visualizer instance for helper methods.
        screen: Pygame surface to draw onto.
        graph: Graph containing zone metadata used to size badges.
        positions: Mapping of zone name to pixel (x, y) coordinates.
        drones: List of drone objects to render.
        layout: Computed `_Layout` instance.

    Drones inside zones are laid out in a compact grid; excess drones are
    summarized with a "+N" badge. Transit drones are positioned along the
    connection line using `vis._transit_drone_position`.
    """
    import pygame

    zone_radius = vis._node_radius(layout, len(graph.zones))
    badge_font = pygame.font.SysFont("DejaVu Sans", 11, bold=True)
    transit_badge_radius = 11

    drones_by_zone: Dict[str, List[Any]] = {}
    transit_drones: List[Any] = []
    for drone in drones:
        if drone.in_transit and drone.transit_target is not None:
            transit_drones.append(drone)
            continue
        if drone.current_zone is None:
            continue
        drones_by_zone.setdefault(drone.current_zone, []).append(drone)

    for zone_name, zone_drones in drones_by_zone.items():
        base = positions.get(zone_name)
        if base is None:
            continue

        zone = graph.zones.get(zone_name)
        if zone is None:
            continue

        sorted_zone_drones = sorted(
            zone_drones, key=lambda drone_obj: drone_obj.drone_id
        )
        if zone.is_start or zone.is_end:
            grid_cols = 4
            badge_radius = 11
            grid_spacing = 20
            max_visible = 16
        else:
            grid_cols = 3
            badge_radius = 13
            grid_spacing = 27
            max_visible = 9

        for index, drone in enumerate(sorted_zone_drones[:max_visible]):
            row = index // grid_cols
            col = index % grid_cols
            offset_x = (col - ((grid_cols - 1) / 2)) * grid_spacing
            offset_y = (row - ((grid_cols - 1) / 2)) * grid_spacing
            cx = int(base[0] + offset_x)
            cy = int(base[1] + offset_y)
            pygame.draw.circle(
                screen, (38, 46, 58), (cx, cy), badge_radius
            )
            pygame.draw.circle(
                screen, (248, 249, 251), (cx, cy), badge_radius, 2
            )
            drone_text = badge_font.render(
                str(drone.drone_id), True, (255, 255, 255)
            )
            drone_rect = drone_text.get_rect(center=(cx, cy))
            screen.blit(drone_text, drone_rect)

        if len(zone_drones) > max_visible:
            extra = len(zone_drones) - max_visible
            extra_font = pygame.font.SysFont(
                "DejaVu Sans", 12, bold=True
            )
            extra_text = extra_font.render(
                f"+{extra}", True, (20, 24, 29)
            )
            extra_rect = extra_text.get_rect(
                center=(base[0], base[1] + zone_radius + 30)
            )
            screen.blit(extra_text, extra_rect)

    for drone in transit_drones:
        cx, cy = vis._transit_drone_position(
            drone, graph, positions, layout
        )
        if cx <= 0 and cy <= 0:
            continue
        pygame.draw.circle(
            screen, (38, 46, 58), (cx, cy), transit_badge_radius
        )
        pygame.draw.circle(
            screen, (248, 249, 251), (cx, cy), transit_badge_radius, 2
        )
        drone_text = badge_font.render(
            str(drone.drone_id), True, (255, 255, 255)
        )
        drone_rect = drone_text.get_rect(center=(cx, cy))
        screen.blit(drone_text, drone_rect)
