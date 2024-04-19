import json
import os

import paho.mqtt.client as mqtt

from ds18b20_datalogger.model import DeviceMap, MqttSettings, Reading


def read_temp_raw(device_file):
    f = open(device_file, "r")
    lines = f.readlines()
    f.close()
    return lines


def read_temp(device_file):
    maxAttempts = 3
    while True:
        temp = try_temp(device_file)
        if temp != -99.0:
            return temp
        maxAttempts -= 1
        if maxAttempts <= 0:
            return temp


def try_temp(device_file):
    temp_c = -99.0
    try:
        lines = read_temp_raw(device_file + "/w1_slave")
    except FileNotFoundError:
        return None
    if len(lines) == 2:
        if lines[0].strip()[-3:] == "YES":
            equals_pos = lines[1].find("t=")
            temp_string = lines[1][equals_pos + 2 :]
            temp_c = float(temp_string) / 1000.0
    return temp_c


def send_measurement_mqtt(mqtt_settings: MqttSettings, reading: Reading):
    """
    Publish measurement to MQTT topic in JSON format.
    """
    # Serialize reading to JSON.
    payload = json.dumps(reading.to_dict())
    # Publish to MQTT.
    pid = os.getpid()
    client_id = "{}:{}".format(mqtt_settings.client_id, str(pid))
    backend = mqtt.Client(client_id=client_id, clean_session=True)
    if mqtt_settings.username and mqtt_settings.password:
        backend.username_pw_set(mqtt_settings.username, mqtt_settings.password)
    backend.connect(mqtt_settings.host, mqtt_settings.port or 1883)
    backend.publish(mqtt_settings.topic, payload)
    backend.disconnect()


def read_ds18b20_sensor_matrix(devicemap: DeviceMap) -> Reading:
    """
    Acquire measurement reading from an array matrix of DS18B20 sensors, connected to a Raspberry Pi machine.

    Make sure to use the correct configuration for your sensor setup.
    In order to research into it, use, for example:

        ls -la /sys/bus/w1/devices/
    """

    # Install drivers, in order to provide sysfs-based
    # access to devices connected to the one-wire bus.
    os.system("modprobe w1-gpio")  # noqa: S605, S607
    os.system("modprobe w1-therm")  # noqa: S605, S607

    reading = Reading()
    for device in devicemap.devices:
        value = read_temp(device.path)
        reading.add_measurement(name=device.name, value=value)
    return reading
