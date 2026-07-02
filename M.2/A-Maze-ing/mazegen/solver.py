"""Maze solver module.

This module finds the shortest path between the entry and exit cells using
breadth-first search (BFS). The solver works on the internal wall-bitmask
representation used by the maze generator.
"""

from collections import deque
from typing import Deque, Dict, List, Optional, Set, Tuple

# Wall bit constants
NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8

# (direction_label, dx, dy, wall_bit_to_check_in_current_cell)
_DIRECTIONS: List[Tuple[str, int, int, int]] = [
    ("N", 0, -1, NORTH),
    ("E", 1, 0, EAST),
    ("S", 0, 1, SOUTH),
    ("W", -1, 0, WEST),
]


def solve(
    grid: List[List[int]],
    width: int,
    height: int,
    entry: Tuple[int, int],
    exit_pos: Tuple[int, int],
) -> Optional[List[str]]:
    """Find the shortest path from the entry cell to the exit cell.

    The maze is treated as an unweighted graph, so breadth-first search is
    used to guarantee the shortest valid path when one exists.

    Args:
        grid: 2D list of wall bitmasks indexed as grid[y][x].
        width: Maze width in cells.
        height: Maze height in cells.
        entry: Starting cell coordinates (x, y).
        exit_pos: Target cell coordinates (x, y).

    Returns:
        A list of direction letters ('N', 'E', 'S', 'W') describing the
        shortest path, an empty list if entry equals exit, or None if no path
        exists.
    """
    if entry == exit_pos:
        return []

    visited: Set[Tuple[int, int]] = {entry}
    # Store predecessor for path reconstruction to avoid growing lists in queue
    parent: Dict[
        Tuple[int, int],
        Optional[Tuple[Tuple[int, int], str]]
    ] = {entry: None}
    queue: Deque[Tuple[int, int]] = deque([entry])

    while queue:
        x, y = queue.popleft()
        cell = grid[y][x]

        for direction, dx, dy, wall_bit in _DIRECTIONS:
            if cell & wall_bit:
                # wall is closed
                continue
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue
            if (nx, ny) in visited:
                continue

            visited.add((nx, ny))
            parent[(nx, ny)] = ((x, y), direction)

            if (nx, ny) == exit_pos:
                # Reconstruct path
                path: List[str] = []
                cur: Tuple[int, int] = exit_pos
                while parent[cur] is not None:
                    prev_info = parent[cur]
                    assert prev_info is not None
                    prev, d = prev_info
                    path.append(d)
                    cur = prev
                path.reverse()
                return path

            queue.append((nx, ny))
    # no path found
    return None
