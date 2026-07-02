"""Unit tests for the maze output writer."""

from __future__ import annotations

from pathlib import Path

from mazegen.writer import write_output_file


def test_write_output_file(tmp_path: Path) -> None:
    """Verify that the output file is written in the required format."""
    out_file = tmp_path / "output_maze.txt"

    grid = [
        [0xF, 0xA],
        [0x5, 0x0],
    ]
    entry = (0, 0)
    exit_ = (1, 1)
    shortest_path = ["E", "S"]

    write_output_file(
        path=str(out_file),
        grid=grid,
        entry=entry,
        exit_=exit_,
        shortest_path=shortest_path,
    )

    content = out_file.read_text(encoding="utf-8")
    expected = (
        "FA\n"
        "50\n"
        "\n"
        "0,0\n"
        "1,1\n"
        "ES\n"
    )
    assert content == expected
