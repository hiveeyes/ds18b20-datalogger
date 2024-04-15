import contextlib
import os
import sys

import pytest
import yaml
from pyfakefs.fake_filesystem_unittest import Patcher as FakeFS

from ds18b20_datalogger.core import read_ds18b20_sensor_matrix, send_measurement_mqtt

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


@contextlib.contextmanager
def synthesize_hardware(description):
    """
    Provide a fake sysfs filesystem to test cases, reflecting a hardware description.
    """
    with FakeFS():
        for item in description:
            identifier = item["device"]
            value = item["value"]
            path = f"/sys/bus/w1/devices/{identifier}"
            os.makedirs(path, exist_ok=True)
            with open(f"{path}/w1_slave", "w") as f:
                f.write(f"YES\nt={value}")
        yield


@pytest.fixture
def fake_hardware_success():
    """
    Provide a fake sysfs filesystem to test cases, reflecting a dummy reading, defined in `onewire-success.yaml`.

    This fixture reflects that all DS18B20 sensors work well.
    """
    description = get_hardware_description("onewire-success.yaml")
    with synthesize_hardware(description):
        yield


@pytest.fixture
def fake_hardware_defunct():
    """
    Provide a fake sysfs filesystem to test cases, reflecting a dummy reading, defined in `onewire-defunct.yaml`.

    This fixture reflects that a few DS18B20 sensors are defunct.
    """
    description = get_hardware_description("onewire-defunct.yaml")
    with synthesize_hardware(description):
        yield


def test_sensors_success(fake_hardware_success):
    reading = read_ds18b20_sensor_matrix()
    assert reading == [
        [0.001, 0.002, 0.003, 0.004, 0.005],
        [0.006, 0.007, 0.008, 0.009, 0.010],
        [0.011, 0.012, 0.013, 0.014, 0.015],
        [0.016, 0.017, 0.018, 0.019, 0.020],
        [0.021, 0.022, 0.023, 0.024, 0.025],
        [0.026, 0.027, 0.028, 0.029, 0.030],
    ]


def test_sensors_defunct(fake_hardware_defunct):
    reading = read_ds18b20_sensor_matrix()
    assert reading == [
        [0.001, 0.002, 0.003, 0.004, 0.005],
        [-99.0, 0.007, 0.008, None, 0.010],
        [0.011, 0.012, 0.013, 0.014, 0.015],
        [0.016, 0.017, 0.018, 0.019, 0.020],
        [0.021, 0.022, 0.023, 0.024, 0.025],
        [0.026, 0.027, 0.028, 0.029, 0.030],
    ]


def test_sensors_none():
    reading = read_ds18b20_sensor_matrix()
    assert reading == [
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
    ]


def test_telemetry():
    reading = read_ds18b20_sensor_matrix()
    send_measurement_mqtt(reading)
