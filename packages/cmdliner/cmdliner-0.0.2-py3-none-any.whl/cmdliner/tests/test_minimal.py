"""
A test utility
"""
from cmdliner import cli, verbose
from unittest.mock import patch


@cli("0.0.1")
def main():
    print("hello")
    verbose(1, "Printed on verbose mode")
    verbose(2, "Very verbose mode")


@cli("0.0.1", __doc__)
def doc_main():
    pass


def test_simple(capsys):
    main()
    assert capsys.readouterr().out == "hello\n"


def test_doc_help(capsys):
    with patch("sys.argv", ["program_name", "--help"]):
        doc_main()
    assert capsys.readouterr().out == "\nA test utility\n\n"


def test_verbose(capsys):
    with patch("sys.argv", ["program_name", "-v"]):
        main()
    assert capsys.readouterr().out == "hello\nPrinted on verbose mode\n"


def test_very_verbose(capsys):
    with patch("sys.argv", ["program_name", "-vvv"]):
        main()
    assert (
        capsys.readouterr().out == "hello\nPrinted on verbose mode\nVery verbose mode\n"
    )
