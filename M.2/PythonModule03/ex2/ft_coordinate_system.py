#!/usr/bin/env python3

import math


def split_coordinates(raw: str) -> tuple[str, str, str]:
    first_comma = -1
    second_comma = -1
    comma_count = 0
    i = 0

    for char in raw:
        if char == ",":
            comma_count += 1
            if comma_count == 1:
                first_comma = i
            elif comma_count == 2:
                second_comma = i
        i += 1

    if comma_count != 2:
        raise ValueError("Invalid syntax")

    x_str = raw[:first_comma]
    y_str = raw[first_comma + 1:second_comma]
    z_str = raw[second_comma + 1:]

    if x_str == "" or y_str == "" or z_str == "":
        raise ValueError("Invalid syntax")

    if x_str[0] == " ":
        x_str = x_str[1:]
    if y_str[0] == " ":
        y_str = y_str[1:]
    if z_str[0] == " ":
        z_str = z_str[1:]

    if x_str != "" and x_str[-1] == " ":
        x_str = x_str[:-1]
    if y_str != "" and y_str[-1] == " ":
        y_str = y_str[:-1]
    if z_str != "" and z_str[-1] == " ":
        z_str = z_str[:-1]

    return (x_str, y_str, z_str)


def parse_coordinates(raw: str) -> tuple[float, float, float]:
    x_str, y_str, z_str = split_coordinates(raw)

    try:
        x = float(x_str)
    except ValueError as exc:
        print(f"Error on parameter '{x_str}': {exc}")
        raise

    try:
        y = float(y_str)
    except ValueError as exc:
        print(f"Error on parameter '{y_str}': {exc}")
        raise

    try:
        z = float(z_str)
    except ValueError as exc:
        print(f"Error on parameter '{z_str}': {exc}")
        raise

    return (x, y, z)


def get_player_pos() -> tuple[float, float, float]:
    while True:
        raw = input("Enter new coordinates as floats in format 'x,y,z': ")
        try:
            return parse_coordinates(raw)
        except ValueError as exc:
            if str(exc) == "Invalid syntax":
                print("Invalid syntax")


def distance_3d(
    p1: tuple[float, float, float],
    p2: tuple[float, float, float],
) -> float:
    return math.sqrt(
        (p2[0] - p1[0]) ** 2
        + (p2[1] - p1[1]) ** 2
        + (p2[2] - p1[2]) ** 2
    )


def main() -> None:
    print("=== Game Coordinate System ===")
    print()

    print("Get a first set of coordinates")
    first_pos = get_player_pos()
    print(f"Got a first tuple: {first_pos}")
    print(f"It includes: X={first_pos[0]}, Y={first_pos[1]}, Z={first_pos[2]}")
    print(f"Distance to center: "
          f"{round(distance_3d((0.0, 0.0, 0.0), first_pos), 4)}")
    print()

    print("Get a second set of coordinates")
    second_pos = get_player_pos()
    print("Distance between the 2 sets of coordinates: "
          f"{round(distance_3d(first_pos, second_pos), 4)}")


if __name__ == "__main__":
    main()
