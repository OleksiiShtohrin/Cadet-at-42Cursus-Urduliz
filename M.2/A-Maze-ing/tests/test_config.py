"""Unit tests for configuration parsing and validation."""

from __future__ import annotations

from pathlib import Path

import pytest

from mazegen.config import load_config


def test_load_config_success(tmp_path: Path) -> None:
    """Verify that a valid configuration file is parsed correctly."""
    config_file = tmp_path / "config.txt"
    config_file.write_text(
        "\n".join(
            [
                "WIDTH=20",
                "HEIGHT=15",
                "ENTRY=0,0",
                "EXIT=19,14",
                "OUTPUT_FILE=output_maze.txt",
                "PERFECT=True",
                "SEED=42",
            ]
        ),
        encoding="utf-8",
    )

    config = load_config(str(config_file))

    assert config.width == 20
    assert config.height == 15
    assert config.entry == (0, 0)
    assert config.exit_pos == (19, 14)
    assert config.output_file == "output_maze.txt"
    assert config.perfect is True
    assert config.seed == 42


def test_load_config_missing_key(tmp_path: Path) -> None:
    """Verify that missing required config keys raise a ValueError."""
    config_file = tmp_path / "bad_config.txt"
    config_file.write_text(
        "\n".join(
            [
                "WIDTH=20",
                "HEIGHT=15",
                "ENTRY=0,0",
                "EXIT=19,14",
                "PERFECT=True",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Missing required config key"):
        load_config(str(config_file))


def test_load_config_invalid_seed(tmp_path: Path) -> None:
    """Verify that a non-integer SEED value raises a ValueError."""
    config_file = tmp_path / "bad_seed.txt"
    config_file.write_text(
        "\n".join(
            [
                "WIDTH=20",
                "HEIGHT=15",
                "ENTRY=0,0",
                "EXIT=19,14",
                "OUTPUT_FILE=output_maze.txt",
                "PERFECT=True",
                "SEED=abc",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="SEED must be an integer"):
        load_config(str(config_file))
