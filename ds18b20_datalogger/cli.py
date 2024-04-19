import json
import sys
from pathlib import Path

from ds18b20_datalogger.core import read_ds18b20_sensor_matrix, send_measurement_mqtt
from ds18b20_datalogger.model import Settings

if sys.version_info < (3, 9):
    from importlib_resources import files  # pragma: nocover
else:
    from importlib.resources import files


def main():

    # Sanity checks.
    if not sys.argv[1:]:
        raise ValueError("Program needs a subcommand")
    subcommand = sys.argv[1]

    # Evaluate subcommand.
    if subcommand in ["run", "read"]:
        if not sys.argv[2:]:
            raise ValueError("Program needs a configuration file")
        configfile = Path(sys.argv[2])
        if not configfile.exists():
            raise ValueError(f"Configuration file does not exist: {configfile}")
        settings = Settings.from_file(configfile)
        reading = read_ds18b20_sensor_matrix(settings.devicemap)
        if subcommand == "read":
            print(json.dumps(reading.to_dict(), indent=2))  # noqa: T201
        elif subcommand == "run":
            send_measurement_mqtt(settings.mqtt, reading)

    elif subcommand == "make-config":
        config_template = files("ds18b20_datalogger") / "datalogger.yaml"
        print(config_template.read_text(), file=sys.stdout)  # noqa: T201

    elif subcommand == "make-dashboard":
        dashboard = files("ds18b20_datalogger") / "grafana-dashboard.json"
        print(dashboard.read_text(), file=sys.stdout)  # noqa: T201

    else:
        raise ValueError(f"Subcommand unknown: {subcommand}")
