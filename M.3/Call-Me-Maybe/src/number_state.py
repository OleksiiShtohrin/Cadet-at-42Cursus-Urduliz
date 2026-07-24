"""NumberState Enum module.

Represents all logical lexical states during the token-by-token generation of
a JSON number.
"""

from enum import Enum, auto


class NumberState(Enum):
    """States of the JSON number parser."""

    START = auto()
    """Initial state expecting a sign or a digit."""

    SIGN = auto()
    """State after consuming a minus sign, expecting a digit."""

    INTEGER = auto()
    """State after consuming integer digits, expecting more digits or a dot."""

    DOT = auto()
    """State after consuming a dot, expecting fraction digits."""

    FRACTION = auto()
    """State after consuming fraction digits, expecting more digits."""
