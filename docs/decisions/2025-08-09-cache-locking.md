# Cache locking strategy

## Context
Concurrent runs could corrupt the JSON cache file.

## Decision
Use the `filelock` library with atomic temp-file writes to serialize access to the cache file.

## Consequences
- Prevents partial writes from concurrent processes.
- Introduces a small runtime dependency.
