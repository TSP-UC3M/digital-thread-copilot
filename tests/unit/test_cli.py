"""Unit tests of the command line parser."""

import pytest

from digital_thread_copilot import __version__
from digital_thread_copilot.__main__ import build_parser, main


def test_version_is_a_semantic_version():
    parts = __version__.split(".")
    assert len(parts) == 4
    assert all(part.isdigit() for part in parts)


def test_version_option_prints_the_version_and_exits(capsys):
    with pytest.raises(SystemExit) as exit_info:
        build_parser().parse_args(["--version"])
    assert exit_info.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_main_without_argument_prints_help_and_returns_zero(capsys):
    assert main([]) == 0
    assert "usage: dtc" in capsys.readouterr().out


def test_unknown_option_is_rejected():
    with pytest.raises(SystemExit) as exit_info:
        main(["--no-such-option"])
    assert exit_info.value.code == 2
