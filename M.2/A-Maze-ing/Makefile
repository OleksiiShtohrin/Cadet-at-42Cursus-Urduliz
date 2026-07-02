# Makefile for A‑Maze‑ing project

PY = python3
VENV = .venv
PIP = $(VENV)/bin/pip
PYTEST = $(VENV)/bin/pytest

MAIN = a_maze_ing.py

.PHONY: install run debug clean lint lint-strict test

install:
	@echo "Creating virtualenv (if needed) and installing dev dependencies..."
	@test -d $(VENV) || $(PY) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PY) $(MAIN) config.txt

debug:
	$(PY) -m pdb $(MAIN) config.txt

test:
	$(PYTEST) -q

clean:
	@echo "Cleaning Python caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache build dist *.egg-info

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
