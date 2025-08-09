# Use python-frontmatter for vault parsing

## Context
Manual string splitting in `read_previous_balance` was brittle and missed malformed front-matter edge cases.

## Decision
Adopt the `python-frontmatter` library to parse YAML front matter reliably.

## Consequences
- Adds a new runtime dependency.
- Simplifies parsing logic and centralizes YAML handling.
- Enables detection of malformed or missing front matter.
