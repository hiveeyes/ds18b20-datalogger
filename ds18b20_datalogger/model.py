import dataclasses
import typing as t
from collections import OrderedDict
from pathlib import Path

import yaml

from ds18b20_datalogger.util import partition


@dataclasses.dataclass
class Device:
    """
    Manage a one-wire device, mapping a sysfs path to a user-assigned name/label.
    """

    name: str
    path: str


class DeviceMap:
    """
    Manage a map of one-wire devices to names/labels.
    """

    def __init__(self):
        self.devices: t.List[Device] = []

    def by_name(self, name: str) -> Device:
        for device in self.devices:
            if device.name == name:
                return device
        raise KeyError(f"Device not found: name={name}")

    def by_fullpath(self, path: Path) -> Device:
        for device in self.devices:
            if str(device.path) == str(path):
                return device
        raise KeyError(f"Device not found: path={path}")

    def by_pathname(self, path: Path) -> Device:
        needle = Path(path).name
        for device in self.devices:
            if Path(device.path).name == needle:
                return device
        raise KeyError(f"Device not found: pathname={needle}")


@dataclasses.dataclass
class MqttSettings:
    """
    Container for MQTT settings.
    """

    host: str
    topic: str
    port: t.Optional[int] = None
    username: t.Optional[str] = None
    password: t.Optional[str] = None
    client_id: t.Optional[str] = None


@dataclasses.dataclass
class Settings:
    """
    General settings container.
    """

    mqtt: MqttSettings
    devicemap: DeviceMap

    @classmethod
    def from_file(cls, configfile: Path):
        data = yaml.safe_load(configfile.read_text())
        devicemap = DeviceMap()
        for item in data["one-wire"]:
            devicemap.devices.append(Device(**item))
        return cls(mqtt=MqttSettings(**data["mqtt"]), devicemap=devicemap)


@dataclasses.dataclass
class Measurement:
    """
    Manage a measurement, coming from a device.
    """

    name: str
    value: float


@dataclasses.dataclass
class Reading:
    """
    Manage a reading, made of multiple measurements.
    """

    measurements: t.List[Measurement] = dataclasses.field(default_factory=list)

    def add_measurement(self, name: str, value: float):
        self.measurements.append(Measurement(name=name, value=value))

    def to_dict(self) -> t.Dict[str, float]:
        data = OrderedDict()
        for measurement in self.measurements:
            data[measurement.name] = measurement.value
        return data

    def to_matrix(self, rowlength: int):
        values = [m.value for m in self.measurements]
        return list(partition(values, rowlength))
