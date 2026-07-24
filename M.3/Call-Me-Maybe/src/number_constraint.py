"""NumberConstraint module.

Handles token-by-token generation of syntactically correct JSON numbers or
integers.
"""

from src.constraint import Constraint
from src.llm import LLM
from src.number_state import NumberState


class NumberConstraint(Constraint):
    """Restricts generation of JSON numbers
    using cached single digit token IDs.
    """

    def __init__(self, model: LLM, is_integer: bool = False) -> None:
        """Cache standard digit and sign token IDs dynamically.

        Args:
            model: The LLM wrapper instance.
            is_integer: If True, restricts generation to integers only
                (no decimals).
        """
        self._digits: set[int] = {
            model.encode_single_token(str(i))
            for i in range(10)
        }
        self._minus: int = model.encode_single_token("-")
        self._dot: int = model.encode_single_token(".")
        self._is_integer: bool = is_integer

    def next_allowed(self, generated: list[int]) -> set[int]:
        """Return allowed tokens based on current parse state.

        Args:
            generated: A list of token IDs generated for this number so far.

        Returns:
            A set of allowed digit or sign token IDs.

        Raises:
            ValueError: If the generated tokens do not form
                a valid number prefix.
        """
        if len(generated) >= 15:
            return set()

        state = self._state_of(generated)

        if state == NumberState.START:
            return self._digits | {self._minus}

        if state == NumberState.SIGN:
            return self._digits

        if state == NumberState.INTEGER:
            if self._is_integer:
                return self._digits
            return self._digits | {self._dot}

        if state == NumberState.DOT:
            return self._digits

        if state == NumberState.FRACTION:
            return self._digits

        raise ValueError("Invalid number prefix.")

    def is_complete(self, generated: list[int]) -> bool:
        """Number is complete if it stopped in a valid numeric state.

        Args:
            generated: A list of token IDs generated for this number so far.

        Returns:
            True if the number is in a complete numeric state, False otherwise.
        """
        try:
            state = self._state_of(generated)
            return state in {NumberState.INTEGER, NumberState.FRACTION}
        except ValueError:
            return False

    def _state_of(self, generated: list[int]) -> NumberState:
        """Determine the current lexical state of
        the generated numeric token IDs.

        Args:
            generated: A list of token IDs generated for this number so far.

        Returns:
            The corresponding NumberState enum value.

        Raises:
            ValueError: If the generated token sequence represents
                an invalid prefix.
        """
        if len(generated) == 0:
            return NumberState.START

        if generated == [self._minus]:
            return NumberState.SIGN

        if all(token in self._digits for token in generated):
            return NumberState.INTEGER

        if (
            generated[0] == self._minus
            and all(token in self._digits for token in generated[1:])
        ):
            return NumberState.INTEGER

        if (
            len(generated) >= 2
            and generated[-1] == self._dot
            and all(token in self._digits for token in generated[:-1])
        ):
            return NumberState.DOT

        if (
            len(generated) >= 3
            and generated[0] == self._minus
            and generated[-1] == self._dot
            and all(token in self._digits for token in generated[1:-1])
        ):
            return NumberState.DOT

        if self._dot in generated:
            dot = generated.index(self._dot)
            if (
                all(token in self._digits for token in generated[:dot])
                and all(token in self._digits for token in generated[dot + 1:])
                and len(generated[dot + 1:]) > 0
            ):
                return NumberState.FRACTION

        if (
            generated[0] == self._minus
            and self._dot in generated[1:]
        ):
            dot = generated.index(self._dot)
            if (
                all(token in self._digits for token in generated[1:dot])
                and all(token in self._digits for token in generated[dot + 1:])
                and len(generated[dot + 1:]) > 0
            ):
                return NumberState.FRACTION

        raise ValueError("Invalid number prefix.")
