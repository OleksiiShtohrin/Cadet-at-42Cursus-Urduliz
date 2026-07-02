# Top-level minimal stub for pygame to satisfy mypy in this repo
from typing import Any

display: Any
time: Any
event: Any
font: Any
mouse: Any
transform: Any
draw: Any

Rect: Any
Surface: Any

QUIT: Any
KEYDOWN: Any
K_ESCAPE: Any
K_q: Any
K_SPACE: Any
K_RIGHT: Any
K_LEFT: Any

def init() -> Any: ...

def quit() -> Any: ...

class ColorError(Exception): ...
