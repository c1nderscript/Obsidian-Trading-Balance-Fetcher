# 2025-08-16 Docker Support

## Status
Accepted

## Context
Running the balance fetcher in a container allows easier scheduling and deployment without managing host Python environments.

## Decision
Provide a `Dockerfile` that installs the project and exposes the `balancefetcher` console script. Supply a sample `docker-compose.yml` to execute the container daily.

## Consequences
- Simplifies distribution and scheduling via Docker.
- Requires maintaining container build instructions.
