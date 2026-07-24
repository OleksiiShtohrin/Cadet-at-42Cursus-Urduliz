"""Main orchestration module running the full constrained decoding suite.

Reads natural language prompts, applies state-constrained grammar parsing,
and writes validated outputs using Pydantic schemas. Includes execution timing
and robust schema validation error handling.
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List
from pydantic import ValidationError

from src.generator import Generator
from src.llm import LLM
from src.models import FunctionCallResult
from src.parser import parse_function_definitions, parse_test_prompts


def main() -> None:
    """Execution pipeline reading prompts, driving decoder,
    and saving validated JSON.
    """
    parser = argparse.ArgumentParser(
        description="Structured JSON Function Calling with LLMs "
        "(Modular Edition)"
    )
    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json",
        help="Path to functions schema file",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
        help="Path to input prompts file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json",
        help="Path to output results file",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="Qwen/Qwen3-0.6B",
        help="Model name (default: Qwen/Qwen3-0.6B)"
    )
    args = parser.parse_args()

    # Gracefully handle file errors
    try:
        functions = parse_function_definitions(args.functions_definition)
    except FileNotFoundError:
        print(
            f"Error: Functions schema not found at "
            f"{args.functions_definition}", file=sys.stderr
        )
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(
            f"Error: Invalid JSON structure in functions definition: {e}",
            file=sys.stderr
        )
        sys.exit(1)
    except ValidationError as e:
        print(
            f"Error: Schema validation failed for functions definition:\n{e}",
            file=sys.stderr
        )
        sys.exit(1)

    try:
        prompts = parse_test_prompts(args.input)
    except FileNotFoundError:
        print(
            f"Error: Prompt tests file not found at {args.input}",
            file=sys.stderr
        )
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(
            f"Error: Invalid JSON structure in input tests: {e}",
            file=sys.stderr
        )
        sys.exit(1)
    except ValidationError as e:
        print(
            f"Error: Schema validation failed for input tests:\n{e}",
            file=sys.stderr
        )
        sys.exit(1)

    print(f"Loaded {len(functions)} functions.")
    print(f"Loaded {len(prompts)} prompts.")

    print("Loading LLM model...")
    model = LLM(model_name=args.model)
    generator = Generator(model)

    results: List[Dict[str, Any]] = []

    print("\nStarting modular constrained decoding inference...")

    # Start the execution timer
    start_time = time.time()

    for i, prompt in enumerate(prompts, start=1):
        print(f"[{i}/{len(prompts)}] Processing prompt: '{prompt.prompt}'")
        print("Thinking...\n", end="", flush=True)

        try:
            # Generate the entire valid JSON object string
            # via Decoder State Machine
            result_str = generator.generate(
                prompt=prompt,
                functions=functions,
            )
            print()  # Newline after progress dots

            # Safely parse the generated JSON
            parsed_json = json.loads(result_str)

            # Standardize prompt key in parameters object if necessary
            unquoted_name = parsed_json.get("name", "").replace('"', "")

            # FIXED: Strict schema-based type conversion & whitespace
            func_schema = next(
                (f for f in functions if f.name == unquoted_name), None
            )
            actual_params = parsed_json.get("parameters", {})
            parameters_to_save: Dict[str, Any] = {}

            if func_schema:
                for p_name, p_info in func_schema.parameters.items():
                    val = actual_params.get(p_name)
                    if val is not None:
                        if p_info.type == "number":
                            parameters_to_save[p_name] = float(val)
                        elif p_info.type == "integer":
                            parameters_to_save[p_name] = int(val)
                        elif p_info.type == "string":
                            # Strip accidental leading spaces
                            val_str = str(val).strip()
                            parameters_to_save[p_name] = val_str
                        else:
                            parameters_to_save[p_name] = val
                    else:
                        parameters_to_save[p_name] = None
            else:
                parameters_to_save = actual_params

            # Validate using Pydantic result model
            validated_call = FunctionCallResult(
                prompt=prompt.prompt,
                name=unquoted_name,
                parameters=parameters_to_save
            )
            results.append(validated_call.model_dump())

        except Exception as e:
            # Fallback to prevent crashes on weird inputs
            print(
                f"\nWarning: Failed to parse result for prompt {i}: {e}",
                file=sys.stderr
            )
            fallback = FunctionCallResult(
                prompt=prompt.prompt,
                name="fn_unknown",
                parameters={}
            )
            results.append(fallback.model_dump())

    # Write target validation outputs
    try:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
    except Exception as e:
        print(f"Error: Failed to write output file: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\n🎉 Successfully saved structured output to: {args.output}")

    # Calculate and display the total elapsed time
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    print(
        f"⏱️  Total execution time: "
        f"{int(minutes)}m {seconds:.2f}s ({elapsed_time:.2f}s)"
    )


if __name__ == "__main__":
    main()
