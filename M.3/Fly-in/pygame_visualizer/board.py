from __future__ import annotations

import math
from typing import Any, Dict, Tuple


def draw_board_background(vis: Any, screen: Any, layout: Any) -> None:
    """Draw the board and sidebar background panels.

    Args:
        vis: The visualizer instance (unused; present for API symmetry).
        screen: Pygame surface to draw onto.
        layout: Computed `_Layout` instance with panel geometry.
    """
    import pygame

    board_rect = pygame.Rect(
        layout.board_x,
        layout.board_y,
        layout.board_width,
        layout.board_height,
    )
    sidebar_rect = pygame.Rect(
        layout.sidebar_x,
        layout.sidebar_y,
        layout.sidebar_width,
        layout.sidebar_height,
    )

    shadow = board_rect.move(6, 8)
    pygame.draw.rect(
        screen,
        (223, 228, 234),
        shadow,
        border_radius=18,
    )
    pygame.draw.rect(
        screen,
        (251, 252, 253),
        board_rect,
        border_radius=18,
    )
    pygame.draw.rect(
        screen,
        (215, 220, 227),
        board_rect,
        1,
        border_radius=18,
    )

    pygame.draw.rect(
        screen,
        (247, 248, 250),
        sidebar_rect,
        border_radius=18,
    )
    pygame.draw.rect(
        screen,
        (214, 219, 226),
        sidebar_rect,
        1,
        border_radius=18,
    )


def draw_grid(
    vis: Any,
    screen: Any,
    graph: Any,
    positions: Dict[str, Tuple[int, int]],
    layout: Any,
) -> None:
    """Draw subtle guide grid lines aligned to zone positions.

    Args:
        vis: The visualizer instance.
        screen: Pygame surface to draw onto.
        graph: Graph containing zones and connections.
        positions: Mapping of zone name to pixel (x, y) coordinates.
        layout: Computed `_Layout` instance.
    """
    import pygame

    board_rect = pygame.Rect(
        layout.board_x,
        layout.board_y,
        layout.board_width,
        layout.board_height,
    )
    grid_color = (226, 230, 236)

    x_lines: Dict[int, int] = {}
    y_lines: Dict[int, int] = {}
    for zone in graph.zones.values():
        pos = positions.get(zone.name)
        if pos is None:
            continue
        x_lines.setdefault(zone.x, pos[0])
        y_lines.setdefault(zone.y, pos[1])

    for x in sorted(x_lines.values()):
        pygame.draw.line(
            screen,
            grid_color,
            (x, board_rect.top),
            (x, board_rect.bottom),
            1,
        )

    for y in sorted(y_lines.values()):
        pygame.draw.line(
            screen,
            grid_color,
            (board_rect.left, y),
            (board_rect.right, y),
            1,
        )


def draw_edges(
    vis: Any,
    screen: Any,
    graph: Any,
    positions: Dict[str, Tuple[int, int]],
    layout: Any,
) -> None:
    """Render connections between zones as stroked lines with arrowheads.

    Args:
        vis: The visualizer instance used to compute radii.
        screen: Pygame surface to draw onto.
        graph: Graph with `connections` list.
        positions: Mapping of zone name to pixel (x, y) coordinates.
        layout: Computed `_Layout` instance.

    The function draws a dual-toned stroked line for each connection and an
    arrowhead polygon at the target end. Line thickness scales with
    connection capacity.
    """
    import pygame

    base_radius = vis._node_radius(layout, len(graph.zones))

    for connection in graph.connections:
        pos_a = positions.get(connection.zone_a)
        pos_b = positions.get(connection.zone_b)
        if pos_a is None or pos_b is None:
            continue

        zone_a = graph.zones.get(connection.zone_a)
        zone_b = graph.zones.get(connection.zone_b)
        if zone_a is None or zone_b is None:
            continue

        dx = pos_b[0] - pos_a[0]
        dy = pos_b[1] - pos_a[1]
        length = math.hypot(dx, dy)
        if length < 1:
            continue

        unit_x = dx / length
        unit_y = dy / length
        radius_a = vis._zone_radius(zone_a, base_radius)
        radius_b = vis._zone_radius(zone_b, base_radius)

        start_x = pos_a[0] + (unit_x * (radius_a + 2))
        start_y = pos_a[1] + (unit_y * (radius_a + 2))
        end_x = pos_b[0] - (unit_x * (radius_b + 2))
        end_y = pos_b[1] - (unit_y * (radius_b + 2))

        width = max(3, min(8, 2 + connection.max_link_capacity))
        pygame.draw.line(
            screen,
            (201, 206, 214),
            (start_x, start_y),
            (end_x, end_y),
            width + 2,
        )
        pygame.draw.line(
            screen,
            (113, 122, 133),
            (start_x, start_y),
            (end_x, end_y),
            width,
        )

        arrow_length = 22
        arrow_width = 14
        tip_x = end_x
        tip_y = end_y
        back_x = tip_x - (unit_x * arrow_length)
        back_y = tip_y - (unit_y * arrow_length)
        left_x = back_x + (-unit_y * arrow_width)
        left_y = back_y + (unit_x * arrow_width)
        right_x = back_x - (-unit_y * arrow_width)
        right_y = back_y - (unit_x * arrow_width)

        pygame.draw.polygon(
            screen,
            (201, 206, 214),
            [
                (tip_x, tip_y),
                (left_x, left_y),
                (right_x, right_y),
            ],
        )
        inner_left_x = (left_x * 0.94) + (tip_x * 0.06)
        inner_left_y = (left_y * 0.94) + (tip_y * 0.06)
        inner_right_x = (right_x * 0.94) + (tip_x * 0.06)
        inner_right_y = (right_y * 0.94) + (tip_y * 0.06)
        pygame.draw.polygon(
            screen,
            (113, 122, 133),
            [
                (tip_x, tip_y),
                (inner_left_x, inner_left_y),
                (inner_right_x, inner_right_y),
            ],
        )
