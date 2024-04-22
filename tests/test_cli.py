import json
import shlex
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


def test_cli_run_read_no_config():
    exitcode, output = invoke("ds18b20-datalogger run")
    assert "Program needs a configuration file" in output

    exitcode, output = invoke("ds18b20-datalogger read")
    assert "Program needs a configuration file" in output


def test_cli_run_read_nonexist_config():
    exitcode, output = invoke("ds18b20-datalogger run foo.yaml")
    assert "Configuration file does not exist: foo.yaml" in output


def test_cli_read_success():
    command = shlex.split("ds18b20-datalogger read ds18b20_datalogger/datalogger.yaml")
    process = subprocess.run(command, stdout=subprocess.PIPE)  # noqa: S603
    reading = json.loads(process.stdout)
    assert "temp-ir-1-1" in reading
    assert "temp-ir-2-3" in reading
    assert len(reading) == 6


def test_cli_run_almost_success():
    exitcode, output = invoke("ds18b20-datalogger run ds18b20_datalogger/datalogger.yaml")
    assert exitcode == 1
    assert "nodename nor servname provided, or not known" in output or "Name or service not known" in output


def test_cli_make_config():
    command = shlex.split("ds18b20-datalogger make-config")
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # noqa: S603
    config = yaml.safe_load(process.stdout)
    assert "mqtt" in config
    assert "one-wire" in config
    assert b"Please make sure to edit the configuration" in process.stderr


def test_cli_make_dashboard():
    exitcode, output = invoke("ds18b20-datalogger make-dashboard")
    dashboard = json.loads(output)
    assert "annotations" in dashboard
    assert "panels" in dashboard
    assert "title" in dashboard
