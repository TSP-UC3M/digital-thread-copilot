"""Generate docs/quality.md: source code quality metrics computed by local tools.

Metrics (plan step F3): test coverage, lint findings, cyclomatic complexity, duplication.

    python scripts/dev.py unit           writes coverage.xml
    python scripts/quality_report.py     writes docs/quality.md

Run it from the repository root. Coverage is read from coverage.xml; without that
file the page says "not measured" instead of failing. Lint findings come from ruff,
complexity from radon, and duplication is computed here (see duplication()).
"""

import datetime
import json
import pathlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ElementTree

CODE_DIRS = ("src", "tests", "scripts")
COMPLEXITY_DIRS = ("src", "scripts")
WINDOW = 6  # consecutive code lines that must repeat to count as duplicated
COMPLEXITY_LIMIT = 10  # blocks above this value are listed (McCabe's usual threshold)
OUTPUT = pathlib.Path("docs/quality.md")


def run(command: list[str]) -> str:
    """Return the standard output of a command; empty string when the tool is missing."""
    try:
        return subprocess.run(command, capture_output=True, text=True, check=False).stdout
    except OSError:
        return ""


def code_lines(text: str) -> list[str]:
    """Return the lines of a Python source without blank lines and comment-only lines."""
    lines = (line.strip() for line in text.splitlines())
    return [line for line in lines if line and not line.startswith("#")]


def duplication(sources: dict[str, str], window: int = WINDOW) -> tuple[int, int]:
    """Return (duplicated lines, total lines) over the given sources.

    A line is duplicated when it belongs to a run of `window` consecutive code lines
    that occurs at least twice, in the same file or in two files. Blank lines and
    comment-only lines are ignored and the indentation is removed before comparing.
    """
    lines_of = {name: code_lines(text) for name, text in sources.items()}
    seen: dict[tuple[str, ...], list[tuple[str, int]]] = {}
    for name, lines in lines_of.items():
        for start in range(len(lines) - window + 1):
            seen.setdefault(tuple(lines[start : start + window]), []).append((name, start))
    duplicated: set[tuple[str, int]] = set()
    for places in seen.values():
        if len(places) > 1:
            for name, start in places:
                duplicated.update((name, start + offset) for offset in range(window))
    return len(duplicated), sum(len(lines) for lines in lines_of.values())


def read_coverage(path: pathlib.Path) -> dict | None:
    """Return the totals and the per-file rates of a Cobertura coverage.xml, or None."""
    if not path.exists():
        return None
    root = ElementTree.parse(path).getroot()
    files = {node.get("filename", "?"): float(node.get("line-rate", "0")) for node in root.iter("class")}
    return {
        "line_rate": float(root.get("line-rate", "0")),
        "branch_rate": float(root.get("branch-rate", "0")),
        "lines_valid": int(root.get("lines-valid", "0")),
        "lines_covered": int(root.get("lines-covered", "0")),
        "files": files,
    }


def coverage_threshold() -> str:
    """Return the fail_under value of pyproject.toml, or "not set"."""
    path = pathlib.Path("pyproject.toml")
    match = re.search(r"^fail_under\s*=\s*(\d+)", path.read_text(encoding="utf-8"), re.M) if path.exists() else None
    return f"{match.group(1)} %" if match else "not set"


def lint_findings(dirs: list[str]) -> dict[str, int] | None:
    """Return the number of ruff findings per rule code, or None when ruff did not run."""
    output = run([sys.executable, "-m", "ruff", "check", *dirs, "--output-format", "json", "--exit-zero"])
    try:
        findings = json.loads(output)
    except json.JSONDecodeError:
        return None
    counts: dict[str, int] = {}
    for finding in findings:
        code = finding.get("code") or "syntax"
        counts[code] = counts.get(code, 0) + 1
    return counts


def complexity(dirs: list[str]) -> list[tuple[str, str, int]] | None:
    """Return (file, block, cyclomatic complexity) for every block, or None when radon did not run."""
    output = run([sys.executable, "-m", "radon", "cc", "-j", *dirs])
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return None
    blocks = []
    for name, entries in data.items():
        if isinstance(entries, list):
            blocks.extend((name.replace("\\", "/"), entry["name"], int(entry["complexity"])) for entry in entries)
    return blocks


def percent(rate: float) -> str:
    return f"{100 * rate:.1f} %"


def table(header: list[str], rows: list[list[str]], empty: str) -> list[str]:
    """Return a Markdown table, or the sentence `empty` when there is no row."""
    if not rows:
        return [empty]
    lines = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    return lines + ["| " + " | ".join(row) + " |" for row in rows]


def coverage_rows(cov: dict | None) -> list[list[str]]:
    if cov is None:
        return [["Coverage of the unit tests", "not measured (no `coverage.xml`)", "Run `python scripts/dev.py unit`"]]
    lines = f"{percent(cov['line_rate'])} ({cov['lines_covered']} of {cov['lines_valid']} lines)"
    return [
        ["Line coverage of the unit tests", lines, f"Threshold: {coverage_threshold()}"],
        ["Branch coverage of the unit tests", percent(cov["branch_rate"]), "Reported, no threshold"],
    ]


def complexity_row(blocks: list[tuple[str, str, int]] | None) -> list[str]:
    name = "Cyclomatic complexity (radon)"
    if blocks is None:
        return [name, "not measured (radon did not run)", ""]
    if not blocks:
        return [name, "no function or class found", ""]
    values = [value for _, _, value in blocks]
    above = sum(value > COMPLEXITY_LIMIT for value in values)
    value = f"mean {sum(values) / len(values):.1f}, maximum {max(values)}, over {len(values)} blocks"
    return [name, value, f"{above} block(s) above {COMPLEXITY_LIMIT}"]


def build_page() -> str:
    dirs = [name for name in CODE_DIRS if pathlib.Path(name).is_dir()]
    sources = {
        path.as_posix(): path.read_text(encoding="utf-8")
        for name in dirs
        for path in sorted(pathlib.Path(name).rglob("*.py"))
    }
    commit = run(["git", "rev-parse", "--short", "HEAD"]).strip() or "unknown"
    commit_date = run(["git", "log", "-1", "--format=%cI"]).strip() or "unknown"
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    cov = read_coverage(pathlib.Path("coverage.xml"))
    lint = lint_findings(dirs)
    blocks = complexity([name for name in COMPLEXITY_DIRS if pathlib.Path(name).is_dir()])
    duplicated, total = duplication(sources)
    not_measured = "Not measured."

    lint_value = "not measured (ruff did not run)" if lint is None else str(sum(lint.values()))
    duplication_value = f"{percent(duplicated / total if total else 0.0)} ({duplicated} of {total} lines)"
    summary = [
        *coverage_rows(cov),
        ["Lint findings (ruff)", lint_value, "Expected: 0, the lint job blocks the merge"],
        complexity_row(blocks),
        ["Duplicated code lines", duplication_value, f"Runs of {WINDOW} identical code lines"],
    ]
    per_file = [[f"`{name}`", percent(value)] for name, value in sorted((cov or {}).get("files", {}).items())]
    per_rule = [[f"`{code}`", str(count)] for code, count in sorted((lint or {}).items())]
    high = sorted((block for block in blocks or [] if block[2] > COMPLEXITY_LIMIT), key=lambda block: -block[2])
    high_rows = [[f"`{name}`", f"`{block}`", str(value)] for name, block, value in high]
    method = [
        ["Coverage", "`coverage.py` through `pytest-cov`, unit tests only, read from `coverage.xml`"],
        ["Lint findings", "`ruff check` with the rules selected in `pyproject.toml`"],
        [
            "Cyclomatic complexity",
            "`radon cc` on `src/` and `scripts/`: McCabe's number per function, method and class",
        ],
        [
            "Duplication",
            f"Computed by the script: share of code lines that belong to a run of {WINDOW} consecutive lines found "
            "at least twice; blank lines, comment-only lines and indentation are ignored",
        ],
    ]
    out = [
        "# Code quality",
        "",
        "This page is generated by `scripts/quality_report.py`; do not edit it by hand. Continuous integration",
        "regenerates it before each publication of the site.",
        "",
        f"- Generated: {now}",
        f"- Commit: `{commit}` (committed {commit_date})",
        f"- Python files analysed: {len(sources)} in {', '.join(f'`{name}/`' for name in dirs) or 'no folder'}",
        "",
        "## Summary",
        "",
        *table(["Metric", "Value", "Reference"], summary, not_measured),
        "",
        "## Coverage per file",
        "",
        *table(["File", "Line coverage"], per_file, not_measured),
        "",
        "## Lint findings per rule",
        "",
        *table(["Rule", "Findings"], per_rule, not_measured if lint is None else "No finding."),
        "",
        f"## Blocks with a cyclomatic complexity above {COMPLEXITY_LIMIT}",
        "",
        *table(["File", "Block", "Complexity"], high_rows, not_measured if blocks is None else "None."),
        "",
        "## How the metrics are computed",
        "",
        *table(["Metric", "Tool and definition"], method, not_measured),
        "",
    ]
    return "\n".join(out)


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_page(), encoding="utf-8", newline="\n")
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
