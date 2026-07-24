"""Base constraint interface module.

Defines the abstract contract that all schema-guided JSON token constraints
must satisfy during greedy decoding.
"""

from abc import ABC
from abc import abstractmethod


class Constraint(ABC):
    """Base interface for all decoder constraints.

    A constraint decides which tokens may be generated next
    and whether generation of the constrained fragment
    has completed.
    """

    @abstractmethod
    def next_allowed(
        self,
        generated_tokens: list[int],
    ) -> set[int]:
        """Return all tokens currently allowed.

        Args:
            generated_tokens: A list of token IDs generated for this active
                constraint sequence so far.

        Returns:
            A set of allowed token IDs that can legally succeed the currently
            generated fragment.
        """
        ...

    @abstractmethod
    def is_complete(
        self,
        generated_tokens: list[int],
    ) -> bool:
        """Return True when the constraint has been completely generated.

        Args:
            generated_tokens: A list of token IDs generated for this active
                constraint sequence so far.

        Returns:
            True if the constraint is fully satisfied and complete,
            False otherwise.
        """
        ...
