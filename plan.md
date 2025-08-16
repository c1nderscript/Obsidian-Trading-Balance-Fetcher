# Plan

## Goals
- Generate release notes from `CHANGELOG.md` during the release workflow.

## Constraints
- Follow existing GitHub Actions style and keep changes minimal.
- Avoid persistent artifacts; release notes should be generated at runtime.

## Risks
- Release workflow fails if the changelog entry for the version is missing or misformatted.
- Incorrect parsing could produce empty release notes.

## Test Plan
- `pre-commit run --all-files`
- `pytest`
- `pip-audit`

## SemVer Impact
- Patch release: 0.3.2

## Affected Packages
- obsidian-trading-balance-fetcher

## Rollback
- Revert script, workflow, version, and changelog changes.
