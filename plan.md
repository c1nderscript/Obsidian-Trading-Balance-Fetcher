# Plan

## Goals
- Allow cache location configuration via env var `BALANCE_CACHE_FILE` and CLI flag `--cache-file`.
- Prevent cache corruption by using atomic writes with file locking.
- Scaffold repository release and documentation infrastructure (CHANGELOG, CI, AGENTS).

## Constraints
- Maintain compatibility with existing behavior; default cache path remains `~/.kucoin_balance_log.json`.
- Use lightweight dependencies only.

## Risks
- Concurrent access may still fail if lock not released; ensure file locking handles contention.
- Environment variables may override CLI unintentionally; CLI should take precedence.

## Test Plan
- Unit tests for `mark_logged` concurrent access.
- Tests for environment variable and CLI cache path overrides.
- Run `pytest`.

## SemVer Impact
- Minor release: adds backwards-compatible features.
