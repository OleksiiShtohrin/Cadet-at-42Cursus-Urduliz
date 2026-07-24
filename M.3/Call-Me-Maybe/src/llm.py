"""LLM Module.

A clean wrapper around the provided Small_LLM_Model to prevent
PyTorch/Transformers imports within the student's core codebase.
"""

import sys
from typing import cast

# Safe import validation to prevent compile-time crashes if llm_sdk is missing
try:
    from llm_sdk.llm_sdk import Small_LLM_Model
except ImportError:
    print(
        "❌ Error: 'llm_sdk' package not found or import path is incorrect!\n"
        "Please ensure the 'llm_sdk' directory is present"
        " in the project root.",
        file=sys.stderr
    )
    sys.exit(1)


class LLM:
    """Wrapper around the provided Small_LLM_Model.

    This class hides SDK-specific implementation details and prevents
    importing PyTorch or Transformers inside the student's src/ codebase.
    """

    def __init__(self, model_name: str = "Qwen/Qwen3-0.6B") -> None:
        """Load local causal language model weights under the hood."""
        self._model: Small_LLM_Model = Small_LLM_Model(model_name=model_name)

    def encode(self, text: str) -> list[int]:
        """Convert raw string to token IDs as a list of integers.

        Args:
            text: A string of text to encode.

        Returns:
            A list of token ID integers.
        """
        tensor_ids = self._model.encode(text)
        return cast(list[int], tensor_ids[0].tolist())

    def decode(self, input_ids: list[int]) -> str:
        """Convert token IDs back to a readable string.

        Args:
            input_ids: A list of token ID integers to decode.

        Returns:
            The decoded human-readable string.
        """
        return self._model.decode(input_ids)

    def get_logits(self, input_ids: list[int]) -> list[float]:
        """Get prediction logits for the next token using clean Python lists.

        Args:
            input_ids: A list of token ID integers representing
                the sequence context.

        Returns:
            A list of floats representing predicted next-token logits.
        """
        return self._model.get_logits_from_input_ids(input_ids)

    def get_vocab_path(self) -> str:
        """Return vocabulary filepath.

        Returns:
            The absolute or relative file path to the model's vocabulary file.
        """
        return self._model.get_path_to_vocab_file()

    def encode_single_token(self, text: str) -> int:
        """Encode a string mapping strictly to exactly one BPE token.

        Args:
            text: A string of text representing a single target token.

        Returns:
            The corresponding token ID.

        Raises:
            ValueError: If the input text encodes to multiple tokens.
        """
        ids = self.encode(text)

        if len(ids) != 1:
            raise ValueError(f'"{text}" is encoded into multiple tokens.')

        return ids[0]

    def encode_sequence(self, text: str) -> list[int]:
        """Encode string to a standard sequence of token IDs.

        Args:
            text: A string of text to encode.

        Returns:
            A list of token ID integers.
        """
        return self.encode(text)
