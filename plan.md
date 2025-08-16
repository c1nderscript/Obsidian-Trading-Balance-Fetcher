# Plan

## Goals
- Add a dependency vulnerability audit to CI using `pip-audit`.

## Constraints
- Use existing GitHub Actions workflow style.
- Keep changes minimal and reversible.

## Risks
- CI failures due to transient advisory database issues.
- Increased runtime for CI jobs.

## Test Plan
- `pre-commit run --all-files`
- `pytest`
- `pip-audit`

## SemVer Impact
- Patch release: 0.3.1

## Affected Packages
- obsidian-trading-balance-fetcher

## Rollback
- Revert workflow, documentation, and version changes.
