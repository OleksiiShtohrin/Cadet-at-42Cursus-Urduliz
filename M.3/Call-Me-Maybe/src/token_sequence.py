"""Fixed token sequence constraint module.

Enforces the generation of specific literal JSON structural delimiters or key
names.
"""

from src.constraint import Constraint


class TokenSequence(Constraint):
    """Represents one fixed sequence of token ids.

    Used by the constrained decoder to emit multi-token
    JSON fragments one token at a time.
    """

    def __init__(self, tokens: list[int]) -> None:
        """Initialize the token sequence with a copy of target token IDs.

        Args:
            tokens: A list of target token IDs that need to be generated
                one-by-one.
        """
        self._tokens: list[int] = tokens.copy()

    def tokens(self) -> list[int]:
        """Return the complete token sequence.

        Returns:
            A copy of the complete target token sequence.
        """
        return self._tokens.copy()

    def length(self) -> int:
        """Return sequence length.

        Returns:
            The total number of tokens in the expected sequence.
        """
        return len(self._tokens)

    def next_allowed(self, generated: list[int]) -> set[int]:
        """Return the next allowed token ID.

        Args:
            generated: A list of token IDs generated for this sequence
                so far.

        Returns:
            A set containing exactly one token ID representing the next
            legal token in the sequence.

        Raises:
            ValueError: If the generated tokens are not a valid prefix
                of the target sequence.
        """
        if len(generated) > len(self._tokens):
            raise ValueError(
                "Generated tokens are not a prefix of the target sequence."
            )

        if generated != self._tokens[:len(generated)]:
            raise ValueError(
                "Generated tokens are not a prefix of the target sequence."
            )

        if len(generated) == len(self._tokens):
            return set()

        return {self._tokens[len(generated)]}

    def is_complete(self, generated: list[int]) -> bool:
        """Return True if the full sequence has been generated.

        Args:
            generated: A list of token IDs generated for this sequence
                so far.

        Returns:
            True if all tokens in the target sequence have been successfully
            and sequentially matched, False otherwise.
        """
        return generated == self._tokens
