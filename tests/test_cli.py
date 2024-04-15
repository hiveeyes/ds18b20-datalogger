import shlex
import subprocess


def test_cli():
    command = "ds18b20-datalogger"
    subprocess.check_call(shlex.split(command))  # noqa: S603, S605
