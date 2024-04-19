import subprocess
import typing as t

import yaml


def invoke(command: str) -> t.Tuple[int, str]:
    return subprocess.getstatusoutput(command)  # noqa: S603, S605


def test_cli_no_subcommand():
    exitcode, output = invoke("ds18b20-datalogger")
    assert "Program needs a subcommand" in output


def test_cli_unknown_subcommand():
    exitcode, output = invoke("ds18b20-datalogger foo")
    assert "Subcommand unknown: foo" in output


def test_cli_run_no_config():
    exitcode, output = invoke("ds18b20-datalogger run")
    assert "Program needs a configuration file" in output


def test_cli_make_config():
    exitcode, output = invoke("ds18b20-datalogger make-config")
    config = yaml.safe_load(output)
    assert "mqtt" in config
    assert "one-wire" in config
