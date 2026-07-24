"""Decoder coordinator module.

Coordinates and transitions through the master states of the output JSON string
object: START, PROMPT_KEY, PROMPT_VALUE, NAME_KEY, NAME_VALUE, PARAMETERS_KEY,
PARAMETER, FINISHED.
"""

import json
from src.decoder_state import DecoderState
from src.llm import LLM
from src.models import FunctionDefinition, Prompt
from src.token_sequence import TokenSequence
from src.function_name_constraint import FunctionNameConstraint
from src.parameter_constraint import ParameterConstraint
from src.constraint import Constraint


class Decoder:
    """Stateful coordinator of constraints for JSON generation."""

    def __init__(
        self,
        model: LLM,
        prompt: Prompt,
        functions: list[FunctionDefinition],
    ) -> None:
        """Setup JSON-grammar states conforming to expected results schema.

        Args:
            model: The LLM wrapper instance.
            prompt: The user prompt input model.
            functions: List of available function definitions.
        """
        self._model: LLM = model
        self._prompt: Prompt = prompt
        self._functions: list[FunctionDefinition] = functions

        self._state: DecoderState = DecoderState.START
        self._generated_tokens: list[int] = []

        self._symbols: dict[str, int] = {
            "open_brace": model.encode_single_token("{"),
            "close_brace": model.encode_single_token("}"),
            "quote": model.encode_single_token('"'),
            "comma": model.encode_single_token(","),
        }

        self._sequences: dict[str, TokenSequence] = {
            "prompt_key": TokenSequence(
                model.encode_sequence('"prompt":')
            ),
            "name_key": TokenSequence(
                model.encode_sequence('"name":')
            ),
            "parameters_key": TokenSequence(
                model.encode_sequence('"parameters":')
            ),
        }

        # FIXED:
        # Use json.dumps to properly escape quotes in prompt string values
        self._prompt_sequence: TokenSequence = TokenSequence(
            model.encode_sequence(json.dumps(prompt.prompt))
        )

        quoted_functions: list[FunctionDefinition] = []
        for function in functions:
            copied = FunctionDefinition(
                name=f'"{function.name}"',
                description=function.description,
                parameters=function.parameters,
                returns=function.returns,
            )
            quoted_functions.append(copied)

        self._function_names: FunctionNameConstraint = FunctionNameConstraint(
            model=model, functions=quoted_functions
        )

        self._parameter_constraint: ParameterConstraint | None = None
        self._constraint_start: int = 0

        self._constraints: dict[DecoderState, Constraint | None] = {
            DecoderState.PROMPT_KEY: self._sequences["prompt_key"],
            DecoderState.PROMPT_VALUE: self._prompt_sequence,
            DecoderState.NAME_KEY: self._sequences["name_key"],
            DecoderState.NAME_VALUE: self._function_names,
            DecoderState.PARAMETERS_KEY: self._sequences["parameters_key"],
            DecoderState.PARAMETER: None,
        }

        self._next_state: dict[DecoderState, DecoderState] = {
            DecoderState.PROMPT_KEY: DecoderState.PROMPT_VALUE,
            DecoderState.PROMPT_VALUE: DecoderState.NAME_KEY,
            DecoderState.NAME_KEY: DecoderState.NAME_VALUE,
            DecoderState.NAME_VALUE: DecoderState.PARAMETERS_KEY,
            DecoderState.PARAMETERS_KEY: DecoderState.PARAMETER,
            DecoderState.PARAMETER: DecoderState.FINISHED,
        }

    def current_state(self) -> DecoderState:
        """Return current state.

        Returns:
            The active DecoderState enum value.
        """
        return self._state

    def allowed_tokens(self) -> set[int]:
        """Prune next tokens based on active schema boundary.

        Returns:
            A set of allowed token IDs that are legally permitted next.
        """
        if self._state == DecoderState.START:
            return {self._symbols["open_brace"]}

        if self._state == DecoderState.FINISHED:
            open_count = self._generated_tokens.count(
                self._symbols["open_brace"]
            )
            close_count = self._generated_tokens.count(
                self._symbols["close_brace"]
            )
            if close_count < open_count:
                return {self._symbols["close_brace"]}
            return set()

        constraint = self._constraints.get(self._state)
        if constraint is None:
            return set()

        return constraint.next_allowed(self._current_sequence_tokens())

    def consume_token(self, token_id: int) -> None:
        """Register the token and update states accordingly.

        Args:
            token_id: The newly generated token ID to append and process.
        """
        self._generated_tokens.append(token_id)

        if (
            self._state == DecoderState.FINISHED
            and token_id == self._symbols["close_brace"]
        ):
            return

        if self._state == DecoderState.START:
            if token_id == self._symbols["open_brace"]:
                self._state = DecoderState.PROMPT_KEY
                self._constraint_start = len(self._generated_tokens)
            return

        current_constraint = self._constraints.get(self._state)
        if current_constraint is None:
            return

        if isinstance(current_constraint, ParameterConstraint):
            current_constraint.consume_token(token_id)

        if current_constraint.is_complete(
            self._current_sequence_tokens()
        ):
            if self._state == DecoderState.NAME_VALUE:
                selected = self._function_names.selected_function()
                unquoted_name = selected.name.replace('"', "")
                real_selected = next(
                    f for f in self._functions if f.name == unquoted_name
                )

                self._parameter_constraint = ParameterConstraint(
                    model=self._model,
                    function=real_selected,
                )
                self._constraints[
                    DecoderState.PARAMETER
                ] = self._parameter_constraint

            # Inject delimiters between fields to comply with JSON syntax
            if self._state == DecoderState.PROMPT_VALUE:
                self._generated_tokens.append(self._symbols["comma"])

            elif self._state == DecoderState.NAME_VALUE:
                self._generated_tokens.append(self._symbols["comma"])

            if self._state in self._next_state:
                self._state = self._next_state[self._state]

            self._constraint_start = len(self._generated_tokens)

    def generated_tokens(self) -> list[int]:
        """Return generated token sequence.

        Returns:
            A copy of the list of generated token IDs.
        """
        return self._generated_tokens.copy()

    def _current_sequence_tokens(self) -> list[int]:
        """Slices generated tokens to return only
        those belonging to current state.

        Returns:
            A slice of generated token IDs for the active state constraint.
        """
        return self._generated_tokens[self._constraint_start:]
