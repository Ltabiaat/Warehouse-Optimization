PYTHON ?= python3
PYTHONPATH := src

.PHONY: help test test-verbose clean-pyc

help:
	@echo "Available targets:"
	@echo "  make test         - Run unit tests"
	@echo "  make test-verbose - Run unit tests with verbose output"
	@echo "  make clean-pyc    - Remove Python cache files"

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover -s tests

test-verbose:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover -s tests -v

clean-pyc:
	find src tests -type d -name '__pycache__' -prune -exec rm -rf {} +
