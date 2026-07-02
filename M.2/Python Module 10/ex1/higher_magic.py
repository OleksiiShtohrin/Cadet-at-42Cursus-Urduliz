#!/usr/bin/env python3
from collections.abc import Callable


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} damage"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(target: str, power: int) -> tuple[str, str]:
        return spell1(target, power), spell2(target, power)

    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)

    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def conditional(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"

    return conditional


def spell_sequence(spells: list[Callable]) -> Callable:
    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]

    return sequence


def main() -> None:
    combined = spell_combiner(fireball, heal)
    print("Testing spell combiner...")
    result = combined("Dragon", 10)
    print(f"Combined spell result: {result[0]}, {result[1]}")

    mega_fireball = power_amplifier(fireball, 3)
    print("\nTesting power amplifier...")
    print(f"Original: 10, Amplified: {mega_fireball('Dragon', 10)}")

    def strong_enough(target: str, power: int) -> bool:
        return power >= 20 and target != "Wizard"

    conditional_spell = conditional_caster(strong_enough, fireball)
    print("\nTesting conditional caster...")
    print(conditional_spell("Wizard", 25))
    print(conditional_spell("Goblin", 25))

    sequence = spell_sequence([fireball, heal])
    print("\nTesting spell sequence...")
    results = sequence("Knight", 12)
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
