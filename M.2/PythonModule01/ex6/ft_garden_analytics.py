#!/usr/bin/env python3

class Plant:
    class Stats:
        def __init__(self) -> None:
            self.grow_calls = 0
            self.age_calls = 0
            self.show_calls = 0

        def display(self) -> str:
            return (
                f"Stats: {self.grow_calls} grow, "
                f"{self.age_calls} age, "
                f"{self.show_calls} show"
            )

    def __init__(self, name: str, height: float, age: int,
                 growth: float) -> None:
        self.name = name
        self.height = height
        self.age = age
        self.growth = growth
        self._stats = Plant.Stats()

    def grow(self) -> None:
        self.height += self.growth
        self._stats.grow_calls += 1

    def age_plant(self, days: int = 1) -> None:
        self.age += days
        self._stats.age_calls += 1

    def show(self) -> str:
        self._stats.show_calls += 1
        return f"{self.name}: {self.height:.1f}cm, {self.age} days old"

    @staticmethod
    def is_older_than_year(age: int) -> bool:
        return age > 365

    @classmethod
    def create_anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0, 0.0)


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str,
                 growth: float) -> None:
        super().__init__(name, height, age, growth)
        self.color = color
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
                 trunk_diameter: float, growth: float) -> None:
        super().__init__(name, height, age, growth)
        self.trunk_diameter = trunk_diameter
        self.shade_calls = 0

    def produce_shade(self) -> None:
        self.shade_calls += 1
        print(
            f"Tree {self.name} now produces a shade of "
            f"{self.height:.1f}cm long and {self.trunk_diameter:.1f}cm wide."
        )

    def show(self) -> str:
        result = super().show()
        result += f"\n Trunk diameter: {self.trunk_diameter:.1f}cm"
        return result


class Seed(Flower):
    def __init__(self, name: str, height: float, age: int, color: str,
                 growth: float, seeds: int = 0) -> None:
        super().__init__(name, height, age, color, growth)
        self.seeds = seeds

    def bloom(self) -> None:
        super().bloom()
        self.seeds = 42

    def show(self) -> str:
        result = super().show()
        result += f"\n Seeds: {self.seeds}"
        return result


def display_statistics(plant: Plant) -> None:
    print(f"[statistics for {plant.name}]")
    print(plant._stats.display())
    if isinstance(plant, Tree):
        print(f" {plant.shade_calls} shade")


def main() -> None:
    print("=== Garden statistics ===")
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.is_older_than_year(30)}")
    print(f"Is 400 days more than a year? -> {Plant.is_older_than_year(400)}")
    print()

    print("=== Flower")
    flower = Flower("Rose", 15.0, 10, "red", 8.0)
    print(flower.show())
    display_statistics(flower)
    print(f"[asking the {flower.name.lower()} to grow and bloom]")
    flower.grow()
    flower.bloom()
    print(flower.show())
    display_statistics(flower)
    print()

    print("=== Tree")
    tree = Tree("Oak", 200.0, 365, 5.0, 0.0)
    print(tree.show())
    display_statistics(tree)
    print(f"[asking the {tree.name.lower()} to produce shade]")
    tree.produce_shade()
    display_statistics(tree)
    print()

    print("=== Seed")
    seed = Seed("Sunflower", 80.0, 45, "yellow", 30.0)
    print(seed.show())
    print(f"[make {seed.name.lower()} grow, age and bloom]")
    seed.grow()
    seed.age_plant(20)
    seed.bloom()
    print(seed.show())
    display_statistics(seed)
    print()

    print("=== Anonymous")
    anonymous = Plant.create_anonymous()
    print(anonymous.show())
    display_statistics(anonymous)


if __name__ == "__main__":
    main()
