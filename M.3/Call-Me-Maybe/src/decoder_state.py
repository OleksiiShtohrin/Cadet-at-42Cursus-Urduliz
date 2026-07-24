"""Decoder State Enum module.

Represents all logical stages of the modular state-machine based constrained
JSON parser.
"""

from enum import Enum, auto


class DecoderState(Enum):
    """Current state of the constrained JSON parser."""

    START = auto()
    """Initial state expecting the starting open brace."""

    PROMPT_KEY = auto()
    """State expecting the exact literal '"prompt":'."""

    PROMPT_VALUE = auto()
    """State expecting the prompt value string (escaped user prompt)."""

    NAME_KEY = auto()
    """State expecting the exact literal '"name":'."""

    NAME_VALUE = auto()
    """State expecting one of the registered function names."""

    PARAMETERS_KEY = auto()
    """State expecting the exact literal '"parameters":'."""

    PARAMETER = auto()
    """State executing the active schema-guided ParameterConstraint."""

    FINISHED = auto()
    """State verifying final closing JSON structural delimiters."""
