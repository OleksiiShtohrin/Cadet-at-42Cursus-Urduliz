from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, cast

from .errors import InvalidCreatureStrategyError
from ex1.creatures import Creature


@runtime_checkable
class HealProtocol(Protocol):
    def heal(self) -> str:
        ...


@runtime_checkable
class TransformProtocol(Protocol):
    def transform(self) -> str:
        ...

    def revert(self) -> str:
        ...


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        raise NotImplementedError

    @abstractmethod
    def act(self, creature: Creature) -> list[str]:
        raise NotImplementedError


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise InvalidCreatureStrategyError(
                f"Invalid Creature '{creature.name}' for this normal strategy"
            )
        return [creature.attack()]


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealProtocol)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise InvalidCreatureStrategyError(
                f"Invalid Creature '{creature.name}' "
                f"for this defensive strategy"
            )
        healer = cast(HealProtocol, creature)
        return [creature.attack(), healer.heal()]


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformProtocol)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise InvalidCreatureStrategyError(
                f"Invalid Creature '{creature.name}' "
                f"for this aggressive strategy"
            )
        transformer = cast(TransformProtocol, creature)
        return [
            transformer.transform(),
            creature.attack(),
            transformer.revert(),
        ]
