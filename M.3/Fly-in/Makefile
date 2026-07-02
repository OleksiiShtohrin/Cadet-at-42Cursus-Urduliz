PYTHON = python3
VENV = .venv
PIP = $(VENV)/bin/pip
PYTEST = $(VENV)/bin/pytest
#MAP = maps/easy/01_linear_path.txt
#MAP = maps/easy/02_simple_fork.txt
#MAP = maps/easy/03_basic_capacity.txt
#MAP = maps/medium/01_dead_end.txt
#MAP = maps/medium/02_circular_loop.txt
#MAP = maps/medium/03_priority_puzzle.txt
#MAP = maps/hard/01_maze_nightmare.txt
#MAP = maps/hard/02_capacity_hell.txt
#MAP = maps/hard/03_ultimate_challenge.txt
MAP = maps/challenger/01_the_impossible_dream.txt

install:
	@echo "Creating virtualenv (if needed) and installing dev dependencies..."
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(PIP) install -U pip
	$(PIP) install flake8 mypy pytest pygame

run:
	$(PYTHON) main.py $(MAP)

run-visual:
	$(PYTHON) main.py $(MAP) --visual

run-pygame:
	$(PYTHON) main.py $(MAP) --pygame

debug:
	$(PYTHON) -m pdb main.py $(MAP)

test:
	$(PYTHON) -m pytest

clean:
	@echo "Cleaning Python caches..."
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run run-pygame run-visual debug test clean lint lint-strict