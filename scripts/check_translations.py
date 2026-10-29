"""Warn when a translated page is older than its English source.

Translated pages follow the MkDocs i18n suffix convention:
docs/<page>.<lang>.md is the translation of docs/<page>.md.
The last commit date of each file is read from Git history.

Usage: python scripts/check_translations.py [--strict]
  --strict  exit with code 1 when a translation is outdated (default: warn only)
"""

import pathlib
import subprocess
import sys

DOCS_DIR = pathlib.Path("docs")
LANGUAGES = ("fr", "es")


def last_commit_time(path: pathlib.Path) -> int | None:
    """Return the Unix timestamp of the last commit touching path, or None."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ct", "--", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    value = result.stdout.strip()
    return int(value) if value else None


def find_outdated() -> list[tuple[pathlib.Path, pathlib.Path]]:
    """Return (translation, source) pairs where the source is more recent."""
    outdated = []
    for lang in LANGUAGES:
        for translation in sorted(DOCS_DIR.rglob(f"*.{lang}.md")):
            source = translation.with_name(translation.name.replace(f".{lang}.md", ".md"))
            if not source.exists():
                print(f"::warning file={translation}::No English source found for {translation}")
                continue
            source_time = last_commit_time(source)
            translation_time = last_commit_time(translation)
            if source_time is None or translation_time is None:
                continue
            if source_time > translation_time:
                outdated.append((translation, source))
    return outdated


def main() -> int:
    strict = "--strict" in sys.argv[1:]
    outdated = find_outdated()
    for translation, source in outdated:
        print(f"::warning file={translation}::{translation} is older than {source}; update the translation.")
    if not outdated:
        print("All translations are up to date.")
    return 1 if strict and outdated else 0


if __name__ == "__main__":
    sys.exit(main())
