# Plan

## Goals
- Incorporate Syft to generate SBOM for the built wheel in the release workflow.
- Attach the generated SBOM to GitHub Releases.

## Constraints
- Follow repository instructions in `AGENTS.md`.
- Keep changes minimal and reversible.
- Preserve existing release workflow behavior.

## Risks
- Syft installation or execution may fail, breaking the release process.
- Uploading assets requires the release to exist.

## Test Plan
- `pre-commit run --all-files`
- `pytest`
- `pip-audit`

## SemVer Impact
- No version change (CI-only).

## Affected Packages
- `obsidian-trading-balance-fetcher`

## Rollback
- Revert the commit.
