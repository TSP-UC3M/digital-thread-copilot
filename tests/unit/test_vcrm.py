"""Unit tests of scripts/vcrm.py on hand-made baselines and evidence (plan step F7)."""

import csv
import importlib.util
import json
import pathlib
import sys

import pytest
import yaml

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "vcrm.py"
spec = importlib.util.spec_from_file_location("vcrm", SCRIPT)
vcrm = importlib.util.module_from_spec(spec)
sys.modules["vcrm"] = vcrm  # dataclasses look the module up by name
spec.loader.exec_module(vcrm)


def requirement(rid, method="test", priority="M", **verification):
    return {
        "id": rid,
        "module": "Tools",
        "text": f"The system shall do {rid}.",
        "verification": {"method": method, "criterion": f"criterion of {rid}", **verification},
        "traces_to": ["OE4"],
        "priority": priority,
        "status": "unchanged",
    }


@pytest.fixture
def run(tmp_path, monkeypatch):
    """Write the baseline and the evidence, run the script, return (exit code, matrix text, output folder)."""
    for name in ("GITHUB_RUN_ID", "GITHUB_REPOSITORY", "GITHUB_SERVER_URL", "RUNNER_OS"):
        monkeypatch.delenv(name, raising=False)

    def _run(requirements=None, evidence=None, *options):
        args = ["--out", str(tmp_path / "reports"), "--evidence", str(tmp_path / "evidence.json")]
        baseline = tmp_path / "requirements.yaml"
        if requirements is not None:
            baseline.write_text(yaml.safe_dump(requirements), encoding="utf-8")
        args += ["--requirements", str(baseline)]
        if evidence is not None:
            (tmp_path / "evidence.json").write_text(json.dumps(evidence), encoding="utf-8")
        code = vcrm.main([*args, *options])
        return code, (tmp_path / "reports" / "vcrm.md").read_text(encoding="utf-8"), tmp_path / "reports"

    return _run


def statuses(text):
    """Status column of the compact table, by identifier."""
    rows = [line.split("|") for line in text.splitlines() if line.startswith("| R-")]
    return {cells[1].strip(): cells[5].strip().strip("*") for cells in rows if len(cells) == 8}


def test_status_of_test_method_requirements_follows_their_tests(run):
    baseline = {"requirements": [requirement(r) for r in ("R-1", "R-2", "R-3", "R-4")]}
    evidence = {
        "t::a": {"requirements": ["R-1"], "outcome": "passed"},
        "t::b": {"requirements": ["R-1", "R-2"], "outcome": "passed"},
        "t::c": {"requirements": ["R-2"], "outcome": "failed"},
        "t::d": {"requirements": ["R-3"], "outcome": "skipped"},
    }
    code, text, _ = run(baseline, evidence)
    assert statuses(text) == {"R-1": "Passed", "R-2": "Failed", "R-3": "In progress", "R-4": "No evidence"}
    assert "| 4 | 1 | 1 | 0 | 1 | 1 | 25 % |" in text
    assert "- `t::c` (R-2)" in text
    assert code == 1  # R-2 is Failed


def test_removed_requirement_is_not_listed_and_a_test_citing_it_is_an_error(run):
    removed = requirement("R-9") | {"status": "removed"}
    baseline = {"requirements": [requirement("R-1"), removed]}
    evidence = {
        "t::a": {"requirements": ["R-1"], "outcome": "passed"},
        "t::z": {"requirements": ["R-9"], "outcome": "passed"},
    }
    code, text, _ = run(baseline, evidence)
    assert set(statuses(text)) == {"R-1"}
    assert "Removed requirements, not listed: 1." in text
    assert "- `t::z` cites R-9" in text
    assert code == 1


def test_unknown_identifier_fails_the_consistency_rule(run):
    code, text, _ = run(
        {"requirements": [requirement("R-1")]}, {"t::a": {"requirements": ["R-404"], "outcome": "passed"}}
    )
    assert code == 1
    assert "- `t::a` cites R-404" in text


def test_manual_method_needs_evidence_to_be_passed(run):
    without = requirement("R-1", method="inspection", status="passed")
    with_evidence = requirement("R-2", method="analysis", status="passed", evidence="PR 42 review")
    pending = requirement("R-3", method="demonstration")
    code, text, _ = run({"requirements": [without, with_evidence, pending]}, {})
    assert statuses(text) == {"R-1": "Passed", "R-2": "Passed", "R-3": "Pending"}
    assert code == 1  # R-1 has no evidence


def test_exit_rules_coverage_and_complete_only_concern_must_requirements(run):
    baseline = {
        "requirements": [
            requirement("R-1"),
            requirement("R-2", priority="S"),
            requirement("R-3", method="inspection"),
        ]
    }
    evidence = {"t::a": {"requirements": ["R-1"], "outcome": "skipped"}}
    assert run(baseline, evidence)[0] == 0
    assert run(baseline, evidence, "--fail-on", "coverage")[0] == 0  # R-1 has a test; R-2 is a should
    assert run(baseline, {}, "--fail-on", "coverage")[0] == 1
    assert run(baseline, evidence, "--fail-on", "complete")[0] == 1  # R-1 in progress, R-3 pending


def test_without_baseline_the_matrix_only_counts_the_evidence(run):
    evidence = {
        "t::a": {"requirements": ["R-1"], "outcome": "passed"},
        "t::b": {"requirements": [], "outcome": "passed"},
    }
    code, text, _ = run(None, evidence)
    assert code == 0
    assert "No requirements baseline in the repository yet" in text
    assert "Tests run: 2, of which 1 carry a requirement identifier." in text


def test_validation_activities_are_listed_apart_and_identifiers_are_unique(run):
    baseline = {
        "requirements": [requirement("R-1")],
        "validation_activities": [
            {"id": "VAL-01", "need": "Answers help the engineer", "method": "analysis", "criterion": "c"},
            {"id": "R-1", "need": "duplicate", "method": "demonstration", "criterion": "c"},
        ],
    }
    code, text, _ = run(baseline, {"t::a": {"requirements": ["R-1"], "outcome": "passed"}})
    section = text.split("### Validation activities")[1].split("<details>")[0]
    assert "| VAL-01 | Answers help the engineer | Analysis (A) | c | Pending |  |" in section
    assert code == 1  # R-1 used twice


def test_csv_has_the_twelve_columns_of_the_course_template(run):
    baseline = {"requirements": [requirement("R-1", method="analysis", criterion="a | b")]}
    _, text, folder = run(baseline, {})
    with (folder / "vcrm.csv").open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert tuple(rows[0]) == vcrm.COLUMNS
    assert rows[0]["Acceptance criterion"] == "a | b"
    assert "a \\| b" in text  # escaped in Markdown, kept as is in the CSV


def test_summary_file_receives_the_matrix(run, tmp_path):
    summary = tmp_path / "summary.md"
    summary.write_text("before\n", encoding="utf-8")
    run({"requirements": [requirement("R-1")]}, {}, "--summary", str(summary))
    assert summary.read_text(encoding="utf-8").startswith("before\n## Verification matrix (VCRM)")


def test_ci_run_gives_a_link_to_the_github_run(monkeypatch):
    monkeypatch.setenv("GITHUB_RUN_ID", "123")
    monkeypatch.setenv("GITHUB_REPOSITORY", "org/repo")
    monkeypatch.setenv("GITHUB_SERVER_URL", "https://github.com")
    monkeypatch.setenv("RUNNER_OS", "Linux")
    environment, link = vcrm.ci_run()
    assert environment.startswith("GitHub Actions, Linux, Python ")
    assert link == "[CI run 123](https://github.com/org/repo/actions/runs/123)"


def test_failed_validation_activity_is_reported_without_failing_the_job(run):
    rejected = {
        "id": "VAL-01",
        "need": "n",
        "method": "analysis",
        "criterion": "c",
        "status": "failed",
        "evidence": "I4",
    }
    code, text, _ = run(
        {"requirements": [requirement("R-1", method="inspection")], "validation_activities": [rejected]}, {}
    )
    assert "| VAL-01 | n | Analysis (A) | c | Failed | I4 |" in text
    assert code == 0
