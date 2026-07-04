#!/usr/bin/env python3

class SecurePlant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self._height: float = height
        self._age: int = age

    def set_height(self, height: float) -> None:
        if height < 0:
            print(f"{self.name}: Error, height can't be negative")
            print("Height update rejected")
            return
        self._height = height
        print(f"Height updated: {round(self._height)}cm")

    def set_age(self, age: int) -> None:
        if age < 0:
            print(f"{self.name}: Error, age can't be negative")
            print("Age update rejected")
            return
        self._age = age
        print(f"Age updated: {self._age} days")

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age

    def show(self) -> str:
        return f"{self.name}: {self._height:.1f}cm, {self._age} days old"


def main() -> None:
    print("=== Garden Security System ===")

    plant = SecurePlant("Rose", 15.0, -10)
    print(f"Plant created: {plant.show()}")
    print()

    plant.set_height(25)
    plant.set_age(30)
    print()

    plant.set_height(-5)
    plant.set_age(-3)
    print()
    print(f"Current state: {plant.show()}")


if __name__ == "__main__":
    main()
