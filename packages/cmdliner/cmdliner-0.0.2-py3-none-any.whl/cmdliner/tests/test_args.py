"""
A test utility
"""
import pytest
from cmdliner import cli
from unittest.mock import patch


@cli("0.0.1")
def main(name):
    print(f"Hello {name}")


def test_missing_parameter(capsys):
    with patch("sys.argv", ["program_name"]):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert capsys.readouterr().out == ""
    assert capsys.readouterr().err == ""


def test_using_parameter(capsys):
    with patch("sys.argv", ["program_name", "Joe"]):
        main()
    assert capsys.readouterr().out == "Hello Joe\n"
