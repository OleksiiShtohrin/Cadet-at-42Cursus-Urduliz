#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age

    def show(self) -> str:
        return f"{self.name}: {self.height}cm, {self.age} days old"


def main() -> None:
    rose = Plant("Rose", 25, 30)
    sunflower = Plant("Sunflower", 80, 45)
    cactus = Plant("Cactus", 15, 120)
    hibisco = Plant("Hibisco", 31, 42)

    print("=== Garden Plant Registry ===")
    print(rose.show())
    print(sunflower.show())
    print(cactus.show())
    print(hibisco.show())


if __name__ == "__main__":
    main()
