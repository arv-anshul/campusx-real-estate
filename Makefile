.ONESHELL:
SHELL := /bin/bash

# Get package name from pwd
PACKAGE_NAME := $(shell pwd)  # works for (mac | linux)
.DEFAULT_GOAL := help

# UPDATE ME
PYTHON_VENV = .venv
STREAMLIT_APP = Real_Estate_Project.py
MAX_LINE_LENGTH = 88  # Variable for formatters

define PRINT_HELP_PYSCRIPT
import re, sys

class Style:
    BLACK = '\033[30m'
    BLUE = '\033[34m'
    BOLD = '\033[1m'
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    MAGENTA = '\033[35m'
    RED = '\033[31m'
    WHITE = '\033[37m'
    YELLOW = '\033[33m'
    ENDC = '\033[0m'

print(f"{Style.BOLD}Please use `make <target>` where <target> is one of{Style.ENDC}")
for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if line.startswith("# -------"):
		print(f"\n{Style.RED}{line}{Style.ENDC}")
	if match:
		target, help_msg = match.groups()
		if not target.startswith('--'):
			print(f"{Style.BOLD+Style.GREEN}{target:20}{Style.ENDC} - {help_msg}")
endef

export PRINT_HELP_PYSCRIPT


# If you want a specific Python interpreter define it as an envvar
# $ export PYTHON_ENV=
ifdef PYTHON_ENV
	PYTHON := $(PYTHON_ENV)
else
	PYTHON := python3
endif

help:
	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

# -------------------------------- Builds and Installations -----------------------------

bootstrap: clean gitignore install-hooks venv ## Installs development packages, hooks, create venv

gitignore:  ## Create .gitignore file for pyhton project
	curl -sL https://www.gitignore.io/api/venv,python,JupyterNotebooks,VisualStudioCode >> .gitignore

venv:  ## Create a new virtual environment, with default name '.venv'.
	@$(PYTHON) -m venv "$(PYTHON_VENV)" || (echo "Failed to create virtual environment" && exit 1); \
	echo >&2 "Created venv in '$(PYTHON_VENV)'"; \
	echo -e "Activate your env with the command:"; \
	echo -e "\033[1;32m$$\033[0m \033[31msource $(PYTHON_VENV)/bin/activate\033[0m"; \

# -------------------------------------- Project Execution -------------------------------

streamlit: $(STREAMLIT_APP)  ## Run streamlit app (First define the STREAMLIT_APP variable in Makefile)
	@streamlit run $<

# -------------------------------------- Clean Up  --------------------------------------
.PHONY: clean
clean: clean-build clean-pyc clean-test ## Remove all build, test, coverage and Python artefacts

clean-venv: $(PYTHON_VENV)
	rm -rf .venv

clean-build: ## Remove build artefacts
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -rf {} +
	find . -name '*.xml' -exec rm -rf {} +


clean-pyc: ## Remove Python file artefacts
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm -rf {} +
	find . -name '*~' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean-test: ## Remove test and coverage artefacts
	rm -rf .venv
	rm -rf .tox/
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache

# -------------------------------------- Code Style  -------------------------------------

lint: ## Check style with `flake8` and `mypy`
	@$(PYTHON) -m flake8 --max-line-length $(MAX_LINE_LENGTH) $(PACKAGE_NAME)
	$(PYTHON) -m mypy

formatter: ## Format style with `black` and sort imports with `isort`
	@isort . -m 3 --profile black -l $(MAX_LINE_LENGTH)
	black . -l $(MAX_LINE_LENGTH)

# ---------------------------------- Git Hooks ------------------------------------------

install-hooks: .configs/.pre-commit-config.yaml  ## Install `pre-commit-hooks` on local directory [see: https://pre-commit.com]
	$(PYTHON) -m pip install pre-commit
	pre-commit install --install-hooks -c .configs/.pre-commit-config.yaml

pre-commit-all: ## Run `pre-commit` on all files
	pre-commit run --all-files -c .configs/.pre-commit-config.yaml

pre-commit: ## Run `pre-commit` on staged files
	pre-commit run -c .configs/.pre-commit-config.yaml
