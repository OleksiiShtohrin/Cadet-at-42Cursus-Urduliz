#!/usr/bin/env python3
from __future__ import annotations

from collections.abc import Callable
from functools import lru_cache, partial, reduce, singledispatch
import operator
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0

    operations: dict[str, Callable[[int, int], int]] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min,
    }

    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")

    func: Callable[[int, int], int] = operations[operation]
    return reduce(func, spells)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    fire_enchantment = partial(base_enchantment, 50, "fire")
    ice_enchantment = partial(base_enchantment, 50, "ice")
    wind_enchantment = partial(base_enchantment, 50, "wind")

    return {
        "fire": fire_enchantment,
        "ice": ice_enchantment,
        "wind": wind_enchantment,
    }


def base_enchantment(power: int, element: str, target: str) -> str:
    return f"{element.capitalize()} enchantment on {target} with power {power}"


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @singledispatch
    def dispatch(value: Any) -> str:
        return "Unknown spell type"

    @dispatch.register
    def _(value: int) -> str:
        return f"Damage spell: {value} damage"

    @dispatch.register
    def _(value: str) -> str:
        return f"Enchantment: {value}"

    @dispatch.register
    def _(value: list) -> str:
        return f"Multi-cast: {len(value)} spells"

    return dispatch


def main() -> None:
    print("Testing spell reducer...")
    spell_powers = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(spell_powers, 'add')}")
    print(f"Product: {spell_reducer(spell_powers, 'multiply')}")
    print(f"Max: {spell_reducer(spell_powers, 'max')}")
    print(f"Min: {spell_reducer(spell_powers, 'min')}")

    enchanted_spells = partial_enchanter(base_enchantment)

    print("\nTesting partial enchanter...")
    print(enchanted_spells["fire"]("Dragon"))
    print(enchanted_spells["ice"]("Goblin"))
    print(enchanted_spells["wind"]("Wizard"))

    print("\nTesting memoized fibonacci...")
    print(f"Fib(0): {memoized_fibonacci(0)}")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")

    print("\nTesting spell dispatcher...")
    dispatcher = spell_dispatcher()
    print(dispatcher(42))
    print(dispatcher("fireball"))
    print(dispatcher([1, 2, 3]))
    print(dispatcher({"unknown": True}))


if __name__ == "__main__":
    main()
