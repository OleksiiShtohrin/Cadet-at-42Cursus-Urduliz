"""Inference generator module implementing schema-constrained greedy decoding.

Leverages numpy for high-performance logit selection on large vocabularies
and implements real-time color-coded terminal visualization
of the decoding process.
"""

import numpy as np
from src.decoder import Decoder
from src.llm import LLM
from src.models import FunctionDefinition, Prompt


class Generator:
    """Performs greedy constrained decoding utilizing Decoder-states."""

    def __init__(self, model: LLM) -> None:
        """Initialize generator wrapper.

        Args:
            model: The LLM wrapper instance.
        """
        self._model: LLM = model
        # Structural JSON tokens should never receive repetition penalty.
        self._excluded_tokens: set[int] = {
            self._model.encode_single_token('"'),
            self._model.encode_single_token(","),
            self._model.encode_single_token(":"),
            self._model.encode_single_token("{"),
            self._model.encode_single_token("}"),
        }

        # Numbers are commonly repeated inside JSON values.
        self._excluded_tokens |= {
            self._model.encode_single_token(str(i))
            for i in range(10)
        }

    def generate(
        self,
        prompt: Prompt,
        functions: list[FunctionDefinition],
    ) -> str:
        """Generate a constrained, schema-compliant JSON string safely.

        Args:
            prompt: The input user prompt.
            functions: List of available function definitions.

        Returns:
            The complete, validated JSON string representing the function call.
        """
        decoder = Decoder(
            model=self._model,
            prompt=prompt,
            functions=functions,
        )

        # High-density system prompt keeping the original robust structure
        # with tailored clean guidelines for our specific functions.
        system_text = (
            "System: You are an API assistant. Choose the correct function"
            " name to call based on the user request. Output only the valid"
            " JSON response.\nAvailable functions:\n"
        )
        for func in functions:
            params_str = ", ".join(
                f"{p_name}: {p_info.type}"
                for p_name, p_info in func.parameters.items()
            )
            system_text += f"- {func.name}({params_str}): {func.description}\n"

        system_text += """
Respond with a JSON object containing:
"prompt": the original user request
"name": the function name to call
"parameters": object with the function parameters

Rules:
"source_string" must be exactly the raw string or sentence to modify,
without any changes. Do NOT perform any substitutions
or edits yourself inside the JSON values.
"regex" must be the simplest pattern to find ("cat" for the word) don't add $.
"replacement" must be the exact replacement string "*", don't add the JSON.

Example:
{"prompt": "What is the sum of 40 and 2?",
"name": "fn_add_numbers", "parameters": {"a": 40.0, "b": 2.0}}
"""

        system_text += f"\nUser: {prompt.prompt}\nAssistant: "

        # Start tokens list
        input_ids = self._model.encode_sequence(system_text)

        # Increased to 250 to prevent truncation on longer parameters
        max_tokens = 150
        token_count = 0

        while True:
            token_count += 1
            if token_count > max_tokens:
                break

            allowed = decoder.allowed_tokens()

            if not allowed:
                break

            # OPTIMIZATION 1: Bypass LLM forward pass if only
            # 1 token is grammatically valid
            if len(allowed) == 1:
                next_token = list(allowed)[0]
                prob_str = "\033[90mForced\033[0m"
            else:
                logits = self._model.get_logits(input_ids)

                # REPETITION PENALTY:
                # Prevent infinite loops in regex generation
                # Do not penalize structural JSON tokens.
                recent_tokens = set(input_ids[-10:])

                for token_id in recent_tokens:
                    if token_id in self._excluded_tokens:
                        continue

                    if token_id in allowed and token_id < len(logits):
                        if logits[token_id] > 0:
                            logits[token_id] /= 1.2
                        else:
                            logits[token_id] *= 1.2

                # OPTIMIZATION 2:
                # Super fast C-level NumPy argmax for huge allowed sets
                allowed_arr = np.array(list(allowed), dtype=np.int32)
                allowed_logits = np.array(logits)[allowed_arr]
                next_token = int(allowed_arr[np.argmax(allowed_logits)])

                # Calculate the token's probability via Softmax
                exp_logits = np.exp(allowed_logits - np.max(allowed_logits))
                probs = exp_logits / np.sum(exp_logits)
                selected_idx = list(allowed).index(next_token)
                prob = probs[selected_idx]
                prob_str = f"\033[95m{prob:.1%}\033[0m"

            # Beautiful real-time console visualization
            state_name = decoder.current_state().name
            raw_token_text = self._model.decode([next_token])
            # Escape newlines so terminal output remains single-line per token
            clean_token_repr = repr(raw_token_text.replace("\n", "\\n"))

            print(
                f"\033[92m[Dec]\033[0m "
                f"State: \033[94m{state_name:<15}\033[0m | "
                f"Token: \033[93m{clean_token_repr:<12}\033[0m | "
                f"Allowed: {len(allowed):<3} | "
                f"Prob: {prob_str}"
            )

            decoder.consume_token(next_token)
            input_ids.append(next_token)

        generated = decoder.generated_tokens()
        return self._model.decode(generated)
