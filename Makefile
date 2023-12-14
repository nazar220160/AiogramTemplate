VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
SRC_DIR := src
REQUIREMENTS := requirements.txt

.PHONY: install
install: $(VENV)/bin/activate ## Install dependencies into virtual environment

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install -r $(REQUIREMENTS)
	@echo "Virtual environment is now activated. Run 'source $(VENV)/bin/activate' to enter the environment."
