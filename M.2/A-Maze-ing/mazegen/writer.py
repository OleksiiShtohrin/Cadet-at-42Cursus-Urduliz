"""Maze output writer.

This module writes the generated maze to a text file in the format required
by the A-Maze-ing subject. It also exposes a compatibility wrapper expected
by the tests.
"""

from __future__ import annotations

import sys
from typing import List, Optional, Tuple


def write_output(
    filename: str,
    grid: List[List[int]],
    entry: Tuple[int, int],
    exit_pos: Tuple[int, int],
    path: Optional[List[str]],
) -> None:
    """Write the maze to a file using the required hexadecimal format.

    The output contains:
    - one hexadecimal digit per cell, row by row;
    - one empty line;
    - the entry coordinates;
    - the exit coordinates;
    - the shortest path as a string of N/E/S/W letters.

    Args:
        filename: Destination file path.
        grid: Maze grid as wall bitmasks.
        entry: Entry coordinates (x, y).
        exit_pos: Exit coordinates (x, y).
        path: Shortest path as a list of moves, or None if unavailable.

    Raises:
        SystemExit: If the file cannot be written.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for row in grid:
                f.write("".join(format(cell, "X") for cell in row) + "\n")

            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_pos[0]},{exit_pos[1]}\n")

            if path is None:
                f.write("\n")
            else:
                f.write("".join(path) + "\n")
    except OSError as exc:
        print(f"Error writing output file"
              f" '{filename}': {exc}", file=sys.stderr)
        sys.exit(1)


def write_output_file(
    *,
    path: str,
    grid: List[List[int]],
    entry: Tuple[int, int],
    exit_: Tuple[int, int],
    shortest_path: Optional[List[str]] = None,
) -> None:
    """Compatibility wrapper for the output writer.

    This function matches the API expected by the tests and forwards the
    arguments to write_output().

    Args:
        path: Destination file path.
        grid: Maze grid as wall bitmasks.
        entry: Entry coordinates (x, y).
        exit_: Exit coordinates (x, y).
        shortest_path: Shortest path as a list of moves, or None.

    Returns:
        None.
    """
    write_output(path, grid, entry, exit_, shortest_path)


__all__ = ["write_output", "write_output_file"]
