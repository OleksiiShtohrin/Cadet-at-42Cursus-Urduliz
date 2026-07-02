"""Unit tests for the 42 pattern helpers."""

from __future__ import annotations

import pytest

from mazegen.patterns import build_42_pattern, can_place_42


def test_can_place_42_large_enough() -> None:
    """Verify that a large enough maze can contain the 42 pattern."""
    assert can_place_42(20, 15) is True


def test_can_place_42_too_small() -> None:
    """Verify that a too-small maze cannot contain the 42 pattern."""
    assert can_place_42(5, 5) is False


def test_build_42_pattern_not_empty() -> None:
    """Verify that the 42 pattern builder returns a non-empty set of cells."""
    cells = build_42_pattern(0, 0)

    assert len(cells) > 0
    assert all(isinstance(cell, tuple) and len(cell) == 2 for cell in cells)


__all__ = ["pytest"]
