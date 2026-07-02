"""Reusable maze generation package.

This package exposes MazeGenerator as a reusable class for other projects.
It can be installed with pip from the provided wheel or source distribution.

Example:
    from mazegen import MazeGenerator

    maze = MazeGenerator(width=20, height=15, seed=42)
    maze.generate()
    print(maze.grid)
    print(maze.path)
    print(maze.cells_42)

    # 2-D list [y][x] of wall bitmasks (bit0=N, bit1=E, bit2=S, bit3=W)
    grid = mg.grid

    # Shortest path from entry to exit: list of 'N'/'E'/'S'/'W' strings
    path = mg.path

    # Set of (x, y) tuples for the '42' pattern cells (all walls closed)
    cells_42 = mg.cells_42

Custom parameters::

    mg = MazeGenerator(
        width=30, height=20,
        seed=7,
        entry=(0, 0),
        exit_pos=(29, 19),
        perfect=True,       # unique path between every pair of cells
        include_42=True,    # embed the visible '42' pattern
    )
    mg.generate()
"""

from .generator import MazeGenerator

__all__ = ["MazeGenerator"]
__version__ = "1.0.0"
