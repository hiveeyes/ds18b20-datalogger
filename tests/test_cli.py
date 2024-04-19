import subprocess
import typing as t


def invoke(command: str) -> t.Tuple[int, str]:
    return subprocess.getstatusoutput(command)  # noqa: S603, S605


def test_cli_run():
    invoke("ds18b20-datalogger run")


def test_cli_no_subcommand():
    exitcode, output = invoke("ds18b20-datalogger")
    assert "Program needs a subcommand" in output


def test_cli_unknown_subcommand():
    exitcode, output = invoke("ds18b20-datalogger foo")
    assert "Subcommand unknown: foo" in output
