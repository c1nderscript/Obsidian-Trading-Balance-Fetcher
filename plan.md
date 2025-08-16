# Plan

## Goals
- Add `LOG_LEVEL` environment variable defaulting to `INFO`.
- Modify `setup_logging()` to respect `LOG_LEVEL`.
- Document `LOG_LEVEL` in `.env.example` and `README`.

## Constraints
- Follow repository instructions in `AGENTS.md`.
- Keep changes minimal and reversible.

## Risks
- Invalid log level values could cause confusion.

## Test Plan
- `pre-commit run --all-files`
- `pytest`
- `pip-audit`

## SemVer Impact
- Minor release: `0.4.0`

## Affected Packages
- `obsidian-trading-balance-fetcher`

## Rollback
- Revert the commit.
