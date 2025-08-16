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
- Docker: `Dockerfile` installs the project and runs the `balancefetcher` console script

## Development
- Install deps: `pip install -r requirements-dev.txt`
- Run linters: `pre-commit run --all-files`
- Run tests: `pytest`
- Audit dependencies: `pip-audit`
- Update version in `pyproject.toml` and `CHANGELOG.md` for code changes
- Follow Conventional Commits
- Build container: `docker build -t balancefetcher .`
