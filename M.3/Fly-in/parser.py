from __future__ import annotations

"""Parser for Fly-in map files.

This module exposes `Parser` which reads a map file and produces a
`Graph` and drone count. It validates syntax and metadata fields and raises
`ParserError` for malformed input.
"""

from typing import Optional

from errors import ParserError
from models import Connection, Graph, Zone


def _edge_key(zone_a: str, zone_b: str) -> tuple[str, str]:
    """Return a normalized undirected edge key.

    The returned tuple is ordered so that keys can be compared/hashed
    independent of direction.
    """
    if zone_a <= zone_b:
        return zone_a, zone_b
    return zone_b, zone_a


class Parser:
    """Parses Fly-in map files into graph models.

    Use `parse(path)` to obtain `(nb_drones, graph)`.
    """

    def _split_metadata(
        self,
        text: str,
        line_number: int,
        kind: str,
    ) -> tuple[str, str]:
        """Split a definition line into main part and metadata block.

        This helper separates the part before the first '[' from the token
        content inside the single metadata block. It validates that at most
        one metadata block exists and that no trailing text follows it.

        Args:
            text: The full right-hand text of a definition line.
            line_number: Source line number used for error reporting.
            kind: Human readable kind string used in error messages
                (e.g. "zone" or "connection").

        Returns:
            A tuple of `(main_part, metadata)` where `metadata` may be an
            empty string when no metadata block is present.
        """
        if "[" not in text and "]" not in text:
            return text.strip(), ""

        if text.count("[") != 1 or text.count("]") != 1:
            raise ParserError(
                f"Line {line_number}: Invalid {kind} metadata block syntax"
            )

        open_index = text.find("[")
        close_index = text.find("]")

        if open_index > close_index:
            raise ParserError(
                f"Line {line_number}: Invalid {kind} metadata block syntax"
            )

        trailing = text[close_index + 1:].strip()
        if trailing:
            raise ParserError(
                f"Line {line_number}: Invalid {kind} metadata trailing text"
            )

        main_part = text[:open_index].strip()
        metadata = text[open_index + 1:close_index].strip()
        return main_part, metadata

    def parse(self, path: str) -> tuple[int, Graph]:
        """
        Parse the map file.

        Args:
            path: Path to the map file.

        Returns:
            Number of drones and parsed graph.

        Example:
            parser = Parser()
            nb, graph = parser.parse("maps/easy/01_linear_path.txt")
        """
        graph = Graph()
        nb_drones: Optional[int] = None
        start_zone_name: Optional[str] = None
        end_zone_name: Optional[str] = None
        seen_zone_names: set[str] = set()
        seen_connections: set[tuple[str, str]] = set()
        first_content_line_seen = False

        try:
            with open(path, "r", encoding="utf-8") as file:
                for line_number, raw_line in enumerate(file, start=1):
                    line = raw_line.strip()

                    if not line or line.startswith("#"):
                        continue

                    if not first_content_line_seen:
                        first_content_line_seen = True
                        if not line.startswith("nb_drones:"):
                            raise ParserError(
                                f"Line {line_number}: The first meaningful "
                                f"line must be nb_drones:"
                            )

                    if line.startswith("nb_drones:"):
                        if nb_drones is not None:
                            raise ParserError(
                                f"Line {line_number}: Duplicate "
                                f"nb_drones definition"
                            )
                        nb_drones = self._parse_nb_drones(line, line_number)

                    elif line.startswith("start_hub:"):
                        if start_zone_name is not None:
                            raise ParserError(
                                f"Line {line_number}: Duplicate "
                                f"start_hub definition"
                            )
                        zone = self._parse_zone(
                            line,
                            line_number,
                            is_start=True,
                        )
                        self._register_zone(
                            zone,
                            graph,
                            seen_zone_names,
                            line_number,
                        )
                        start_zone_name = zone.name

                    elif line.startswith("end_hub:"):
                        if end_zone_name is not None:
                            raise ParserError(
                                f"Line {line_number}: Duplicate "
                                f"end_hub definition"
                            )
                        zone = self._parse_zone(
                            line,
                            line_number,
                            is_end=True,
                        )
                        self._register_zone(
                            zone,
                            graph,
                            seen_zone_names,
                            line_number,
                        )
                        end_zone_name = zone.name

                    elif line.startswith("hub:"):
                        zone = self._parse_zone(line, line_number)
                        self._register_zone(
                            zone,
                            graph,
                            seen_zone_names,
                            line_number,
                        )

                    elif line.startswith("connection:"):
                        connection = self._parse_connection(line, line_number)
                        self._register_connection(
                            connection,
                            graph,
                            seen_connections,
                            seen_zone_names,
                            line_number,
                        )

                    else:
                        raise ParserError(
                            f"Line {line_number}: Unknown statement: {line}"
                        )
        except OSError as error:
            raise ParserError(f"Cannot read file: {error}") from error

        if nb_drones is None:
            raise ParserError("Missing nb_drones definition")
        if start_zone_name is None:
            raise ParserError("Missing start_hub definition")
        if end_zone_name is None:
            raise ParserError("Missing end_hub definition")

        return nb_drones, graph

    def _register_zone(
        self,
        zone: Zone,
        graph: Graph,
        seen_zone_names: set[str],
        line_number: int,
    ) -> None:
        """Register a parsed `Zone` into the graph.

        This validates the zone name is not duplicated and inserts the zone
        into the graph structures.

        Args:
            zone: Parsed `Zone` instance to register.
            graph: `Graph` being populated.
            seen_zone_names: Mutable set tracking seen zone names.
            line_number: Line number used when raising `ParserError`.
        """
        if zone.name in seen_zone_names:
            raise ParserError(
                f"Line {line_number}:"
                f" Duplicate zone name: {zone.name}"
            )
        seen_zone_names.add(zone.name)
        graph.add_zone(zone)

    def _register_connection(
        self,
        connection: Connection,
        graph: Graph,
        seen_connections: set[tuple[str, str]],
        seen_zone_names: set[str],
        line_number: int,
    ) -> None:
        """Validate and register a `Connection` into the graph.

        Checks that both endpoint zone names were previously declared and
        that the undirected edge is not duplicated. On validation failures a
        `ParserError` is raised referencing `line_number`.

        Args:
            connection: Parsed `Connection` instance.
            graph: `Graph` being populated.
            seen_connections: Mutable set of edge keys already added.
            seen_zone_names: Set of zone names that have been declared.
            line_number: Source line number for error messages.
        """
        if connection.zone_a not in seen_zone_names:
            raise ParserError(
                f"Line {line_number}: Unknown zone in connection: "
                f"{connection.zone_a}"
            )
        if connection.zone_b not in seen_zone_names:
            raise ParserError(
                f"Line {line_number}: Unknown zone in connection: "
                f"{connection.zone_b}"
            )

        key = _edge_key(connection.zone_a, connection.zone_b)
        if key in seen_connections:
            raise ParserError(
                f"Line {line_number}: Duplicate connection: "
                f"{connection.zone_a}-{connection.zone_b}"
            )

        seen_connections.add(key)
        graph.add_connection(connection)

    def _parse_nb_drones(self, line: str, line_number: int) -> int:
        """Parse the `nb_drones:` declaration and return the integer value.

        The function validates that the value is a positive integer and
        raises `ParserError` with an informative message when validation
        fails.

        Args:
            line: The full source line beginning with `nb_drones:`.
            line_number: Source line number for error messages.

        Returns:
            Parsed positive integer number of drones.
        """
        _, value = line.split(":", 1)
        value = value.strip()

        if not value.isdigit():
            raise ParserError(
                f"Line {line_number}: nb_drones must be a positive integer"
            )

        nb_drones = int(value)
        if nb_drones <= 0:
            raise ParserError(
                f"Line {line_number}: nb_drones must be greater than zero"
            )
        return nb_drones

    def _parse_zone(
        self,
        line: str,
        line_number: int,
        is_start: bool = False,
        is_end: bool = False,
    ) -> Zone:
        """Parse a single `hub:`/`start_hub:`/`end_hub:` zone definition.

        The expected syntax is: `hub: NAME X Y [metadata]` where NAME is a
        single token and X/Y are integer coordinates. Optional metadata is
        parsed and returned in the `Zone` instance.

        Args:
            line: Full source line containing the zone definition.
            line_number: Source line number for error messages.
            is_start: Whether this zone is the start hub.
            is_end: Whether this zone is the end hub.

        Returns:
            A `Zone` instance populated with parsed values.
        """
        _, rest = line.split(":", 1)
        rest = rest.strip()

        rest, metadata = self._split_metadata(rest, line_number, "zone")

        parts = rest.split()
        if len(parts) != 3:
            raise ParserError(f"Line {line_number}: Invalid zone definition")

        name = parts[0]
        x_str = parts[1]
        y_str = parts[2]

        if "-" in name or " " in name:
            raise ParserError(
                f"Line {line_number}:"
                f" Zone names cannot contain dashes or spaces"
            )

        try:
            x = int(x_str)
            y = int(y_str)
        except ValueError as error:
            raise ParserError(
                f"Line {line_number}: Zone coordinates must be integers"
            ) from error

        zone_type = "normal"
        color: Optional[str] = None
        max_drones = 1

        if metadata:
            zone_type, color, max_drones = self._parse_zone_metadata(
                metadata,
                line_number,
            )

        return Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=color,
            max_drones=max_drones,
            is_start=is_start,
            is_end=is_end,
        )

    def _parse_zone_metadata(
        self,
        metadata: str,
        line_number: int,
    ) -> tuple[str, Optional[str], int]:
        """Parse the content of a zone metadata block.

        Supported metadata keys are `zone`, `color` and `max_drones`. Values
        are validated; invalid keys or values raise `ParserError`.

        Args:
            metadata: The inner text from the metadata block.
            line_number: Source line number for error messages.

        Returns:
            A tuple of `(zone_type, color, max_drones)` extracted from
            the metadata. `color` may be `None` when not present.
        """
        zone_type = "normal"
        color: Optional[str] = None
        max_drones = 1

        for item in metadata.split():
            if "=" not in item:
                raise ParserError(
                    f"Line {line_number}: Invalid metadata item: {item}"
                )

            key, value = item.split("=", 1)

            if key == "zone":
                if value not in {
                    "normal",
                    "blocked",
                    "restricted",
                    "priority",
                }:
                    raise ParserError(
                        f"Line {line_number}: Invalid zone type: {value}"
                    )
                zone_type = value

            elif key == "color":
                color = value

            elif key == "max_drones":
                if not value.isdigit() or int(value) <= 0:
                    raise ParserError(
                        f"Line {line_number}:"
                        f" max_drones must be a positive integer"
                    )
                max_drones = int(value)

            else:
                raise ParserError(
                    f"Line {line_number}: Unknown zone metadata key: {key}"
                )

        return zone_type, color, max_drones

    def _parse_connection(self, line: str, line_number: int) -> Connection:
        """Parse a single `connection:` definition and optional metadata.

        Syntax: `connection: A - B [max_link_capacity=2]` where the metadata
        currently supports `max_link_capacity`.

        Args:
            line: Full source line starting with `connection:`.
            line_number: Source line number for error messages.

        Returns:
            A `Connection` instance with parsed endpoints and capacity.
        """
        _, rest = line.split(":", 1)
        rest = rest.strip()

        rest, metadata = self._split_metadata(
            rest,
            line_number,
            "connection",
        )

        parts = rest.split("-")
        if len(parts) != 2:
            raise ParserError(
                f"Line {line_number}: Invalid connection definition"
            )

        zone_a = parts[0].strip()
        zone_b = parts[1].strip()

        if not zone_a or not zone_b:
            raise ParserError(
                f"Line {line_number}: Invalid connection endpoints"
            )

        max_link_capacity = 1
        if metadata:
            max_link_capacity = self._parse_connection_metadata(
                metadata,
                line_number,
            )

        return Connection(
            zone_a=zone_a,
            zone_b=zone_b,
            max_link_capacity=max_link_capacity,
        )

    def _parse_connection_metadata(
        self,
        metadata: str,
        line_number: int,
    ) -> int:
        """Parse metadata for a connection and return the integer
        `max_link_capacity`.

        Only `max_link_capacity` is accepted and it must be a positive
        integer.

        Args:
            metadata: Inner metadata text.
            line_number: Source line number for error messages.

        Returns:
            Parsed `max_link_capacity` as an int.
        """
        max_link_capacity = 1

        for item in metadata.split():
            if "=" not in item:
                raise ParserError(
                    f"Line {line_number}: Invalid metadata item: {item}"
                )
            key, value = item.split("=", 1)

            if key != "max_link_capacity":
                raise ParserError(
                    f"Line {line_number}:"
                    f" Unknown connection metadata key: {key}"
                )

            if not value.isdigit() or int(value) <= 0:
                raise ParserError(
                    f"Line {line_number}: max_link_capacity must be "
                    f"a positive integer"
                )

            max_link_capacity = int(value)

        return max_link_capacity
