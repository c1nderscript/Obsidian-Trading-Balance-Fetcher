# Plan

## Goals
- Add a `Dockerfile` that installs the package and runs the `balancefetcher` console script.
- Document Docker build/run instructions in `README.md`.
- Provide a sample `docker-compose.yml` for daily execution.

## Constraints
- Preserve the existing Python-based workflow and dependency management.
- Keep changes minimal and reversible.

## Risks
- Misconfigured volumes or env vars could prevent balance files from being written.
- Docker image size may grow if dependencies are not pruned.

## Test Plan
- `pip install -r requirements-dev.txt`
- `pre-commit run --all-files`
- `pytest`
- `pip-audit -r requirements.lock`
- `docker build -t balancefetcher .`

## SemVer Impact
- Minor release: new Docker packaging is a backwards-compatible feature.

## Affected Packages
- obsidian-trading-balance-fetcher

## Rollback
- Remove `Dockerfile` and `docker-compose.yml`.
- Revert documentation, version, and changelog updates.
