# Plan

## Goals
- Pin runtime dependencies in `requirements.txt`.
- Generate a deterministic lock file `requirements.lock`.
- Update installation docs to reference the lock file.

## Constraints
- Use pip and `pip-tools` within the existing `requirements*.txt` workflow.
- Preserve current development setup via `requirements-dev.txt`.

## Risks
- Locked versions may become outdated and need periodic refresh.
- Transitive dependencies resolved by `pip-compile` could introduce conflicts.

## Test Plan
- `pip install -r requirements-dev.txt`
- `pre-commit run --all-files`
- `pytest`
- `pip-audit -r requirements.lock`

## SemVer Impact
- Patch release: dependency pinning and documentation only.

