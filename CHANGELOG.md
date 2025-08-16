# Changelog
All notable changes to this project will be documented here.

## [Unreleased]

## [0.3.2] - 2025-08-16
### Changed
- Generate release notes from `CHANGELOG.md` during release.

## [0.3.1] - 2025-08-16
### Added
- Document cron and systemd deployment with environment variable setup.

### Security
- Run `pip-audit` in CI to fail on vulnerable dependencies.

## [0.3.0] - 2025-08-16
### Added
- Dockerfile exposing the `balancefetcher` console script.
- Documentation for building and running via Docker with optional `docker-compose` scheduling.

## [0.2.5] - 2025-08-16
### Changed
- Document all environment variables and optional settings in root `.env.example`.
- README now references the canonical `.env.example`.
### Removed
- Duplicate `.env.example` under `balancefetcher/`.

## [0.2.4] - 2025-08-16
### Changed
- Pin runtime dependencies and add `requirements.lock` for deterministic installs.
- Installation instructions now reference the lock file.

## [0.2.3] - 2025-08-09
### Added
- Ruff and Black linting via pre-commit and GitHub Actions workflow.

## [0.2.2] - 2025-08-09
### Added
- Integration test covering `start.main()` balance logging and cache behavior.

## [0.2.1] - 2025-08-09
### Changed
- Use `python-frontmatter` to parse vault front matter.
### Added
- Tests for malformed front matter scenarios.

## [0.2.0] - 2025-08-09
### Added
- Configurable cache file location via `BALANCE_CACHE_FILE` env var or `--cache-file` flag.
- Atomic cache writes with file locking to prevent concurrent corruption.

## [0.1.0] - 2025-08-09
### Added
- Initial release.
