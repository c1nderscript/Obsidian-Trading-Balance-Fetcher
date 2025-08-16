# Plan

## Goals
- Add a "Deployment" section to the README with cron and systemd examples.
- Document environment variable setup for production hosts.

## Constraints
- Documentation only; no code changes.
- Use minimal, reversible examples.

## Risks
- Misconfigured environment files could expose credentials.
- Incorrect scheduling may lead to missed runs.

## Test Plan
- `pre-commit run --all-files`
- `pytest`
- `pip-audit -r requirements.lock`

## SemVer Impact
- No version change; docs only.

## Affected Packages
- obsidian-trading-balance-fetcher (documentation)

## Rollback
- Revert README, CHANGELOG, and plan updates.
