from __future__ import annotations

from typing import Any


def _draw_sidebar_title(
    screen: Any,
    sidebar_rect: Any,
    title_font: Any,
    small_font: Any,
) -> None:
    """Draw the sidebar header block with title and subtitle.

    Args:
        screen: Pygame surface to draw onto.
        sidebar_rect: Rectangle of the sidebar area.
        title_font: Font used for the main title.
        small_font: Font used for the subtitle.
    """
    header = title_font.render("Flight Control", True, (32, 35, 41))
    screen.blit(header, (sidebar_rect.x + 20, sidebar_rect.y + 18))

    subtitle = small_font.render(
        "Reference-style pygame view",
        True,
        (93, 101, 112),
    )
    screen.blit(
        subtitle,
        (sidebar_rect.x + 20, sidebar_rect.y + 52),
    )


def _pill(
    screen: Any,
    rect_values: Any,
    text: str,
    color: Any,
    font: Any,
) -> None:
    """Draw a pill-shaped colored label with centered text.

    Args:
        screen: Pygame surface to draw onto.
        rect_values: Iterable of four ints: (x, y, width, height).
        text: Label text to render centered inside the pill.
        color: Background color for the pill.
        font: Font used to render the text.
    """
    import pygame

    rect = pygame.Rect(*rect_values)
    pygame.draw.rect(screen, color, rect, border_radius=16)
    pygame.draw.rect(screen, (255, 255, 255), rect, 1, border_radius=16)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_sidebar(
    vis: Any,
    screen: Any,
    graph: Any,
    snapshot: Any,
    layout: Any,
    paused: bool,
    title_font: Any,
    body_font: Any,
    small_font: Any,
) -> None:
    """Render the right-hand sidebar showing controls and metrics.

    Args:
        vis: The visualizer instance (provides helper methods).
        screen: Pygame surface to draw onto.
        graph: Graph used to compute zone and connection counts.
        snapshot: Current TurnSnapshot with drones, moves, occupancy.
        layout: Computed `_Layout` instance.
        paused: Whether the simulation is currently paused.
        title_font: Font for the sidebar title.
        body_font: Font for body text and section titles.
        small_font: Smaller font for labels and controls.

    The sidebar shows status pill, key metrics, recent moves and control
    hints laid out inside the sidebar rectangle from `layout`.
    """
    import pygame

    sidebar_rect = pygame.Rect(
        layout.sidebar_x,
        layout.sidebar_y,
        layout.sidebar_width,
        layout.sidebar_height,
    )

    _draw_sidebar_title(screen, sidebar_rect, title_font, small_font)

    status = "PLAYING" if not paused else "PAUSED"
    status_color = (34, 197, 94) if not paused else (245, 158, 11)
    _pill(
        screen,
        (
            sidebar_rect.x + 20,
            sidebar_rect.y + 82,
            128,
            30,
        ),
        status,
        status_color,
        small_font,
    )

    total_drones = len(snapshot.drones)
    active_drones = sum(
        1 for drone in snapshot.drones if drone.in_transit
    )
    occupied_zones = sum(
        1 for amount in snapshot.zone_occupancy.values() if amount > 0
    )

    metrics = [
        ("Turn", str(snapshot.turn_index)),
        ("Drones", f"{total_drones} total"),
        ("In transit", str(active_drones)),
        ("Occupied", str(occupied_zones)),
        ("Zones", str(len(graph.zones))),
        ("Connections", str(len(graph.connections))),
    ]

    metrics_top = sidebar_rect.y + 130
    for index, (label, value) in enumerate(metrics):
        y = metrics_top + (index * 42)
        label_surface = small_font.render(label, True, (101, 109, 122))
        value_surface = body_font.render(value, True, (28, 31, 36))
        screen.blit(label_surface, (sidebar_rect.x + 20, y))
        screen.blit(value_surface, (sidebar_rect.x + 20, y + 18))

    move_title = body_font.render(
        "Current move",
        True,
        (32, 35, 41),
    )
    screen.blit(
        move_title,
        (sidebar_rect.x + 20, sidebar_rect.y + 392),
    )

    move_text = " ".join(snapshot.moves) if snapshot.moves else "No moves"
    move_lines = vis._wrap_text(move_text, 34)
    move_y = sidebar_rect.y + 424
    for line in move_lines[:5]:
        move_surface = small_font.render(line, True, (57, 65, 78))
        screen.blit(move_surface, (sidebar_rect.x + 20, move_y))
        move_y += 22

    controls_title = body_font.render(
        "Controls",
        True,
        (32, 35, 41),
    )
    screen.blit(
        controls_title,
        (sidebar_rect.x + 20, sidebar_rect.bottom - 152),
    )

    controls = [
        "SPACE  pause / resume",
        "LEFT   previous turn",
        "RIGHT  next turn",
        "Q or ESC quit",
    ]
    control_y = sidebar_rect.bottom - 120
    for line in controls:
        control_surface = small_font.render(line, True, (57, 65, 78))
        screen.blit(control_surface, (sidebar_rect.x + 20, control_y))
        control_y += 22
