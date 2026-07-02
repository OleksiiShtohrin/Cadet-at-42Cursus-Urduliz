"""Maze generator module.

This module implements the MazeGenerator class, which can generate random
mazes using DFS or Prim's algorithm, optionally place a centered 42 pattern,
solve the maze, and expose the resulting grid and shortest path.

The class is designed to be reusable from other projects via the mazegen
package.
"""

from __future__ import annotations

import random
from typing import Callable, List, Optional, Set, Tuple

from .patterns import (
    EAST,
    NORTH,
    PATTERN_HEIGHT,
    PATTERN_WIDTH,
    SOUTH,
    WEST,
    build_42_pattern,
    can_place_42,
)
from .solver import solve

MAX_REGENERATION_ATTEMPTS: int = 200


class MazeGenerator:
    """Generate a random maze and compute its shortest solution path.

    The generator supports multiple algorithms, reproducible randomness
    through a seed, optional non-perfect mazes, and a centered 42 pattern
    made of fully closed cells.

    The generated structure is stored in memory and can be accessed through
    properties such as grid, path, and cells_42.
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
        entry: Tuple[int, int] = (0, 0),
        exit_pos: Optional[Tuple[int, int]] = None,
        perfect: bool = True,
        include_42: bool = True,
        algorithm: str = "DFS",
        on_step: Optional[Callable[[List[List[int]]], None]] = None,
    ) -> None:
        if width < 1 or height < 1:
            raise ValueError("Maze dimensions must be at least 1x1.")

        ex, ey = entry
        if not (0 <= ex < width and 0 <= ey < height):
            raise ValueError(f"Entry {entry} is outside the maze bounds.")

        default_exit: Tuple[int, int] = (width - 1, height - 1)
        ep = exit_pos if exit_pos is not None else default_exit
        px, py = ep
        if not (0 <= px < width and 0 <= py < height):
            raise ValueError(f"Exit {ep} is outside the maze bounds.")

        if entry == ep:
            raise ValueError("Entry and exit must be different cells.")

        self.width: int = width
        self.height: int = height
        self.seed: Optional[int] = seed
        self.entry: Tuple[int, int] = entry
        self.exit_pos: Tuple[int, int] = ep
        self.perfect: bool = perfect
        self.include_42: bool = include_42
        self.algorithm: str = algorithm.upper()
        self.on_step = on_step

        self._grid: List[List[int]] = []
        self._path: Optional[List[str]] = None
        self._cells_42: Set[Tuple[int, int]] = set()
        self.used_seed: Optional[int] = None
        self.skipped_42: bool = False

    @property
    def grid(self) -> List[List[int]]:
        """Return the generated maze grid as a 2D list of wall bitmasks."""
        return self._grid

    @property
    def path(self) -> Optional[List[str]]:
        """Return the shortest path from entry to exit as a list of moves."""
        return self._path

    @property
    def cells_42(self) -> Set[Tuple[int, int]]:
        """Return the set of cell coordinates occupied by the 42 pattern."""
        return self._cells_42

    def generate(self) -> None:
        """Generate a valid maze.

        The method performs one or more generation attempts until it produces
        a maze that satisfies the project constraints: solvable, coherent,
        and free of forbidden large open areas. If the 42 pattern is enabled
        and fits, it is placed in the center of the maze.

        The result is stored in the object itself and can be accessed later
        through grid, path, and cells_42.

        Returns:
            None. The generated data is stored on the instance.

        Raises:
            RuntimeError: If no valid maze can be produced after all attempts.
        """
        base_seed = self.seed

        for attempt in range(MAX_REGENERATION_ATTEMPTS):
            if base_seed is not None:
                current_seed = base_seed + attempt
            else:
                current_seed = random.randint(0, 2**31 - 1)

            self._generate_once(current_seed)

            # Check for 3x3 open areas
            if self._has_3x3_open_area():
                self._path = None
                continue

            if self._path is not None:
                self.used_seed = current_seed
                return

        saved = self.include_42
        self.include_42 = False
        final_seed = (
            base_seed if base_seed is not None
            else random.randint(0, 2**31 - 1)
        )
        self._generate_once(final_seed)
        self.include_42 = saved
        self.used_seed = final_seed

        if self._path is None:
            raise RuntimeError(
                "Could not generate a solvable maze after "
                f"{MAX_REGENERATION_ATTEMPTS} attempts."
            )

    def _step(self) -> None:
        """Call the optional animation callback after a generation step."""
        if self.on_step is not None:
            self.on_step(self._grid)

    def _generate_once(self, seed: int) -> None:
        """Run one maze generation attempt using a specific random seed.

        This method initializes the maze grid, places the 42 pattern when
        possible, generates passages using the selected algorithm, optionally
        adds extra passages for non-perfect mazes, applies the final 42
        closure, and computes the shortest path.

        Args:
            seed: Random seed used to make this attempt reproducible.

        Returns:
            None. The maze state is written into the instance fields.

        Raises:
            ValueError: If the algorithm name is invalid or if entry/exit
                overlaps with the 42 pattern.
        """
        self.used_seed = seed
        rng = random.Random(seed)
        self.skipped_42 = False

        self._grid = [
            [NORTH | EAST | SOUTH | WEST for _ in range(self.width)]
            for _ in range(self.height)
        ]

        self._cells_42 = set()
        if self.include_42:
            if can_place_42(self.width, self.height):
                origin_x = (self.width - PATTERN_WIDTH) // 2
                origin_y = (self.height - PATTERN_HEIGHT) // 2
                self._cells_42 = build_42_pattern(origin_x, origin_y)

                if (self.entry in self._cells_42 or
                        self.exit_pos in self._cells_42):
                    raise ValueError(
                        "ENTRY or EXIT overlaps with the 42 pattern."
                    )
            else:
                self.skipped_42 = True

        if self.algorithm == "DFS":
            self._generate_dfs(rng)
        elif self.algorithm == "PRIM":
            self._generate_prim(rng)
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")

        if not self.perfect:
            self._add_extra_passages(rng)

        if self._cells_42:
            self._apply_42_pattern()

        self._path = solve(
            self._grid,
            self.width,
            self.height,
            self.entry,
            self.exit_pos,
        )

    def _is_reserved(self, x: int, y: int) -> bool:
        """Return True if the cell belongs to the 42 pattern."""
        return (x, y) in self._cells_42

    def _generate_dfs(self, rng: random.Random) -> None:
        """Generate the maze using the depth-first search backtracking
        algorithm.

        Starting from the entry cell, the algorithm repeatedly moves to
        a random unvisited neighboring cell, opens the wall between the
        two cells, and continues deeper until it reaches a dead end.
        It then backtracks using a stack until another unvisited
        branch is found.

        Args:
            rng: Random number generator used to choose directions.

        Returns:
            None. The grid is modified in place.
        """
        visited = [[False] * self.width for _ in range(self.height)]
        sx, sy = self.entry
        visited[sy][sx] = True
        stack: List[Tuple[int, int]] = [(sx, sy)]

        moves = [
            (0, -1, NORTH, SOUTH),
            (1, 0, EAST, WEST),
            (0, 1, SOUTH, NORTH),
            (-1, 0, WEST, EAST),
        ]

        while stack:
            x, y = stack[-1]
            candidates = [
                (x + dx, y + dy, wall_from, wall_to)
                for dx, dy, wall_from, wall_to in moves
                if 0 <= x + dx < self.width
                and 0 <= y + dy < self.height
                and not visited[y + dy][x + dx]
                and not self._is_reserved(x + dx, y + dy)
            ]

            if candidates:
                nx, ny, wall_from, wall_to = rng.choice(candidates)
                self._grid[y][x] &= ~wall_from
                self._grid[ny][nx] &= ~wall_to
                visited[ny][nx] = True
                stack.append((nx, ny))
                self._step()
            else:
                stack.pop()

    def _generate_prim(self, rng: random.Random) -> None:
        """Generate the maze using a randomized Prim-like algorithm.

        The algorithm keeps a frontier of candidate cells adjacent to
        the current visited area. It repeatedly selects one frontier cell,
        connects it to one already visited neighbor by removing the wall
        between them, and expands the frontier with new neighboring cells.

        Args:
            rng: Random number generator used to choose
            frontier cells and links.

        Returns:
            None. The grid is modified in place.
        """
        visited = [[False] * self.width for _ in range(self.height)]
        frontier: List[Tuple[int, int]] = []

        sx, sy = self.entry
        visited[sy][sx] = True

        def add_frontier(x: int, y: int) -> None:
            if (
                0 <= x < self.width
                and 0 <= y < self.height
                and not visited[y][x]
                and not self._is_reserved(x, y)
            ):
                if (x, y) not in frontier:
                    frontier.append((x, y))

        add_frontier(sx + 1, sy)
        add_frontier(sx - 1, sy)
        add_frontier(sx, sy + 1)
        add_frontier(sx, sy - 1)

        moves = [
            (0, -1, NORTH, SOUTH),
            (1, 0, EAST, WEST),
            (0, 1, SOUTH, NORTH),
            (-1, 0, WEST, EAST),
        ]

        while frontier:
            idx = rng.randrange(len(frontier))
            x, y = frontier.pop(idx)

            neighbors = []
            for dx, dy, wall_from, wall_to in moves:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < self.width
                    and 0 <= ny < self.height
                    and visited[ny][nx]
                    and not self._is_reserved(x, y)
                ):
                    neighbors.append((nx, ny, wall_from, wall_to))

            if not neighbors:
                continue

            nx, ny, wall_from, wall_to = rng.choice(neighbors)
            self._grid[y][x] &= ~wall_from
            self._grid[ny][nx] &= ~wall_to
            visited[y][x] = True
            self._step()

            add_frontier(x + 1, y)
            add_frontier(x - 1, y)
            add_frontier(x, y + 1)
            add_frontier(x, y - 1)

    def _add_extra_passages(self, rng: random.Random) -> None:
        """Add extra horizontal passages to create loops in
        a non-perfect maze.

        This method removes a limited number of interior east-west walls while
        preserving the reserved 42 cells. It is used only when the maze is not
        required to be perfect.

        Args:
            rng: Random number generator used to pick walls to remove.

        Returns:
            None. The grid is modified in place.
        """
        extra = max(1, (self.width * self.height) // 10)
        for _ in range(extra):
            x = rng.randint(0, self.width - 2)
            y = rng.randint(0, self.height - 1)
            if not self._is_reserved(x, y) and not self._is_reserved(x + 1, y):
                self._grid[y][x] &= ~EAST
                self._grid[y][x + 1] &= ~WEST

    def _apply_42_pattern(self) -> None:
        """Close all walls of the cells that belong to the 42 pattern."""
        all_walls = NORTH | EAST | SOUTH | WEST
        for x, y in self._cells_42:
            self._grid[y][x] = all_walls

    def _has_3x3_open_area(self) -> bool:
        """Return True if the maze contains a forbidden 3x3 open area.

        The project specification allows narrow corridors, but forbids open
        areas wider than 2 cells. This check scans every possible 3x3 block
        and detects whether all internal walls are open.

        Returns:
            True if a forbidden 3x3 open area exists, otherwise False.
        """
        if self.width < 3 or self.height < 3:
            return False

        for y in range(self.height - 2):
            for x in range(self.width - 2):
                ok = True

                # Check horizontal openings inside the 3x3 block
                for dy in range(3):
                    for dx in range(2):
                        if self._grid[y + dy][x + dx] & EAST:
                            ok = False
                            break
                    if not ok:
                        break

                if not ok:
                    continue

                # Check vertical openings inside the 3x3 block
                for dy in range(2):
                    for dx in range(3):
                        if self._grid[y + dy][x + dx] & SOUTH:
                            ok = False
                            break
                    if not ok:
                        break

                if ok:
                    return True

        return False
