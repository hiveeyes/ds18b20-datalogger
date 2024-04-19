import sys
from pathlib import Path

from ds18b20_datalogger.core import read_ds18b20_sensor_matrix, send_measurement_mqtt
from ds18b20_datalogger.model import Settings


def main():
    if not sys.argv[1:]:
        raise ValueError("Program needs a subcommand")
    subcommand = sys.argv[1]
    if subcommand == "run":
        if not sys.argv[2:]:
            raise ValueError("Program needs a configuration file")
        configfile = Path(sys.argv[2])
        if not configfile.exists():
            raise ValueError(f"Configuration file does not exist: {configfile}")
        settings = Settings.from_file(configfile)
        reading = read_ds18b20_sensor_matrix(settings.devicemap)
        send_measurement_mqtt(settings.mqtt, reading)
    else:
        raise ValueError(f"Subcommand unknown: {subcommand}")
