"""Pattern helpers and wall constants for the maze generator.

This module defines the wall bit flags used across the project and provides
helpers to build and validate the centered visible 42 pattern.
"""

from __future__ import annotations

from typing import Set, Tuple

# Wall bit constants
NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8

# Visible 42 fits in a 7x5 box.
PATTERN_WIDTH: int = 7
PATTERN_HEIGHT: int = 5


def build_42_pattern(origin_x: int, origin_y: int) -> Set[Tuple[int, int]]:
    """Build the set of coordinates occupied by the visible 42 pattern.

    The pattern is represented as a set of maze cells that should be fully
    closed. Empty cells are not included.

    Args:
        origin_x: X coordinate of the top-left corner of the pattern.
        origin_y: Y coordinate of the top-left corner of the pattern.

    Returns:
        A set of (x, y) coordinates belonging to the 42 pattern.
    """
    cells: Set[Tuple[int, int]] = set()

    four = [
        (0, 0), (2, 0),
        (0, 1), (2, 1),
        (0, 2), (1, 2), (2, 2),
        (2, 3),
        (2, 4),
    ]

    two = [
        (4, 0), (5, 0), (6, 0),
        (6, 1),
        (4, 2), (5, 2), (6, 2),
        (4, 3),
        (4, 4), (5, 4), (6, 4),
    ]

    for dx, dy in four + two:
        cells.add((origin_x + dx, origin_y + dy))

    return cells


def can_place_42(width: int, height: int) -> bool:
    """Check whether the 42 pattern fits inside a maze of given size.

    The pattern needs enough room so it can be centered with at least one
    cell of margin around it.

    Args:
        width: Maze width in cells.
        height: Maze height in cells.

    Returns:
        True if the 42 pattern can be placed, otherwise False.
    """
    return width >= PATTERN_WIDTH + 2 and height >= PATTERN_HEIGHT + 2
