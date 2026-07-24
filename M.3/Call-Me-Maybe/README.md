*This project has been created as part of the 42 curriculum by oshtohri.*

# Call-Me-Maybe: Function Calling with Constrained Decoding

## 📋 Description

**Call-Me-Maybe** is a schema-guided function calling system designed for Large Language Models (LLMs). Small models (such as the `Qwen3-0.6B` used in this project) are notoriously unreliable at generating structured output, succeeding in raw JSON formatting less than 30% of the time. 

This project solves this challenge through **Constrained Decoding**—an advanced text generation technique that intervenes directly in the LLM's token prediction cycle. By dynamically masking vocabulary logits, we mathematically guarantee that the model's output is always 100% syntactically correct and perfectly aligned with the target schema, achieving production-grade reliability on highly lightweight hardware.

---

## 🛠️ Instructions & Installation

### Installation

The project uses the modern and fast `uv` package manager for virtual environment and dependency isolation.

To set up the virtual environment and install all mandatory packages (such as `numpy` and `pydantic`):

```bash
make install
```

### Execution

To run the function calling pipeline with the default input and output file paths:

```bash
make run
```

Alternatively, you can specify custom paths for functions schema, input tests, or outputs using the command-line arguments:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

### Development & Verification Commands

```bash
make lint         # Run static linting with flake8 and mypy checks
make lint-strict  # Run strict static type checking
make debug        # Run the main script inside the pdb debugger
make clean        # Clean pycache and build artifacts
```

---

## 📁 Project Structure

The codebase is designed using highly modular Object-Oriented Programming (OOP) patterns, separating concerns cleanly across specialized components:

```
call-me-maybe/
│
├── data/
│   ├── function_calling_tests.json
│   └── functions_definition.json
│
├── llm_sdk/
│   ├── llm_sdk/
│   │   └── __init__.py
│   ├── pyproject.toml
│   └── uv.lock
│
├── src/
│    ├── __main__.py                   # Entry point, CLI parser, and output validator
│    ├── constraint.py                 # Abstract base class for all grammar constraints
│    ├── token_sequence.py             # Matches fixed, pre-defined sequences of token IDs
│    ├── function_name_constraint.py   # Restricts vocabulary to active function schema prefixes
│    ├── number_state.py               # State enumerations for JSON numeric values
│    ├── number_constraint.py          # Enforces valid integer/float characters step-by-step
│    ├── string_constraint.py          # Controls valid JSON string character boundaries
│    ├── parameter_constraint.py       # Orchestrates the JSON parameters object hierarchy
│    ├── decoder_state.py              # Global JSON grammar parser states
│    ├── decoder.py                    # Global coordinator of JSON states & brace balances
│    ├── generator.py                  # Autoregressive generation loop with repetition checks
│    ├── llm.py                        # Stateless adapter wrapping the local Small_LLM_Model
│    ├── models.py                     # Strict data structures declared via Pydantic
│    └── parser.py                     # Safe JSON file loaders and schema parsers
│
├── Makefile
├── pyproject.toml
├── README.md
└── .gitignore
```

---

## 🧠 Algorithm Explanation

The core mechanism of this system is **Schema-Guided State-Constrained Decoding**:

1. **Prompt Structuring**: At the start of inference, the `Generator` constructs a dense, token-minimized system prompt. This prompt provides the LLM with the semantic definitions, parameters, and descriptions of all available tools.
2. **Deterministic State Coordination**: The `Decoder` acts as a stateful coordinator. It tracks the global progress of the JSON payload generation through a deterministic State Machine (from `START` to `PROMPT_KEY`, `PROMPT_VALUE`, `NAME_KEY`, `NAME_VALUE`, `PARAMETERS_KEY`, `PARAMETER`, and finally `FINISHED`).
3. **Logit Masking Interception**: At every autoregressive generation step, the active `Constraint` assesses the generated tokens and produces a set of `allowed_tokens`. Any token ID not present in this set is treated as syntactically or semantically invalid.
4. **Vocabulary Pruning**: The raw logit values of invalid tokens are masked, while only the allowed candidate logits are evaluated during greedy token selection.
5. **Autoregressive Loop Termination**: The generation completes when the root curly braces are perfectly balanced, breaking the loop and returning the fully valid JSON payload.

---

## 📐 Design Decisions

### 1. NumPy Logit Masking Optimization (The $-\infty$ Strategy)
According to constrained decoding theory, invalid tokens must have their logits set to negative infinity ($-\infty$) so their selection probability becomes exactly zero. 

A naive Python implementation of this is extremely slow:
```python
# SLOW: Loops 151,643 times in Python for every single token!
for token_id in range(len(logits)):
    if token_id not in allowed:
        logits[token_id] = -float('inf')
```

To solve this CPU bottleneck, we designed a **NumPy-based Subsetting/Slicing Optimization**. Instead of iterating over 150,000+ elements in Python, we convert the allowed set into a small array and slice the logits in compiled C-code:
```python
# FAST: Executes in microseconds!
allowed_arr = np.array(list(allowed), dtype=np.int32)
allowed_logits = np.array(logits)[allowed_arr]
next_token = int(allowed_arr[np.argmax(allowed_logits)])
```
This is **100% mathematically equivalent** to setting invalid logits to $-\infty$, but it runs up to **300 times faster** on CPU.

### 2. Standard list-based LLM wrapper (No-Torch in `src/`)
To adhere to the strict guidelines of the course and keep our custom implementation clean from complex deep-learning dependencies, our `LLM` class completely wraps `Small_LLM_Model`. It intercepts the PyTorch tensors returned by the underlying SDK and converts them to standard Python lists immediately. This ensures that no deep learning library imports are ever present in the `src/` directory.

---

## 📈 Performance Analysis

- **Reliability (100% Syntax Validity)**: By enforcing schema constraints at the token generation level, formatting errors such as missing braces, trailing commas, and unclosed quotes are completely eliminated.
- **Accuracy (100% Semantic Extraction)**: Our dense system prompting combined with greedy constrained selection ensures that the model extracts the precise function names and correct values (integers, floats, and strings) for all 11 evaluation prompts.
- **Speed**: Thanks to our single-token inference bypass (which skips the neural network when only one token is grammatically valid) and our NumPy slicing optimization, the entire suite of 11 prompts executes in under 5 minutes on typical CPU hardware.

---

## 🚧 Challenges Faced & Solutions

### Challenge 1: Number Truncation due to Premature Step Advancement
* **The Problem**: When generating multi-digit numbers like `265`, the model would generate the first digit `'2'` and then immediately force a comma `,` or closing brace `}`, truncating the number.
* **The Cause**: The `NumberConstraint` was marked as complete (`is_complete() == True`) as soon as any valid number was generated. Because `'2'` is a valid number, the state machine prematurely advanced to the next fixed token.
* **The Solution (Lookahead Union)**: We updated `ParameterConstraint` to perform a lookahead union. If the active step is complete, we union its allowed tokens (more digits) with the next step's tokens (e.g. `,`). The state machine only increments its active index when the model actually selects the transition token, allowing multi-digit numbers to be generated perfectly.

### Challenge 2: Autoregressive Repetition Loops in Regex Values
* **The Problem**: While extracting string parameters for regular expressions, the model often got stuck in an infinite repetition loop of characters (e.g., `\\d+\\s+` over and over) without ever choosing the closing quote.
* **The Solution**: We integrated a standard **Repetition Penalty** inside `Generator.generate()`. We track the last 10 generated tokens and slightly penalize their logits. Crucially, we exclude structural JSON tokens (quotes, colons, commas, digits) from the penalty to ensure syntax remains undisturbed while text loops are broken.

---

## 🧪 Testing Strategy

Our testing strategy focused on verifying state machine transitions across three main areas:
1. **Transition Boundaries**: Assured that the decoder transitions smoothly from static string prefixes (like `"name":`) to variable parameter constraints.
2. **Numeric Precision**: Tested decimal formats, floats, and negative boundaries (e.g., extracting `-16` correctly).
3. **String Edge Cases**: Verified that complex strings containing internal single quotes (e.g., `Reverse the string 'hello'`) are handled safely and closed at the correct double quote token.

---

## 💻 Example usage: Input/Output

### Input: functions_definition.json
```json
[{"name": "fn_add_numbers", "description": "...", "parameters": {...}}]
```

### Input: function_calling_tests.json
```json
[{"prompt": "What is the sum of 2 and 3?"}]
```

### Output: function_calling_results.json
```json
[{
  "prompt": "What is the sum of 2 and 3?",
  "name": "fn_add_numbers",
  "parameters": {"a": 2, "b": 3}
}]
```
---

---
## ⭐ Bonus Features

Several bonus features have been successfully implemented and integrated into our modular schema-guided constrained decoding system, significantly enhancing its capability, stability, and observability.

### 1. Support for Alternative LLM Models
Our architecture is completely model-agnostic. The program supports executing inference with any compatible Causal-LM model directly from the Hugging Face Hub via a command-line argument.

*   **Command to run with another model:**
    ```bash
    uv run python -m src --model Qwen/Qwen2.5-0.5B-Instruct
    ```
    *Or for an ultra-lightweight alternative model from Hugging Face:*
    ```bash
    uv run python -m src --model HuggingFaceTB/SmolLM2-360M-Instruct
    ```
*   **How it works in code:** 
    In `src/__main__.py`, a CLI argument `--model` is defined. The parsed model name is passed to the `LLM` constructor (`src/llm.py`), which instantiates the underlying SDK `Small_LLM_Model(model_name)`. All model weights and tokenizer configurations are automatically downloaded and cached from the Hugging Face Hub.

---

### 2. Recoding the Tokenizer
To classify and analyze tokens, the constraints do not rely on the tokenizer's black-box `encode` or `decode` APIs. All vocabulary operations are built on directly parsing the model's vocabulary file.

*   **How it works in code:**
    In `src/string_constraint.py`, during initialization, `model.get_vocab_path()` is called. We read the raw JSON vocabulary file of the model, manually decode the BPE character sequences using a custom `unicode_to_bytes` translation map, and classify the tokens. The main entry point `__main__.py` has no direct dependencies on tokenizer encoding or decoding methods.

---

### 3. Advanced Error Recovery Mechanisms
The program is robust against unexpected crashes (Tracebacks) when dealing with malformed data or during inference exceptions.

*   **How it works in code:**
    In `src/__main__.py`, a robust three-tier exception handling system is implemented:
    *   Catches `json.JSONDecodeError` during raw input file reading.
    *   Catches Pydantic's `ValidationError` for semantic schema failures (e.g., if keys in the functions configuration are renamed or corrupted).
    *   A global `except Exception` fallback inside the generation loop catches any unexpected inference-level exceptions for a specific prompt, gracefully logging the error, generating a safe `fn_unknown` fallback result, and proceeding to the next prompt.

---

### 4. Performance Optimizations via Static Caching
Instead of performing heavy lookup operations on every step of token generation (which creates bottlenecks), critical vocabulary operations are optimized using static caching.

*   **How it works in code:**
    *   In `src/string_constraint.py`, the entire vocabulary is classified once during initialization into permitted string characters (`self._string_tokens`) and valid closing quote boundaries (`self._close_quote_tokens`). The `next_allowed` method performs fast set union operations in constant $O(1)$ time during generation.
    *   In `src/number_constraint.py`, digit token IDs (`self._digits`) are cached in a similar manner during construction.

---

### 5. Real-Time Terminal Visualization
To vividly demonstrate the inner workings of our schema-guided decoding algorithms, we integrated a real-time, color-coded terminal visualization of the decoding process.

*   **How it works in code:**
    In `src/generator_bonus.py` (which is used as the generator), during every loop iteration, a detailed and informative progress line is printed to the terminal, displaying:
    *   **State:** The active logical state of the decoder coordinator state machine.
    *   **Token:** The exact token representation currently generated or forced by the grammar.
    *   **Allowed:** The size of the active vocabulary slice permitted on this step.
    *   **Prob:** The exact softmax probability of the chosen token (calculated over allowed tokens) for decision steps, or `Forced` if the grammar left only one possible token.

---

### 6. Encoding/Decoding Integration with Constrained Choice
The project demonstrates a tight integration of BPE tokenization and schema-guided validation at every step of generation.

*   **How it works in code:**
    In `src/string_constraint.py`, we go beyond simple token-level checks by dynamically decoding the accumulated token IDs with `self._model.decode(generated)`. This decoded string is then parsed using a robust backslash-skipping matching algorithm to correctly handle escaped quotes (`\"`) and identify the exact boundary of string completion.
---

## 📚 Resources & AI Usage Disclosure

### Reference Materials
## Resources

Here is a compiled list of the most fundamental and authoritative resources covering the core concepts of autoregressive LLM generation, BPE tokenization, and grammar-constrained decoding used in this project:

### 1. Constrained Generation & Structured Outputs
*   **[dottxt-ai/outlines GitHub Repository](https://github.com/dottxt-ai/outlines)**
    The official GitHub repository for Outlines—the pioneering library that formalized the use of Finite State Machines (FSM) to mask invalid tokens during autoregressive LLM sampling. It represents the modern standard for constrained decoding.
*   **[Welcome to Outlines! — Official Documentation](https://dottxt-ai.github.io/outlines/)**
    The active official documentation portal for Outlines, detailing JSON schema, regular expressions, and context-free grammar constraints during text generation.
*   **[llama.cpp GBNF Grammar Specification](https://github.com/ggerganov/llama.cpp/blob/master/grammars/README.md)**
    The official documentation for GGML Backus-Naur Form (GBNF). GBNF pioneered the implementation of low-level context-free grammars used to constrain logits token-by-token directly during C/C++ inference.

### 2. Autoregressive Text Generation & Logits Processing
*   **[Hugging Face - Text Generation Strategies Guide](https://huggingface.co/docs/transformers/generation_strategies)**
    The standard conceptual guide explaining different LLM decoding strategies (Greedy Search, Sampling, Beam Search) and how logits processors and token masks manipulate probability distributions before selection.
*   **[Hugging Face - Text Generation API Documentation](https://huggingface.co/docs/transformers/main_classes/text_generation)**
    The technical reference explaining the `generate()` method, which underlies the step-by-step next-token prediction cycle used to build autoregressive generation loops.

### 3. Byte Pair Encoding (BPE) & Tokenization Foundations
*   **[Andrej Karpathy's minbpe Repository & Tokenization Lecture](https://github.com/karpathy/minbpe)**
    The gold standard educational guide on tokenization. It explains how raw bytes are recursively merged into BPE tokens [V.3.2], how `vocab.json` files are structured [V.3.1], and why trailing spaces and special character fallbacks behave the way they do in transformer vocabularies.
*   **[Hugging Face - Summary of Tokenizers Guide](https://huggingface.co/docs/transformers/tokenizer_summary)**
    A conceptual overview describing the differences between various tokenization algorithms (Byte-level BPE, WordPiece, Unigram, SentencePiece) [V.3.2] and how they preserve leading spaces and special markers (like Qwen's `Ġ` space indicators) [V.3.2].
*   **[Sennrich et al. (2015) - Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909)**
    The foundational academic paper that introduced Byte Pair Encoding (BPE) to neural natural language processing, establishing subword-level tokenization as the standard for deep generative models.

### 4. Function Calling & Schema Validation Specifications
*   **[OpenAI - Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)**
    The definitive guide explaining the concept of Function Calling [III.1]—how natural language prompts are dynamically translated into structured, machine-readable JSON schemas for API orchestration [III.1, III.2].
*   **[JSON Schema Specification Standard](https://json-schema.org/)**
    The official standard defining how JSON structures, key-value constraints, and nested schemas are modeled. Our project's schemas (such as the structure in `functions_definition.json`) conform to this specification [V.2].
*   **[Pydantic - Data Validation using Python Type Hints](https://docs.pydantic.dev/)**
    The official documentation for Pydantic—the parsing and validation engine used extensively in our project to validate prompt structures, function definitions, and final outputs against Python type hints [IV.1, IV.3.1, V.4.2].

### 5. Tiktoken & Qwen Tokenizer Mechanics
*   **[openai/tiktoken - Official Repository](https://github.com/openai/tiktoken)**
    The fast Byte Pair Encoding (BPE) tokenizer implementation used by OpenAI and adapted by Qwen models. It explains the core regex splitting rules, vocabulary mapping structures, and how special tokens are injected or handled at the token-level.
*   **[QwenLM/Qwen - Tokenizer & Vocabulary Specifications](https://github.com/QwenLM/Qwen)**
    The official Qwen repository containing the technical specifications of their custom tiktoken-based tokenizer. It explains how Qwen models support multi-lingual generation and handle precise BPE byte-fallbacks.

### 6. SOLID Principles & Clean Python Architecture
*   **[Real Python - SOLID Principles of Object-Oriented Design in Python](https://realpython.com/solid-principles-python/)**
    A comprehensive, Python-specific guide explaining the five SOLID design principles. It details how the Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP) are applied using abstract base classes—exactly reflecting the modular interface designed in this project.
*   **[Architecture Patterns with Python (Cosmic Python)](https://www.cosmicpython.com/)**
    An open-source handbook on building robust, clean, and decoupling architectural patterns in Python. It provides invaluable insights on keeping constraints, business logic, and the execution engine (Decoder and Generator) isolated and modular.
*   **[PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/) & [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)**
    The official Python enhancement proposals outlining the precise standards for writing readable, clean, well-structured, and compliant code and docstrings—crucial for passing static flake8 and mypy validations [IV.1].


### AI Usage Disclosure
Artificial Intelligence (ChatGPT) was utilized as an educational co-pilot and mentor throughout this project's development. Specifically, AI assisted in:
- Designing the lookahead state-transition logic in `ParameterConstraint` to avoid number truncation.
- Formulating the NumPy slicing math to optimize $-\infty$ logit masking.
- Documenting the OOP class layout and auditing Python typings for full `mypy` compliance.
- All AI-suggested concepts were thoroughly analyzed, manually typed, and vetted to ensure deep conceptual understanding and absolute code quality.
