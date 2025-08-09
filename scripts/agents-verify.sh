set -euo pipefail
test -f AGENTS.md || { echo "AGENTS.md missing"; exit 1; }

# Example drift signals (customize per stack)
grep -q "build:" .github/workflows/* || true
if grep -q "pnpm" AGENTS.md && ! grep -Rq "pnpm" .; then
  echo "AGENTS.md mentions pnpm but repo doesn't use it."; exit 1
fi
# Extend: check languages, test commands, release steps, dockerfiles vs docs, etc.
echo "AGENTS.md passes basic drift check."
