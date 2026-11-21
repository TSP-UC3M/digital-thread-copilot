"""Functional tests: the installed package is run as a separate process."""

import subprocess
import sys

import pytest

from digital_thread_copilot import __version__

pytestmark = pytest.mark.functional


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "digital_thread_copilot", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_module_reports_its_version():
    result = run("--version")
    assert result.returncode == 0
    assert result.stdout.strip() == f"digital-thread-copilot {__version__}"


def test_module_runs_without_argument():
    result = run()
    assert result.returncode == 0
    assert "usage: dtc" in result.stdout
