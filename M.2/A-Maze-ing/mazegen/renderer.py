"""Terminal renderer for the maze.

This module converts the internal maze grid into a multiline text
representation. It can display walls, entry, exit, shortest path, and the
optional visible 42 pattern. It also supports simple ANSI-based coloring.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8

_WALL = "██"
_EMPTY = "  "
_PATH = "▓▓"
_ENTRY = "▓▓"
_EXIT = "▓▓"
_CELL_42 = "▓▓"

_RESET = "\x1b[0m"
_ENTRY_COLOR = "\x1b[32m"
_EXIT_COLOR = "\x1b[31m"


def _colorize(text: str, code: str, enabled: bool) -> str:
    """Wrap text in an ANSI color sequence when coloring is enabled.

    Args:
        text: The text to colorize.
        code: ANSI escape code to apply.
        enabled: Whether coloring should be used.

    Returns:
        The original text if coloring is disabled, otherwise the wrapped text.
    """
    if not enabled or not code:
        return text
    return f"{code}{text}{_RESET}"


def render_maze(
    grid: List[List[int]],
    width: int,
    height: int,
    entry: Tuple[int, int],
    exit_pos: Tuple[int, int],
    path: Optional[List[str]] = None,
    cells_42: Optional[Set[Tuple[int, int]]] = None,
    show_path: bool = True,
    color: bool = False,
    color_42: bool = False,
    wall_palette: Optional[Dict[str, str]] = None,
    palette_42: Optional[Dict[str, str]] = None,
) -> str:
    """Render the maze as a multiline string.

    The renderer draws the maze walls, the entry and exit cells, the shortest
    path if requested, and the optional 42 pattern. It can also apply ANSI
    colors to normal maze elements and to the 42 pattern.

    Args:
        grid: Maze grid represented as wall bitmasks.
        width: Maze width in cells.
        height: Maze height in cells.
        entry: Entry cell coordinates (x, y).
        exit_pos: Exit cell coordinates (x, y).
        path: Shortest path as a list of direction letters.
        cells_42: Cells that belong to the 42 pattern.
        show_path: Whether to display the shortest path.
        color: Whether to color normal maze elements.
        color_42: Whether to color the 42 pattern.
        wall_palette: ANSI palette for normal maze elements.
        palette_42: ANSI palette for the 42 pattern.

    Returns:
        A string containing the full rendered maze.
    """
    if cells_42 is None:
        cells_42 = set()

    if wall_palette is None:
        wall_palette = {
            "wall": "",
            "path": "",
        }
    if palette_42 is None:
        palette_42 = {
            "cell42": "",
        }

    path_cells: Set[Tuple[int, int]] = set()
    if show_path and path:
        delta: Dict[str, Tuple[int, int]] = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0),
        }
        cx, cy = entry
        path_cells.add((cx, cy))
        for step in path:
            dx, dy = delta[step]
            cx += dx
            cy += dy
            path_cells.add((cx, cy))

    lines: List[str] = []

    top = _WALL * (2 * width + 1)
    lines.append(_colorize(top, wall_palette.get("wall", ""), color))

    for y in range(height):
        mid: List[str] = [
            _colorize(_WALL, wall_palette.get("wall", ""), color)
        ]
        for x in range(width):
            cell = grid[y][x]

            if (x, y) == entry:
                char = f"{_ENTRY_COLOR}{_ENTRY}{_RESET}"
            elif (x, y) == exit_pos:
                char = f"{_EXIT_COLOR}{_EXIT}{_RESET}"
            elif (x, y) in cells_42:
                if color_42:
                    char = _colorize(
                        _CELL_42, palette_42.get("cell42", ""), True
                    )
                else:
                    char = _CELL_42
            elif (x, y) in path_cells:
                char = _colorize(_PATH, wall_palette.get("path", ""), color)
            else:
                char = _EMPTY

            mid.append(char)
            mid.append(
                _colorize(_WALL, wall_palette.get("wall", ""), color)
                if (cell & EAST)
                else _EMPTY
            )

        lines.append("".join(mid))

        bot: List[str] = [
            _colorize(_WALL, wall_palette.get("wall", ""), color)
        ]
        for x in range(width):
            cell = grid[y][x]
            bot.append(
                _colorize(_WALL, wall_palette.get("wall", ""), color)
                if (cell & SOUTH)
                else _EMPTY
            )
            bot.append(_colorize(_WALL, wall_palette.get("wall", ""), color))
        lines.append("".join(bot))

    return "\n".join(lines)
