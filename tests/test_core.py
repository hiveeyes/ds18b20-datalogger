import os
import sys
from pathlib import Path

import pytest
import yaml
from pyfakefs.fake_filesystem_unittest import Patcher as FakeFS

from ds18b20_datalogger.core import read_ds18b20_sensor_matrix, send_measurement_mqtt
from ds18b20_datalogger.model import Settings

if sys.version_info < (3, 9):
    from importlib_resources import files
else:
    from importlib.resources import files


def get_hardware_description(filename: str):
    """
    Read hardware description (map from sensor identifiers to values) from YAML file.
    """
    testfile = files("tests") / filename
    return yaml.safe_load(testfile.read_bytes())


def synthesize_hardware(description):
    """
    Provide a fake sysfs filesystem to test cases, reflecting a hardware description.
    """
    for item in description:
        identifier = item["device"]
        value = item["value"]
        path = f"/sys/bus/w1/devices/{identifier}"
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/w1_slave", "w") as f:
            f.write(f"YES\nt={value}")


@pytest.fixture
def onewire_success():
    """
    This fixture reflects that all DS18B20 sensors work well.
    """
    return get_hardware_description("onewire-success.yaml")


@pytest.fixture
def onewire_defunct():
    """
    This fixture reflects that a few DS18B20 sensors are defunct.
    """
    return get_hardware_description("onewire-defunct.yaml")


@pytest.fixture
def fake_hardware_success(onewire_success, fs: FakeFS):
    synthesize_hardware(onewire_success)
    yield fs


@pytest.fixture
def fake_hardware_defunct(onewire_defunct, fs: FakeFS):
    synthesize_hardware(onewire_defunct)
    yield fs


@pytest.fixture
def settings() -> Settings:
    configfile = Path("etc") / "mois.yaml"
    return Settings.from_file(configfile)


def test_sensors_success(settings, fake_hardware_success):
    reading = read_ds18b20_sensor_matrix(settings.devicemap)
    assert reading.to_matrix(5) == [
        [0.001, 0.002, 0.003, 0.004, 0.005],
        [0.006, 0.007, 0.008, 0.009, 0.010],
        [0.011, 0.012, 0.013, 0.014, 0.015],
        [0.016, 0.017, 0.018, 0.019, 0.020],
        [0.021, 0.022, 0.023, 0.024, 0.025],
        [0.026, 0.027, 0.028, 0.029, 0.030],
    ]


def test_sensors_defunct(settings, fake_hardware_defunct):
    reading = read_ds18b20_sensor_matrix(settings.devicemap)
    assert reading.to_matrix(5) == [
        [0.001, 0.002, 0.003, 0.004, 0.005],
        [-99.0, 0.007, 0.008, None, 0.010],
        [0.011, 0.012, 0.013, 0.014, 0.015],
        [0.016, 0.017, 0.018, 0.019, 0.020],
        [0.021, 0.022, 0.023, 0.024, 0.025],
        [0.026, 0.027, 0.028, 0.029, 0.030],
    ]


def test_sensors_none(settings):
    reading = read_ds18b20_sensor_matrix(settings.devicemap)
    assert reading.to_matrix(5) == [
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
    ]


def test_telemetry(settings):
    reading = read_ds18b20_sensor_matrix(settings.devicemap)
    send_measurement_mqtt(settings.mqtt, reading)


@pytest.fixture
def offset_settings() -> Settings:
    configfile = Path("tests") / "datalogger-offset.yaml"
    return Settings.from_file(configfile)


def test_sensors_offset(offset_settings, fake_hardware_success):
    reading = read_ds18b20_sensor_matrix(offset_settings.devicemap)
    assert reading.to_dict() == {
        "temp-ir-1-1": -0.499,
        "temp-ir-1-2": 0.002,
        "temp-ir-1-3": 0.003,
    }
