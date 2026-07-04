#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name: str = name
        self.height: float = height
        self.age: int = age

    def grow(self) -> None:
        self.height += 2.1

    def age_plant(self, days: int = 1) -> None:
        self.age += days

    def show(self) -> str:
        return f"{self.name}: {self.height:.1f}cm, {self.age} days old"


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str) -> None:
        super().__init__(name, height, age)
        self.color: str = color
        self.bloomed = False

    def bloom(self) -> None:
        self.bloomed = True

    def show(self) -> str:
        result = super().show()
        result += f"\n Color: {self.color}"
        if self.bloomed:
            result += f"\n {self.name} is blooming beautifully!"
        else:
            result += f"\n {self.name} has not bloomed yet"
        return result


class Tree(Plant):
    def __init__(self, name: str, height: float, age: int,
                 trunk_diameter: float) -> None:
        super().__init__(name, height, age)
        self.trunk_diameter: float = trunk_diameter

    def produce_shade(self) -> None:
        print(
            f"Tree {self.name} now produces a shade of "
            f"{self.height:.1f}cm long and {self.trunk_diameter:.1f}cm wide."
        )

    def show(self) -> str:
        result = super().show()
        result += f"\n Trunk diameter: {self.trunk_diameter:.1f}cm"
        return result


class Vegetable(Plant):
    def __init__(self, name: str, height: float, age: int,
                 harvest_season: str) -> None:
        super().__init__(name, height, age)
        self.harvest_season: str = harvest_season
        self.nutritional_value = 0

    def grow(self) -> None:
        super().grow()

    def age_plant(self, days: int = 1) -> None:
        super().age_plant(days)
        self.nutritional_value += days

    def show(self) -> str:
        result = super().show()
        result += f"\n Harvest season: {self.harvest_season}"
        result += f"\n Nutritional value: {self.nutritional_value}"
        return result


def main() -> None:
    print("=== Garden Plant Types ===")

    flower = Flower("Rose", 15.0, 10, "red")
    print("=== Flower")
    print(flower.show())
    print("[asking the rose to bloom]")
    flower.bloom()
    print(flower.show())
    print()

    tree = Tree("Oak", 200.0, 365, 5.0)
    print("=== Tree")
    print(tree.show())
    print("[asking the oak to produce shade]")
    tree.produce_shade()
    print()

    vegetable = Vegetable("Tomato", 5.0, 10, "April")
    print("=== Vegetable")
    print(vegetable.show())
    print("[make tomato grow and age for 20 days]")
    for _ in range(20):
        vegetable.grow()
        vegetable.age_plant()
    print(vegetable.show())


if __name__ == "__main__":
    main()
