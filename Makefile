# Makefile

SHELL := /bin/bash

# define the name of the virtual environment directory
VENV := .venv

# default target, when make executed without arguments
all: venv

# venv python 3
venv: 
	python3 -m venv $(VENV)
	( \
		source $(VENV)/bin/activate; \
		pip install -r requirements.txt; \
		deactivate; \
    )

run:
	./$(VENV)/bin/python3 main.py

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean
