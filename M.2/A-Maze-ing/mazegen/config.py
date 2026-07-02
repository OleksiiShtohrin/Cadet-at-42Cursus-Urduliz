"""Configuration parser for the A-Maze-ing project.

This module provides:
- parse_config(): read raw KEY=VALUE pairs from a config file;
- load_config(): validate the config and return a typed Config object.

It is used by the main application to load maze parameters safely and
to report user-friendly errors for invalid configuration files.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple


def parse_config(filename: str) -> Dict[str, str]:
    """Parse a plain-text KEY=VALUE configuration file.

    The parser ignores empty lines and comment lines starting with '#'.
    Each non-empty line must contain exactly one config entry in the form
    KEY=VALUE. Duplicate keys, missing separators, and empty keys/values
    are rejected as invalid input.

    Args:
        filename: Path to the configuration file.

    Returns:
        A dictionary mapping configuration keys to string values.

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If the file cannot be read.
        ValueError: If a line has invalid syntax or a key is duplicated.
    """
    config: Dict[str, str] = {}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError(f"Invalid config line: {line}")

                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()

                if not key or not value:
                    raise ValueError(f"Invalid config line: {line}")

                if key in config:
                    raise ValueError(f"Duplicate config key: {key}")

                config[key] = value
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Configuration file '{filename}' not found."
        ) from exc
    except OSError as exc:
        raise OSError(f"Error reading configuration file: {exc}") from exc

    return config


@dataclass
class Config:
    """Validated configuration used by the maze generator.

    This object stores all parsed and checked settings from the config file
    in a typed form, so the rest of the project can use them without
    re-parsing raw strings.
    """
    width: int
    height: int
    entry: Tuple[int, int]
    exit_pos: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int]
    display_color: bool
    algorithm: str
    animate: bool
    animation_delay: float


def _parse_bool(raw: str) -> bool:
    """Convert a string representation of a boolean into a Python bool.

    Accepted true values include: true, 1, yes, y, t.
    Accepted false values include: false, 0, no, n, f.

    Args:
        raw: Raw string value from the config file.

    Returns:
        True or False depending on the parsed value.

    Raises:
        ValueError: If the value is not a recognized boolean string.
    """
    value = raw.strip().lower()
    if value in ("true", "1", "yes", "y", "t"):
        return True
    if value in ("false", "0", "no", "n", "f"):
        return False
    raise ValueError(f"Invalid boolean value: {raw}")


def _parse_coords(raw: str, label: str) -> Tuple[int, int]:
    """Parse coordinates from a string in the form 'x,y'.

    Args:
        raw: Raw coordinate string from the config file.
        label: Human-readable name used in error messages.

    Returns:
        A tuple (x, y) with integer coordinates.

    Raises:
        ValueError: If the value cannot be parsed as two integers.
    """
    try:
        x_str, y_str = raw.split(",", 1)
        x = int(x_str.strip())
        y = int(y_str.strip())
    except Exception as exc:
        raise ValueError(f"Invalid {label} coordinates") from exc

    return x, y


def load_config(filename: str) -> Config:
    """Load, validate, and normalize the maze configuration.

    This function reads the raw config file, checks that all required keys
    are present, validates types and ranges, and returns a typed Config
    instance ready to be used by the application.

    The following required keys must exist:
    WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT

    Optional keys such as SEED, DISPLAY_COLOR, ALGORITHM, ANIMATE, and
    ANIMATION_DELAY are supported when present.

    Args:
        filename: Path to the configuration file.

    Returns:
        A validated Config object.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        OSError: If the file cannot be read.
        ValueError: If the configuration is missing, malformed, or invalid.
    """
    raw = parse_config(filename)

    required = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }
    allowed = required | {
        "SEED",
        "DISPLAY_COLOR",
        "ALGORITHM",
        "ANIMATE",
        "ANIMATION_DELAY",
    }

    for key in raw:
        if key not in allowed:
            raise ValueError(f"Unknown config key: {key}")

    for key in required:
        if key not in raw:
            raise ValueError(f"Missing required config key: {key}")

    # WIDTH / HEIGHT
    try:
        width = int(raw["WIDTH"])
        height = int(raw["HEIGHT"])
    except Exception as exc:
        raise ValueError("WIDTH and HEIGHT must be integers") from exc

    if width < 1 or height < 1:
        raise ValueError("WIDTH and HEIGHT must be positive integers")

    # ENTRY / EXIT
    entry = _parse_coords(raw["ENTRY"], "ENTRY")
    exit_pos = _parse_coords(raw["EXIT"], "EXIT")

    # OUTPUT_FILE
    output_file = raw["OUTPUT_FILE"]

    # PERFECT
    perfect = _parse_bool(raw["PERFECT"])

    # ALGORITHM (optional, default DFS)
    algorithm = raw.get("ALGORITHM", "DFS").strip().upper()
    if not algorithm:
        algorithm = "DFS"
    if algorithm not in ("DFS", "PRIM"):
        raise ValueError("ALGORITHM must be DFS or PRIM")

    # SEED (optional)
    seed: Optional[int] = None
    if "SEED" in raw:
        seed_raw = raw["SEED"].strip()
        if seed_raw:
            try:
                seed = int(seed_raw)
            except Exception as exc:
                raise ValueError("SEED must be an integer") from exc

    # DISPLAY_COLOR (optional, default False)
    display_color = False
    if "DISPLAY_COLOR" in raw:
        display_color = _parse_bool(raw["DISPLAY_COLOR"])

    # ANIMATE (optional, default False)
    animate = False
    if "ANIMATE" in raw:
        animate = _parse_bool(raw["ANIMATE"])

    # ANIMATION_DELAY (optional, default 0.03)
    animation_delay = 0.03
    if "ANIMATION_DELAY" in raw:
        try:
            animation_delay = float(raw["ANIMATION_DELAY"].strip())
        except Exception as exc:
            raise ValueError("ANIMATION_DELAY must be a number") from exc
        if animation_delay < 0:
            raise ValueError("ANIMATION_DELAY must be non-negative")

    # Basic coordinate bounds check (entry/exit inside maze)
    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        raise ValueError("ENTRY coordinates are out of bounds")
    if not (0 <= exit_pos[0] < width and 0 <= exit_pos[1] < height):
        raise ValueError("EXIT coordinates are out of bounds")
    if entry == exit_pos:
        raise ValueError("ENTRY and EXIT must be different cells")

    return Config(
        width=width,
        height=height,
        entry=entry,
        exit_pos=exit_pos,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
        display_color=display_color,
        algorithm=algorithm,
        animate=animate,
        animation_delay=animation_delay,
    )


__all__ = ["parse_config", "load_config", "Config"]
