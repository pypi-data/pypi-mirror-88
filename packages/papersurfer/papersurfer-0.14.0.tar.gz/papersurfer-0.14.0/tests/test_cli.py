"""Tests for command line interface (CLI)."""
import os
from typing import Any
import pytest
import papersurfer


def test_runas_module() -> None:
    """Run package as a Python module."""
    exit_status = os.system('python -m papersurfer --help')
    assert exit_status == 0


def test_entrypoint() -> None:
    """Is entrypoint script installed? (setup.py)."""
    exit_status = os.system('papersurfer --help')
    assert exit_status == 0


def test_configfile_fail() -> None:
    """Fail when trying to load a nonexistent config file."""
    cli = 'python -m papersurfer --config /dev/null'
    exit_status = os.system(cli)
    assert exit_status != 0


def test_configfile(shared_datadir: Any) -> None:
    """Load and write a config file."""
    conffile = (shared_datadir / "papersurfer.conf")
    outfile = (shared_datadir / "delme.txt")
    cli = f"python -m papersurfer --config {conffile} -w {outfile}"

    exit_status = os.system(cli)
    assert exit_status == 0

    with open(outfile) as file:
        content = file.read()

    assert "Paperclub" in content


def test_cli() -> None:
    """Test if CLI stops execution w/o a command argument."""
    with pytest.raises(SystemExit):
        papersurfer.__main__.main()  # type: ignore
        pytest.fail("CLI doesn't abort asking for a command argument")
