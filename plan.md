# Plan

## Goals
- Replace manual front-matter parsing in `read_previous_balance` with the `python-frontmatter` library.
- Add tests for malformed front-matter scenarios.

## Constraints
- Keep dependencies minimal.
- Preserve existing balance file format and behavior.

## Risks
- Additional dependency may increase install time.
- Malformed files might still bypass parsing; ensure warnings cover these cases.

## Test Plan
- `pip install -r requirements-dev.txt`
- `pytest`

## SemVer Impact
- Patch release: internal parsing change with new tests.
