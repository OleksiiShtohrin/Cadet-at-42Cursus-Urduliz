# **************************************************************************** #
#                                Call Me Maybe                                #
# **************************************************************************** #

.PHONY: all install run debug lint lint-strict clean help

all: run

help:
	@echo ""
	@echo "Available commands:"
	@echo "  make install      Install project dependencies"
	@echo "  make run          Run the project"
	@echo "  make debug        Run with pdb"
	@echo "  make lint         Run flake8 and mypy"
	@echo "  make lint-strict  Run strict mypy"
	@echo "  make clean        Remove temporary files"
	@echo ""

install:
	@echo "Installing dependencies..."
	uv sync --group dev

run:
	uv run python -m src

debug:
	uv run python -m pdb -m src

lint:
	uv run flake8 src
	uv run mypy src \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs 

lint-strict:
	uv run flake8 src
	uv run mypy src --strict

clean:
	@echo "Cleaning project..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Done."
