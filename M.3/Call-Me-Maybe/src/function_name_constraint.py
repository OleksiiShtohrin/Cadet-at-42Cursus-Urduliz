"""FunctionNameConstraint module.

Constrains the model's choices to exactly match one of the available functions
defined in the schema.
"""

from src.constraint import Constraint
from src.llm import LLM
from src.models import FunctionDefinition
from src.token_sequence import TokenSequence


class FunctionNameConstraint(Constraint):
    """Constrains generation to exactly match one
    of the available function names.
    """

    def __init__(
        self,
        model: LLM,
        functions: list[FunctionDefinition],
    ) -> None:
        """Precompile token sequences for all function names.

        Args:
            model: The LLM wrapper instance.
            functions: A list of available function schemas.
        """
        self._functions: list[FunctionDefinition] = functions
        self._sequences: list[TokenSequence] = [
            TokenSequence(model.encode_sequence(function.name))
            for function in functions
        ]
        self._selected_index: int | None = None

    def next_allowed(self, generated: list[int]) -> set[int]:
        """Collect all allowed next tokens from valid active prefixes.

        Args:
            generated: A list of token IDs generated for this constraint
                so far.

        Returns:
            A set of allowed next token IDs that match at least
            one function name.

        Raises:
            ValueError: If the generated tokens do not match any available
                function name prefix.
        """
        allowed: set[int] = set()

        for sequence in self._sequences:
            try:
                allowed |= sequence.next_allowed(generated)
            except ValueError:
                pass

        if not allowed:
            raise ValueError(
                "Generated tokens do not match any function name."
            )

        return allowed

    def is_complete(self, generated: list[int]) -> bool:
        """Check if any complete function name matches exactly.

        Args:
            generated: A list of token IDs generated for this constraint
                so far.

        Returns:
            True if one of the expected function names has been fully and
            exactly matched, False otherwise.
        """
        for index, sequence in enumerate(self._sequences):
            if sequence.is_complete(generated):
                self._selected_index = index
                return True

        return False

    def selected_function(self) -> FunctionDefinition:
        """Return the parsed function definition after selection.

        Returns:
            The matched FunctionDefinition object.

        Raises:
            RuntimeError: If a function name has not been
                successfully matched yet.
        """
        if self._selected_index is None:
            raise RuntimeError("Function has not been selected yet.")

        return self._functions[self._selected_index]
