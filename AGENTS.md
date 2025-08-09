# AGENTS

## Overview
- Language: Python
- Package manager: pip via `requirements*.txt`
- Entry point: `balancefetcher/start.py`
- Tests: `pytest`
- Versioning: `pyproject.toml` uses Semantic Versioning
- Changelog: `CHANGELOG.md` in Keep a Changelog format
- CI: GitHub Actions workflows in `.github/workflows`
- Release: tag `v<version>` on main; changelog and version must match

## Development
- Install deps: `pip install -r requirements-dev.txt`
- Run tests: `pytest`
- Update version in `pyproject.toml` and `CHANGELOG.md` for code changes
- Follow Conventional Commits
