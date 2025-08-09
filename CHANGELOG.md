# Changelog
All notable changes to this project will be documented here.

## [Unreleased]

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
