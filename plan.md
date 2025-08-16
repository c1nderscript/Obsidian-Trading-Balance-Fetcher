# Plan

## Goals
- Remove duplicate `.env.example` files and keep canonical copy at repository root.
- Ensure root `.env.example` documents required and optional environment variables.
- Update README and any docs to reference the root `.env.example`.

## Constraints
- Maintain existing development workflow and tooling.
- Keep changes minimal and reversible.

## Risks
- Missing environment variable descriptions could confuse users.
- Stale references to removed file might persist in docs.

## Test Plan
- `pip install -r requirements-dev.txt`
- `pre-commit run --all-files`
- `pytest`
- `pip-audit -r requirements.lock`

## SemVer Impact
- Patch release: documentation and configuration cleanup.

## Rollback
- Restore removed `.env.example` and revert documentation changes.
