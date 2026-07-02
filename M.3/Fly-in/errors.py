"""Custom exception types used across the Fly-in project.

This module defines a small hierarchy of exceptions raised by the parser,
planner and simulator to allow callers to cleanly handle known failure
conditions.
"""


class FlyInError(Exception):
    """Base exception for all errors raised by this project.

    Subclass this error for specific failure categories so callers can
    catch broad simulator/parser/planner failures via a single base
    exception type when desired.
    """


class ParserError(FlyInError):
    """Raised when the input map file is invalid.

    This indicates syntax or semantic errors discovered while parsing a
    map file.
    """


class SimulationError(FlyInError):
    """Raised when the simulation cannot continue.

    Examples include deadlocks, unknown zones, or capacity violations.
    """


class PathFinderError(FlyInError):
    """Raised when a route cannot be found or is invalid.

    Indicates failures during path discovery and routing.
    """
