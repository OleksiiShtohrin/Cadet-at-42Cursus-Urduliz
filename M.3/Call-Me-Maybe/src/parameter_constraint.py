"""ParameterConstraint module.

Strictly manages and coordinates token generation for the entire JSON
parameters object, stepping through keys, values, and delimiters.
"""

from src.constraint import Constraint
from src.llm import LLM
from src.models import FunctionDefinition
from src.token_sequence import TokenSequence
from src.number_constraint import NumberConstraint
from src.string_constraint import StringConstraint


class ParameterConstraint(Constraint):
    """Restricts generation of the JSON parameters object."""

    def __init__(
        self,
        model: LLM,
        function: FunctionDefinition,
    ) -> None:
        """Construct parameter constraint matching schema definitions.

        Args:
            model: The LLM wrapper instance.
            function: The selected function definition schema.
        """
        self._model: LLM = model
        self._function: FunctionDefinition = function

        self._steps: list[Constraint] = self._build_steps()
        self._current_step: int = 0
        self._step_start: int = 0
        self._generated_tokens: list[int] = []

    def next_allowed(self, generated: list[int]) -> set[int]:
        """Delegate allowed tokens to the active sub-constraint.

        Args:
            generated: A list of token IDs generated for
                this constraint sequence so far.

        Returns:
            A set of allowed token IDs.
        """
        current = self._steps[self._current_step]
        allowed = current.next_allowed(self._current_tokens())

        # Lookahead Union: If current step is complete,
        # allow next step's tokens too!
        if (
            current.is_complete(self._current_tokens())
            and self._current_step + 1 < len(self._steps)
        ):
            next_step = self._steps[self._current_step + 1]
            try:
                allowed |= next_step.next_allowed([])
            except Exception:
                pass

        return allowed

    def consume_token(self, token: int) -> None:
        """Log token and advance step if sub-constraint completes.

        Args:
            token: The newly z-generated token ID.
        """
        current = self._steps[self._current_step]

        # Transition to the next step if the token belongs
        # to the next step's start
        if (
            current.is_complete(self._current_tokens())
            and self._current_step + 1 < len(self._steps)
        ):
            next_step = self._steps[self._current_step + 1]
            try:
                if token in next_step.next_allowed([]):
                    self._current_step += 1
                    self._step_start = len(self._generated_tokens)
                    current = next_step
            except Exception:
                pass

        self._generated_tokens.append(token)

        if isinstance(current, ParameterConstraint):
            current.consume_token(token)

        # Only advance to the next step automatically if it is
        # a fixed TokenSequence.
        if (
            isinstance(current, TokenSequence)
            and current.is_complete(self._current_tokens())
        ):
            self._current_step += 1
            self._step_start = len(self._generated_tokens)

    def is_complete(self, generated: list[int]) -> bool:
        """Check if all sub-constraints are generated.

        Args:
            generated: A list of token IDs generated for this parameters object
                so far.

        Returns:
            True if all required parameter keys, values, and closing delimiters
            have been successfully emitted, False otherwise.
        """
        return self._current_step == len(self._steps)

    def _current_tokens(self) -> list[int]:
        """Slices generated tokens to return only those belonging
        to the active step.

        Returns:
            A slice of generated token IDs starting from the start of
            the current step.
        """
        return self._generated_tokens[self._step_start:]

    def _build_steps(self) -> list[Constraint]:
        """Compile a list of sub-constraints to parse
        the parameters object sequentially.

        Returns:
            A sequence of constraints representing open brace,
            parameter key-value pairs, commas, and close brace.

        Raises:
            ValueError: If an unsupported parameter type
            is encountered in schema.
        """
        steps: list[Constraint] = []

        steps.append(TokenSequence(self._model.encode_sequence("{")))

        parameters = list(self._function.parameters.items())

        for index, (parameter_name, parameter) in enumerate(parameters):
            steps.append(
                TokenSequence(
                    self._model.encode_sequence(
                        f'"{parameter_name}":'
                    )
                )
            )

            if parameter.type == "number":
                steps.append(NumberConstraint(self._model, is_integer=False))

            elif parameter.type == "integer":
                # FIXED: Fully support integer parameter types!
                steps.append(NumberConstraint(self._model, is_integer=True))

            elif parameter.type == "string":
                steps.append(StringConstraint(self._model))

            else:
                raise ValueError(
                    f"Unsupported parameter type: {parameter.type}"
                )

            if index != len(parameters) - 1:
                steps.append(TokenSequence(self._model.encode_sequence(",")))

        steps.append(TokenSequence(self._model.encode_sequence("}")))

        return steps
