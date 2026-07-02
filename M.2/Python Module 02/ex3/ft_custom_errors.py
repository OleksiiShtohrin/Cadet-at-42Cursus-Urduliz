#!/usr/bin/env python3

class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown water error") -> None:
        super().__init__(message)


def trigger_plant_problem() -> None:
    raise PlantError("The tomato plant is wilting!")


def trigger_water_problem() -> None:
    raise WaterError("Not enough water in the tank!")


def main() -> None:
    print("=== Custom Garden Errors Demo ===")
    print()

    print("Testing PlantError...")
    try:
        trigger_plant_problem()
    except PlantError as exc:
        print(f"Caught PlantError: {exc}")
    print()

    print("Testing WaterError...")
    try:
        trigger_water_problem()
    except WaterError as exc:
        print(f"Caught WaterError: {exc}")
    print()

    print("Testing catching all garden errors...")
    try:
        trigger_plant_problem()
    except GardenError as exc:
        print(f"Caught GardenError: {exc}")

    try:
        trigger_water_problem()
    except GardenError as exc:
        print(f"Caught GardenError: {exc}")

    print()
    print("All custom error types work correctly!")


if __name__ == "__main__":
    main()
