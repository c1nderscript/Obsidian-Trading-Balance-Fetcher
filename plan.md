# Plan

## Goals
- Build wheel and publish to PyPI on tagged releases via GitHub Actions.
- Document `pip install obsidian-trading-balance-fetcher` in README.

## Constraints
- Follow existing GitHub Actions style and keep changes minimal.
- Assume `PYPI_API_TOKEN` is configured as a repository secret.

## Risks
- Publishing fails if the secret is missing or invalid.
- Tagging without updating version or changelog produces incorrect releases.

## Test Plan
- `pre-commit run --all-files`
- `pytest`
- `pip-audit`

## SemVer Impact
- Patch release: 0.3.3

## Affected Packages
- obsidian-trading-balance-fetcher

## Rollback
- Revert workflow, docs, version, and changelog changes.
