"""Unit tests for the BFS maze solver."""

from mazegen import MazeGenerator
from mazegen.solver import solve

# Wall bit constants
NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8


# ── Helpers ──────────────────────────────────────────────────────────────────


def _follow_path(
    grid: list[list[int]],
    width: int,
    height: int,
    start: tuple[int, int],
    path: list[str],
) -> tuple[int, int]:
    """Follow a path through the maze and return the final coordinates."""
    _dir = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    _wall = {"N": NORTH, "E": EAST, "S": SOUTH, "W": WEST}
    x, y = start
    for d in path:
        dx, dy = _dir[d]
        wall = _wall[d]
        assert not (grid[y][x] & wall), (
            f"Wall blocking move {d} from ({x},{y})"
        )
        x += dx
        y += dy
        assert 0 <= x < width and 0 <= y < height, (
            f"Path went out of bounds at ({x},{y})"
        )
    return x, y


# ── Basic solver tests ───────────────────────────────────────────────────────


def test_solve_returns_path() -> None:
    """Verify that the solver returns a path for a solvable maze."""
    mg = MazeGenerator(width=8, height=8, seed=1, include_42=False)
    mg.generate()
    path = solve(mg.grid, 8, 8, (0, 0), (7, 7))
    assert path is not None


def test_solve_path_correctness() -> None:
    """Verify that the returned path actually reaches the exit cell."""
    w, h = 10, 10
    entry, exit_pos = (0, 0), (9, 9)
    mg = MazeGenerator(width=w, height=h, seed=42, include_42=False)
    mg.generate()
    path = solve(mg.grid, w, h, entry, exit_pos)
    assert path is not None
    final = _follow_path(mg.grid, w, h, entry, path)
    assert final == exit_pos, f"Path ended at {final}, expected {exit_pos}"


def test_solve_same_entry_exit() -> None:
    """Verify that equal entry and exit cells return an empty path."""
    mg = MazeGenerator(width=5, height=5, seed=3, include_42=False)
    mg.generate()
    path = solve(mg.grid, 5, 5, (0, 0), (0, 0))
    assert path == []


def test_solve_no_path_for_isolated_cell() -> None:
    """Verify that the solver returns None when no path exists."""
    # Build a 2×1 maze where both cells have all walls closed
    grid = [[NORTH | EAST | SOUTH | WEST, NORTH | EAST | SOUTH | WEST]]
    path = solve(grid, 2, 1, (0, 0), (1, 0))
    assert path is None


def test_solve_shortest_path() -> None:
    """Verify that BFS returns the shortest possible path."""
    # Manually construct a 3×1 corridor: (0,0)→(1,0)→(2,0)
    # Cell 0: E open,  Cell 1: W and E open,  Cell 2: W open
    all_walls = NORTH | EAST | SOUTH | WEST
    grid = [
        [
            (all_walls & ~EAST),          # (0,0): open East
            (all_walls & ~EAST & ~WEST),  # (1,0): open East and West
            (all_walls & ~WEST),          # (2,0): open West
        ]
    ]
    path = solve(grid, 3, 1, (0, 0), (2, 0))
    assert path == ["E", "E"]


# ── Integration with MazeGenerator ───────────────────────────────────────────


def test_generator_path_matches_solver() -> None:
    """Verify that MazeGenerator stores the same shortest path as solve()."""
    w, h = 12, 10
    entry, exit_pos = (0, 0), (11, 9)
    mg = MazeGenerator(width=w, height=h, seed=77, include_42=False,
                       entry=entry, exit_pos=exit_pos)
    mg.generate()

    direct = solve(mg.grid, w, h, entry, exit_pos)
    assert direct is not None
    assert mg.path is not None
    # Both paths should have the same length (BFS is deterministic)
    assert len(mg.path) == len(direct)


def test_solve_with_42_pattern() -> None:
    """Verify that a valid path still exists when 42 is embedded."""
    w, h = 20, 15
    entry, exit_pos = (0, 0), (19, 14)
    mg = MazeGenerator(width=w, height=h, seed=42, include_42=True,
                       entry=entry, exit_pos=exit_pos)
    mg.generate()
    assert mg.path is not None, "No path found with 42 pattern embedded"
    final = _follow_path(mg.grid, w, h, entry, mg.path)
    assert final == exit_pos
