#!/usr/bin/env python3
"""Generate release notes for the given version from CHANGELOG.md."""
import re
import sys
from pathlib import Path


def extract_section(text: str, version: str) -> str:
    pattern = rf"(## \[{re.escape(version)}\].*?)(?=\n## \[|\Z)"
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        raise SystemExit(f"Version {version} not found in changelog")
    return match.group(1).strip() + "\n"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: generate_release_notes.py <version> [output]")
        raise SystemExit(1)
    version = sys.argv[1]
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("RELEASE_NOTES.md")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    section = extract_section(changelog, version)
    output.write_text(section, encoding="utf-8")
    print(f"Wrote release notes for {version} to {output}")


if __name__ == "__main__":
    main()
