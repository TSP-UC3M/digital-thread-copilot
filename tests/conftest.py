"""Evidence of verification: which requirement each test verifies, and its result (plan step F7).

A test declares the requirements it verifies with a marker:

    @pytest.mark.req("FR-TOOL-01")
    @pytest.mark.req("FR-TOOL-02", "FR-TOOL-03")   # several identifiers are allowed

With the option --req-evidence=<file>, the result of every test is written to that JSON file at the
end of the session; scripts/vcrm.py turns it into the verification matrix (VCRM). Without the option,
nothing is written. Pattern of the course workshop "Integración continua como verificación continua".
"""

import json
from pathlib import Path

import pytest

_RANK = {"passed": 0, "skipped": 1, "failed": 2}
_evidence: dict[str, dict] = {}


def pytest_addoption(parser):
    parser.addoption(
        "--req-evidence",
        metavar="FILE",
        default=None,
        help="write the requirement identifiers and the result of each test to FILE (JSON)",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "req(*ids): identifiers of the requirements verified by the test (VCRM)")


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield
    ids = [str(arg) for marker in item.iter_markers(name="req") for arg in marker.args]
    entry = _evidence.setdefault(item.nodeid, {"requirements": ids, "outcome": "passed"})
    # Worst result over setup, call and teardown: failed, then skipped (an expected failure counts as skipped).
    outcome = report.outcome if report.outcome in _RANK else "failed"
    entry["outcome"] = max(entry["outcome"], outcome, key=_RANK.get)
    return report


def pytest_sessionfinish(session):
    target = session.config.getoption("--req-evidence")
    if not target:
        return
    path = Path(target)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
