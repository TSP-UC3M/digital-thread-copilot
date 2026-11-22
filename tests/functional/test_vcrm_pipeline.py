"""Functional test of the verification chain: marked tests, evidence file, then matrix (plan step F7).

A small project is written in a temporary folder with the real tests/conftest.py, run by pytest in a
separate process, and its evidence is turned into a matrix by scripts/vcrm.py, as the CI job does.
"""

import json
import os
import pathlib
import shutil
import subprocess
import sys
import textwrap

import pytest

pytestmark = pytest.mark.functional

ROOT = pathlib.Path(__file__).resolve().parents[2]

SAMPLE_TESTS = textwrap.dedent(
    """
    import pytest

    @pytest.mark.req("REQ-01")
    def test_passes():
        assert True

    @pytest.mark.req("REQ-02")
    def test_fails():
        assert False

    @pytest.mark.req("REQ-03")
    @pytest.mark.skip(reason="not implemented yet")
    def test_skipped():
        pass

    @pytest.fixture
    def broken_teardown():
        yield
        raise RuntimeError("teardown")

    @pytest.mark.req("REQ-01")
    def test_teardown_error_counts_as_failed(broken_teardown):
        pass

    def test_without_marker():
        assert True
    """
)

BASELINE = textwrap.dedent(
    """
    requirements:
      - {id: REQ-01, text: "a", verification: {method: test, criterion: "c"}, priority: M}
      - {id: REQ-02, text: "b", verification: {method: test, criterion: "c"}, priority: M}
      - {id: REQ-03, text: "c", verification: {method: test, criterion: "c"}, priority: M}
      - {id: REQ-04, text: "d", verification: {method: inspection, criterion: "c"}, priority: M}
    """
)


def run(*args, cwd):
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run([sys.executable, *args], cwd=cwd, env=env, capture_output=True, text=True, check=False)


def test_marked_tests_become_rows_of_the_matrix(tmp_path):
    shutil.copy(ROOT / "tests" / "conftest.py", tmp_path / "conftest.py")
    (tmp_path / "test_sample.py").write_text(SAMPLE_TESTS, encoding="utf-8")
    (tmp_path / "requirements.yaml").write_text(BASELINE, encoding="utf-8")

    tests = run("-m", "pytest", "-p", "no:cacheprovider", "--req-evidence=evidence.json", "-q", cwd=tmp_path)
    assert tests.returncode == 1, tests.stdout  # test_fails and the teardown error

    evidence = json.loads((tmp_path / "evidence.json").read_text(encoding="utf-8"))
    outcomes = {node.split("::")[1]: entry for node, entry in evidence.items()}
    assert outcomes["test_passes"] == {"requirements": ["REQ-01"], "outcome": "passed"}
    assert outcomes["test_teardown_error_counts_as_failed"]["outcome"] == "failed"
    assert outcomes["test_skipped"]["outcome"] == "skipped"
    assert outcomes["test_without_marker"]["requirements"] == []

    matrix = run(
        str(ROOT / "scripts" / "vcrm.py"),
        "--requirements=requirements.yaml",
        "--evidence=evidence.json",
        "--out=reports",
        cwd=tmp_path,
    )
    assert matrix.returncode == 1  # REQ-01 and REQ-02 are Failed
    text = (tmp_path / "reports" / "vcrm.md").read_text(encoding="utf-8")
    assert "| REQ-01 |  | Test (T) | 1/2 | **Failed** |" in text
    assert "| REQ-03 |  | Test (T) | 0/1 | In progress |" in text
    assert "| REQ-04 |  | Inspection (I) | n/a | Pending |" in text
    assert "Tests not linked to any requirement: 1." in text


def test_without_the_option_no_evidence_file_is_written(tmp_path):
    shutil.copy(ROOT / "tests" / "conftest.py", tmp_path / "conftest.py")
    (tmp_path / "test_one.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    result = run("-m", "pytest", "-p", "no:cacheprovider", "-q", cwd=tmp_path)
    assert result.returncode == 0, result.stdout
    assert sorted(path.name for path in tmp_path.iterdir()) == ["conftest.py", "test_one.py"]
