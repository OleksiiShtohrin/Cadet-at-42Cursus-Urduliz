#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age_days: int,
                 growth: float) -> None:
        self.name = name
        self.height = height
        self.age_days = age_days
        self.growth = growth

    def grow(self) -> None:
        self.height += self.growth

    def age(self, days: int = 1) -> None:
        self.age_days += days

    def show(self) -> str:
        return f"{self.name}: {self.height:.1f}cm, {self.age_days} days old"


def main() -> None:
    plant = Plant("Rose", 25.0, 30, 0.8)
    start_height = plant.height

    print("=== Garden Plant Growth ===")

    for day in range(1, 8):
        print(f"=== Day {day} ===")
        print(plant.show())

        if day != 7:
            plant.grow()
            plant.age(1)

    growth = round(plant.height - start_height)
    print(f"Growth this week: {growth}cm")


if __name__ == "__main__":
    main()
