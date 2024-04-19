from pathlib import Path

import pytest

from ds18b20_datalogger.model import Device, Settings


@pytest.fixture
def settings() -> Settings:
    configfile = Path("etc") / "mois.yaml"
    return Settings.from_file(configfile)


def test_model_devicemap_by_name_success(settings):
    assert settings.devicemap.by_name("temp-ir-1-1") == Device(
        name="temp-ir-1-1", path="/sys/bus/w1/devices/28-0346d4430b06"
    )


def test_model_devicemap_by_name_failure(settings):
    with pytest.raises(KeyError) as ex:
        settings.devicemap.by_name("foo")
    assert ex.match("'Device not found: name=foo'")


def test_model_devicemap_by_fullpath_success(settings):
    assert settings.devicemap.by_fullpath("/sys/bus/w1/devices/28-0346d4430b06") == Device(
        name="temp-ir-1-1", path="/sys/bus/w1/devices/28-0346d4430b06"
    )


def test_model_devicemap_by_fullpath_failure(settings):
    with pytest.raises(KeyError) as ex:
        settings.devicemap.by_fullpath("foo")
    assert ex.match("'Device not found: path=foo'")


def test_model_devicemap_by_pathname_success(settings):
    assert settings.devicemap.by_pathname("28-0346d4430b06") == Device(
        name="temp-ir-1-1", path="/sys/bus/w1/devices/28-0346d4430b06"
    )


def test_model_devicemap_by_pathname_failure(settings):
    with pytest.raises(KeyError) as ex:
        settings.devicemap.by_pathname("foo")
    assert ex.match("'Device not found: pathname=foo'")
