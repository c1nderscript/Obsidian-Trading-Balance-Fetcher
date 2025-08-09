# Plan

## Goals
- Add integration test calling `start.main()` to verify balance logging, cache updates, and user-visible logging output.

## Constraints
- Use monkeypatched environment variables and CLI arguments.
- Avoid external network calls.

## Risks
- Test depends on current date; ensure paths use `datetime.today()` consistently.

## Test Plan
- `pip install -r requirements-dev.txt`
- `pytest`

## SemVer Impact
- Patch release: tests only, no runtime changes.
