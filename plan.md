# Plan

## Goals
- Add a pytest case asserting `load_config()` exits with `SystemExit` when required environment variables are missing and lists all missing variables.

## Constraints
- Follow repository instructions in `AGENTS.md`.
- Keep changes minimal and reversible.

## Risks
- Environment variable cleanup may affect other tests if not isolated.

## Test Plan
- `pre-commit run --all-files`
- `pytest`
- `pip-audit`

## SemVer Impact
- Patch release: 0.3.4

## Affected Packages
- obsidian-trading-balance-fetcher

## Rollback
- Revert the commit.
