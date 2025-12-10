# Labs Feature Engineering

## Prerequisites
- Python 3.13.x (recommended) and optionally `pyenv`.

## Setup virtual environment
```sh
pyenv install 3.11.9                # optional: install Python
pyenv local 3.11.9                  # set local version
python --version                    # verify
python -m venv .venv                # create venv
source .venv/Scripts/activate       # Windows
# or: source .venv/bin/activate     # Linux/Mac
```

## Install dependencies using poetry

```sh
pip install poetry          # Install poetry
poetry install
```

## Run tests and coverage

```sh
# Run tests
pytest

# Run test with coverage
pytest --cov=src --cov=tests --cov-report=term-missing
```
