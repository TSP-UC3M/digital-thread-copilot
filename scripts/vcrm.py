"""Generate the verification matrix (VCRM) from the requirements and the test evidence (plan step F7).

    python scripts/vcrm.py                       write reports/vcrm.md and reports/vcrm.csv
    python scripts/vcrm.py --summary FILE        also append the Markdown matrix to FILE ($GITHUB_STEP_SUMMARY in CI)
    python scripts/vcrm.py --fail-on coverage    stricter exit rule, see below

Inputs: the requirements baseline (requirements/requirements.yaml, plan step C1) and the evidence file written by
`pytest --req-evidence=reports/evidence.json` (tests/conftest.py). Columns follow the four blocks of the course
matrix (matriz_vcrm_is_ejemplo.xlsx): identification and traceability, verification strategy, planning and
criteria, closure and evidence. Validation activities are listed apart: verifying is not validating.

Status of a requirement whose method is test, computed from the tests that carry its identifier:
    Passed        at least one test, all passed
    Failed        at least one test failed
    In progress   no test failed, at least one was skipped
    No evidence   no test carries its identifier
Status of the other methods (analysis, inspection, demonstration) and of validation activities: written by a
member in the baseline (verification.status: pending | in_progress | passed | failed); passed or failed needs
verification.evidence (the report, review or pull request that proves it).

Exit code 1 when the rule chosen with --fail-on is broken:
    consistency (default)  unreadable baseline, duplicate identifier, test citing an unknown identifier,
                           status passed or failed without evidence, any requirement Failed (a validation
                           activity marked failed, such as a rejected hypothesis, is reported, not an error)
    coverage               consistency, and every must requirement verified by test has at least one test
    complete               consistency, and every must requirement is Passed (final verification, step J3)
Without a baseline in the repository the matrix only lists the evidence, and the exit code is 0.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
METHODS = {
    "test": "Test (T)",
    "analysis": "Analysis (A)",
    "inspection": "Inspection (I)",
    "demonstration": "Demonstration (D)",
}
MANUAL = {"pending": "Pending", "in_progress": "In progress", "passed": "Passed", "failed": "Failed"}
STATUSES = ("Passed", "In progress", "Pending", "No evidence", "Failed")
LEVELS = ("consistency", "coverage", "complete")
COLUMNS = (
    "ID",
    "Subsystem",
    "Requirement",
    "Parent",
    "Method",
    "Status",
    "Lifecycle phase",
    "Acceptance criterion",
    "Plan / procedure",
    "Environment",
    "Evidence",
    "Observations",
)


@dataclass
class Row:
    """One line of the matrix: a requirement or a validation activity."""

    values: dict[str, str]
    priority: str = ""
    tests: dict[str, str] = field(default_factory=dict)

    @property
    def status(self) -> str:
        return self.values["Status"]


@dataclass
class Matrix:
    requirements: list[Row]
    validation: list[Row]
    removed: list[str]
    unlinked_tests: list[str]
    unknown: dict[str, list[str]]
    errors: list[str]
    baseline_found: bool
    tests_total: int = 0


def ci_run() -> tuple[str, str]:
    """Environment and evidence link of the current run (GitHub Actions or local)."""
    python = f"Python {platform.python_version()}"
    if os.environ.get("GITHUB_RUN_ID"):
        runner = os.environ.get("RUNNER_OS", "runner")
        url = "{}/{}/actions/runs/{}".format(
            os.environ.get("GITHUB_SERVER_URL", "https://github.com"),
            os.environ.get("GITHUB_REPOSITORY", ""),
            os.environ["GITHUB_RUN_ID"],
        )
        return f"GitHub Actions, {runner}, {python}", f"[CI run {os.environ['GITHUB_RUN_ID']}]({url})"
    return f"Local run, {platform.system()}, {python}", "Local run (reports/evidence.json)"


def test_status(tests: dict[str, str]) -> str:
    if not tests:
        return "No evidence"
    outcomes = set(tests.values())
    if "failed" in outcomes:
        return "Failed"
    if outcomes == {"passed"}:
        return "Passed"
    return "In progress"


def manual_status(entry: dict, where: str, errors: list[str]) -> str:
    raw = entry.get("status", "pending")
    if raw not in MANUAL:
        errors.append(f"{where}: unknown status '{raw}' (expected one of {', '.join(MANUAL)})")
        return "Pending"
    if raw in ("passed", "failed") and not str(entry.get("evidence", "")).strip():
        errors.append(f"{where}: status '{raw}' without evidence")
    return MANUAL[raw]


def joined(value) -> str:
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return "" if value is None else str(value)


def build(baseline: dict | None, evidence: dict[str, dict]) -> Matrix:
    environment, run_link = ci_run()
    errors: list[str] = []
    rows: list[Row] = []
    removed: list[str] = []
    known: set[str] = set()
    entries = (baseline or {}).get("requirements") or []
    if baseline is not None and not isinstance(entries, list):
        errors.append("baseline: 'requirements' is not a list")
        entries = []

    for index, req in enumerate(entries):
        rid = str(req.get("id", "")).strip() if isinstance(req, dict) else ""
        if not rid:
            errors.append(f"requirement number {index + 1}: no identifier")
            continue
        if rid in known:
            errors.append(f"{rid}: duplicate identifier")
        known.add(rid)
        if req.get("status") == "removed":
            removed.append(rid)
            continue
        ver = req.get("verification") or {}
        method = ver.get("method", "")
        if method not in METHODS:
            errors.append(f"{rid}: unknown verification method '{method}'")
        tests = {node: ev["outcome"] for node, ev in evidence.items() if rid in ev.get("requirements", [])}
        if method == "test":
            status = test_status(tests)
            passed = sum(outcome == "passed" for outcome in tests.values())
            procedure = f"{len(tests)} test(s): {passed} passed" if tests else joined(req.get("plan_steps"))
            env, proof = (environment, run_link) if tests else (ver.get("environment", ""), "")
            phase = ver.get("phase", "Integration (CI)")
        else:
            status = manual_status(ver, rid, errors)
            procedure = ver.get("procedure") or joined(req.get("plan_steps"))
            env, proof = ver.get("environment", ""), ver.get("evidence", "")
            phase = ver.get("phase", "To plan")
        values = {
            "ID": rid,
            "Subsystem": req.get("module", ""),
            "Requirement": req.get("text", ""),
            "Parent": joined(req.get("parent") or req.get("traces_to")),
            "Method": METHODS.get(method, method),
            "Status": status,
            "Lifecycle phase": phase,
            "Acceptance criterion": ver.get("criterion", ""),
            "Plan / procedure": procedure,
            "Environment": env,
            "Evidence": proof,
            "Observations": ver.get("observations", ""),
        }
        rows.append(Row(values=values, priority=str(req.get("priority", "")), tests=tests))

    validation: list[Row] = []
    for act in (baseline or {}).get("validation_activities") or []:
        aid = str(act.get("id", "")).strip()
        if not aid:
            errors.append("validation activity without identifier")
            continue
        if aid in known:
            errors.append(f"{aid}: duplicate identifier")
        known.add(aid)
        method = act.get("method", "")
        if method not in METHODS:
            errors.append(f"{aid}: unknown validation method '{method}'")
        values = {
            "ID": aid,
            "Subsystem": "Validation",
            "Requirement": act.get("need", ""),
            "Parent": joined(act.get("traces_to")),
            "Method": METHODS.get(method, method),
            "Status": manual_status(act, aid, errors),
            "Lifecycle phase": act.get("phase", "Validation"),
            "Acceptance criterion": act.get("criterion", ""),
            "Plan / procedure": act.get("activity", "")
            + (f" ({joined(act.get('plan_steps'))})" if act.get("plan_steps") else ""),
            "Environment": act.get("environment", ""),
            "Evidence": act.get("evidence", ""),
            "Observations": act.get("observations", ""),
        }
        validation.append(Row(values=values))

    unknown: dict[str, list[str]] = {}
    unlinked: list[str] = []
    for node, ev in sorted(evidence.items()):
        ids = ev.get("requirements", [])
        if not ids:
            unlinked.append(node)
        for rid in ids:
            if baseline is not None and (rid not in known or rid in removed):
                unknown.setdefault(rid, []).append(node)
    for rid, nodes in unknown.items():
        errors.append(f"{rid}: cited by {len(nodes)} test(s) but not an active requirement of the baseline")
    # A failed validation activity (for example a rejected hypothesis) is a result to report, not a defect.
    for row in rows:
        if row.status == "Failed":
            errors.append(f"{row.values['ID']}: Failed")
    return Matrix(rows, validation, removed, unlinked, unknown, errors, baseline is not None, len(evidence))


def violations(matrix: Matrix, level: str) -> list[str]:
    found = list(matrix.errors)
    musts = [row for row in matrix.requirements if row.priority == "M"]
    if level in ("coverage", "complete"):
        found += [
            f"{r.values['ID']}: must requirement verified by test has no test"
            for r in musts
            if r.values["Method"] == METHODS["test"] and not r.tests
        ]
    if level == "complete":
        found += [f"{r.values['ID']}: must requirement not Passed ({r.status})" for r in musts if r.status != "Passed"]
    return found


def cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def to_markdown(matrix: Matrix, level: str) -> str:
    lines = ["## Verification matrix (VCRM)", ""]
    if not matrix.baseline_found:
        lines += [
            "No requirements baseline in the repository yet (`requirements/requirements.yaml`, plan step C1).",
            f"Tests run: {matrix.tests_total}, of which {matrix.tests_total - len(matrix.unlinked_tests)} "
            "carry a requirement identifier. The matrix is filled when the baseline is added.",
            "",
        ]
        return "\n".join(lines) + "\n"
    rows = matrix.requirements
    counts = {s: sum(r.status == s for r in rows) for s in STATUSES}
    share = f"{100 * counts['Passed'] / len(rows):.0f} %" if rows else "n/a"
    lines += [
        "| Requirements | Passed | In progress | Pending | No evidence | Failed | Compliance |",
        "|---:|---:|---:|---:|---:|---:|---:|",
        f"| {len(rows)} | {counts['Passed']} | {counts['In progress']} | {counts['Pending']} "
        f"| {counts['No evidence']} | {counts['Failed']} | {share} |",
        "",
        f"Removed requirements, not listed: {len(matrix.removed)}. Exit rule: `{level}`.",
        "",
        "| ID | Parent | Method | Tests (passed/total) | Status | Acceptance criterion |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        v = r.values
        tests = (
            f"{sum(o == 'passed' for o in r.tests.values())}/{len(r.tests)}"
            if v["Method"] == METHODS["test"]
            else "n/a"
        )
        status = f"**{v['Status']}**" if v["Status"] in ("Failed", "No evidence") else v["Status"]
        criterion = cell(v["Acceptance criterion"])
        lines.append(f"| {v['ID']} | {cell(v['Parent'])} | {v['Method']} | {tests} | {status} | {criterion} |")
    if matrix.validation:
        lines += [
            "",
            "### Validation activities",
            "",
            "Validation checks the need (the hypothesis, the users), not the specification.",
            "",
            "| ID | Need | Method | Acceptance criterion | Status | Evidence |",
            "|---|---|---|---|---|---|",
        ]
        for r in matrix.validation:
            v = r.values
            lines.append(
                f"| {v['ID']} | {cell(v['Requirement'])} | {v['Method']} | {cell(v['Acceptance criterion'])} "
                f"| {v['Status']} | {cell(v['Evidence'])} |"
            )
    lines += [
        "",
        "<details><summary>Full matrix (12 columns of the course template)</summary>",
        "",
        "| " + " | ".join(COLUMNS) + " |",
        "|" + "---|" * len(COLUMNS),
    ]
    lines += ["| " + " | ".join(cell(r.values[c]) for c in COLUMNS) + " |" for r in rows + matrix.validation]
    lines += ["", "</details>"]
    failing = [f"- `{node}` ({r.values['ID']})" for r in rows for node, o in r.tests.items() if o == "failed"]
    if failing:
        lines += ["", "### Failing tests", "", *failing]
    if matrix.unknown:
        lines += ["", "### Tests citing an unknown or removed requirement", ""]
        lines += [f"- `{node}` cites {rid}" for rid, nodes in matrix.unknown.items() for node in nodes]
    lines += ["", f"Tests not linked to any requirement: {len(matrix.unlinked_tests)}."]
    return "\n".join(lines) + "\n"


def write_csv(matrix: Matrix, path: Path) -> None:
    # utf-8-sig so that spreadsheet programs read the accents; one row per requirement or activity.
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for row in matrix.requirements + matrix.validation:
            writer.writerow(row.values)


def load(path: Path) -> dict | None:
    if not path.exists():
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping at the top level")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--requirements", type=Path, default=ROOT / "requirements" / "requirements.yaml")
    parser.add_argument("--evidence", type=Path, default=ROOT / "reports" / "evidence.json")
    parser.add_argument("--out", type=Path, default=ROOT / "reports", help="folder of vcrm.md and vcrm.csv")
    parser.add_argument("--summary", type=Path, help="append the Markdown matrix to this file")
    parser.add_argument("--fail-on", choices=LEVELS, default="consistency")
    args = parser.parse_args(argv)

    try:
        baseline = load(args.requirements)
    except (ValueError, yaml.YAMLError) as error:
        print(f"VCRM: unreadable baseline: {error}", file=sys.stderr)
        return 1
    evidence = json.loads(args.evidence.read_text(encoding="utf-8")) if args.evidence.exists() else {}
    matrix = build(baseline, evidence)
    markdown = to_markdown(matrix, args.fail_on)

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "vcrm.md").write_text(markdown, encoding="utf-8")
    write_csv(matrix, args.out / "vcrm.csv")
    if args.summary:
        with args.summary.open("a", encoding="utf-8") as handle:
            handle.write(markdown)
    print(markdown)

    found = violations(matrix, args.fail_on)
    for problem in found:
        print(f"VCRM: {problem}", file=sys.stderr)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
