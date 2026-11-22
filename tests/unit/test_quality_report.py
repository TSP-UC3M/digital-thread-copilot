"""Unit tests of scripts/quality_report.py on hand-computed examples (plan step F3)."""

import importlib.util
import pathlib

SCRIPT = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "quality_report.py"
spec = importlib.util.spec_from_file_location("quality_report", SCRIPT)
quality_report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quality_report)


def test_code_lines_ignore_blank_lines_comments_and_indentation():
    text = "a = 1\n\n    # comment\n    b = 2\n"
    assert quality_report.code_lines(text) == ["a = 1", "b = 2"]


def test_duplication_counts_a_run_repeated_in_two_files():
    run = "\n".join(f"x{i} = {i}" for i in range(6))
    sources = {"a.py": run + "\nunique_a = 1\n", "b.py": "unique_b = 2\n" + run + "\n"}
    # 6 duplicated lines in each file, 7 code lines in each file.
    assert quality_report.duplication(sources) == (12, 14)


def test_duplication_is_zero_below_the_window():
    run = "\n".join(f"x{i} = {i}" for i in range(5))
    assert quality_report.duplication({"a.py": run, "b.py": run}) == (0, 10)


def test_duplication_of_no_source_is_zero():
    assert quality_report.duplication({}) == (0, 0)


def test_read_coverage_returns_totals_and_files(tmp_path):
    report = tmp_path / "coverage.xml"
    report.write_text(
        '<coverage line-rate="0.75" branch-rate="0.5" lines-valid="8" lines-covered="6">'
        '<packages><package><classes><class filename="pkg/a.py" line-rate="0.75"/></classes></package></packages>'
        "</coverage>",
        encoding="utf-8",
    )
    result = quality_report.read_coverage(report)
    assert result["line_rate"] == 0.75
    assert result["lines_covered"] == 6
    assert result["files"] == {"pkg/a.py": 0.75}


def test_read_coverage_without_file_returns_none(tmp_path):
    assert quality_report.read_coverage(tmp_path / "missing.xml") is None
