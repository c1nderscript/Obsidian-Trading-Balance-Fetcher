# Plan

## Goals
- Add ruff and black configuration via `pyproject.toml`.
- Provide pre-commit hooks and GitHub Actions workflow to run linters and tests automatically.

## Constraints
- Use existing pip-based setup (`requirements-dev.txt`).
- Avoid external network calls during tests.

## Risks
- Ruff may surface lint errors requiring code adjustments.

## Test Plan
- `pip install -r requirements-dev.txt`
- `pre-commit run --all-files`
- `pytest`

## SemVer Impact
- Patch release: development tooling only.
