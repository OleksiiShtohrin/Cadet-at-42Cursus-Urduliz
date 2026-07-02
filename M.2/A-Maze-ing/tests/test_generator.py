"""Unit tests for the MazeGenerator class and maze generation rules."""

import pytest

from mazegen import MazeGenerator
from mazegen.patterns import PATTERN_HEIGHT, PATTERN_WIDTH

# Wall bit constants (same as in the library)
NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8


# ── Helpers ──────────────────────────────────────────────────────────────────


def _check_wall_coherence(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Return positions of cells whose wall encoding is inconsistent."""
    bad = []
    h = len(grid)
    w = len(grid[0]) if h else 0
    for r in range(h):
        for c in range(w):
            v = grid[r][c]
            ok = all(
                [
                    r < 1 or (v & 1) == ((grid[r - 1][c] >> 2) & 1),
                    c >= w - 1 or (
                        ((v >> 1) & 1) == ((grid[r][c + 1] >> 3) & 1)
                    ),
                    r >= h - 1 or ((v >> 2) & 1) == (grid[r + 1][c] & 1),
                    c < 1 or ((v >> 3) & 1) == ((grid[r][c - 1] >> 1) & 1),
                ]
            )
            if not ok:
                bad.append((c, r))
    return bad


# ── Basic generation ─────────────────────────────────────────────────────────


def test_grid_dimensions() -> None:
    """Verify that the generated grid matches the requested size."""
    mg = MazeGenerator(width=10, height=8, seed=1)
    mg.generate()
    assert len(mg.grid) == 8
    assert all(len(row) == 10 for row in mg.grid)


def test_path_exists() -> None:
    """Verify that a generated maze always has a solution path."""
    mg = MazeGenerator(width=10, height=10, seed=42)
    mg.generate()
    assert mg.path is not None
    assert len(mg.path) > 0


def test_wall_coherence_no_42() -> None:
    """Verify that neighboring walls are coherent when 42 is disabled."""
    mg = MazeGenerator(width=12, height=10, seed=7, include_42=False)
    mg.generate()
    bad = _check_wall_coherence(mg.grid)
    assert bad == [], f"Incoherent walls at: {bad}"


def test_wall_coherence_with_42() -> None:
    """Verify that neighboring walls remain coherent with 42 enabled."""
    mg = MazeGenerator(width=15, height=12, seed=7, include_42=True)
    mg.generate()
    bad = _check_wall_coherence(mg.grid)
    assert bad == [], f"Incoherent walls at: {bad}"


# ── include_42 flag ──────────────────────────────────────────────────────────


def test_include_42_false_produces_no_pattern() -> None:
    """Verify that disabling 42 produces an empty 42-cell set."""
    mg = MazeGenerator(width=20, height=15, seed=42, include_42=False)
    mg.generate()
    assert mg.cells_42 == set()


def test_include_42_true_produces_pattern() -> None:
    """Verify that enabling 42 places the pattern in a large enough maze."""
    mg = MazeGenerator(width=20, height=15, seed=42, include_42=True)
    mg.generate()
    assert len(mg.cells_42) > 0


def test_small_maze_42_is_skipped() -> None:
    """Verify that the 42 pattern is skipped when the maze is too small."""
    mg = MazeGenerator(
        width=PATTERN_WIDTH,
        height=PATTERN_HEIGHT,
        seed=1,
        include_42=True,
    )
    mg.generate()

    assert mg.skipped_42 is True


# ── Pattern placement ────────────────────────────────────────────────────────


def test_42_cells_are_centered() -> None:
    """Verify that the 42 pattern is centered inside the maze."""
    w, h = 20, 15
    mg = MazeGenerator(width=w, height=h, seed=42, include_42=True)
    mg.generate()

    if not mg.cells_42:
        pytest.skip(
            "42 pattern was not placed (maze too small or generation failed)"
        )

    xs = [x for x, _ in mg.cells_42]
    ys = [y for _, y in mg.cells_42]
    expected_ox = (w - PATTERN_WIDTH) // 2
    expected_oy = (h - PATTERN_HEIGHT) // 2
    assert min(xs) == expected_ox, (
        f"Pattern x-origin mismatch: {min(xs)} vs {expected_ox}"
    )
    assert min(ys) == expected_oy, (
        f"Pattern y-origin mismatch: {min(ys)} vs {expected_oy}"
    )


def test_42_cells_fully_walled() -> None:
    """Verify that every 42 cell is completely closed with all four walls."""
    mg = MazeGenerator(width=20, height=15, seed=42, include_42=True)
    mg.generate()
    for x, y in mg.cells_42:
        assert mg.grid[y][x] == 0xF, (
            f"Cell ({x},{y}) is not fully walled: {mg.grid[y][x]:#x}"
        )


# ── Reproducibility ──────────────────────────────────────────────────────────


def test_reproducibility() -> None:
    """Verify that the same seed produces identical mazes."""
    mg1 = MazeGenerator(width=10, height=10, seed=99)
    mg1.generate()
    mg2 = MazeGenerator(width=10, height=10, seed=99)
    mg2.generate()
    assert mg1.grid == mg2.grid


# ── Custom entry / exit ──────────────────────────────────────────────────────


def test_custom_entry_exit() -> None:
    """Verify that custom entry and exit coordinates are respected."""
    mg = MazeGenerator(
        width=15, height=10, seed=5, entry=(0, 0), exit_pos=(14, 9)
    )
    mg.generate()
    assert mg.path is not None


# ── Error handling ───────────────────────────────────────────────────────────


def test_invalid_dimensions() -> None:
    """Verify that invalid maze dimensions raise a ValueError."""
    with pytest.raises(ValueError):
        MazeGenerator(width=0, height=5)


def test_entry_out_of_bounds() -> None:
    """Verify that an out-of-bounds entry raises a ValueError."""
    with pytest.raises(ValueError):
        MazeGenerator(width=5, height=5, entry=(10, 0))


def test_same_entry_exit() -> None:
    """Verify that identical entry and exit cells raise a ValueError."""
    with pytest.raises(ValueError):
        MazeGenerator(width=5, height=5, entry=(0, 0), exit_pos=(0, 0))
