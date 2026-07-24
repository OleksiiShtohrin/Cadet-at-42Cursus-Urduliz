"""StringConstraint module.

Restricts vocabulary tokens during greedy decoding to form syntactically valid,
properly escaped JSON strings.
"""

import json
from src.constraint import Constraint
from src.llm import LLM


class StringConstraint(Constraint):
    """Allows generation of any valid JSON string,
    terminating strictly on quote.
    """

    def __init__(self, model: LLM) -> None:
        """Parse and classify vocabulary tokens for safe string
        boundary generation.

        Args:
            model: The LLM wrapper instance.
        """
        self._model: LLM = model
        self._quote: int = model.encode_single_token('"')

        # Load clean vocabulary from the model's snapshot path
        with open(model.get_vocab_path(), "r", encoding="utf-8") as f:
            vocab_raw = json.load(f)

        # Standard BPE byte encoder mapping
        bs = (
            list(range(ord("!"), ord("~") + 1))
            + list(range(ord("¡"), ord("¬") + 1))
            + list(range(ord("®"), ord("ÿ") + 1))
        )
        cs = bs[:]
        n = 0
        for b in range(256):
            if b not in bs:
                bs.append(b)
                cs.append(256 + n)
                n += 1
        cs_chars = [chr(x) for x in cs]
        unicode_to_bytes = dict(zip(cs_chars, bs))

        self._clean_vocab: dict[int, str] = {}
        for token_str, token_id in vocab_raw.items():
            try:
                b_list = [
                    unicode_to_bytes[c]
                    for c in token_str
                    if c in unicode_to_bytes
                ]
                decoded = bytes(b_list).decode("utf-8", errors="replace")
                self._clean_vocab[int(token_id)] = decoded
            except Exception:
                self._clean_vocab[int(token_id)] = token_str

        # Separate allowed string characters from valid closing quote tokens
        self._string_tokens: set[int] = set()
        self._close_quote_tokens: set[int] = {self._quote}

        for tid, t in self._clean_vocab.items():
            if tid >= 151643 or t == "<|endoftext|>":
                continue
            if not t:
                continue

            # FIXED: Exclude any tokens containing raw control characters
            # (ASCII < 32).
            if any(ord(c) < 32 for c in t):
                continue

            if '"' not in t:
                # Token is safe to generate inside a JSON string
                self._string_tokens.add(tid)
            elif t.endswith('\\"'):
                self._string_tokens.add(tid)
            elif t.count('"') == 1 and t.endswith('"'):
                # Token acts as a valid closing boundary for a JSON string
                self._close_quote_tokens.add(tid)

    def next_allowed(self, generated: list[int]) -> set[int]:
        """Allow opening quote first, followed by string chars
        or closing quote.

        Args:
            generated: List of token IDs generated for this string so far.

        Returns:
            A set of allowed token IDs.
        """
        if len(generated) == 0:
            return {self._quote}

        # If string is already closed with matching quote,
        # do not allow further string tokens
        if self.is_complete(generated):
            return set()

        return self._string_tokens | self._close_quote_tokens

    def is_complete(self, generated: list[int]) -> bool:
        """String completes when closed with a valid matching quote token.

        Args:
            generated: List of token IDs generated for this string so far.

        Returns:
            True if completed, False otherwise.
        """
        if len(generated) < 2:
            return False

        if generated[0] != self._quote:
            return False

        # Complete if the last token is one of
        # the verified closing quote tokens
        return generated[-1] in self._close_quote_tokens
