#!/usr/bin/env python
"""
Requires:
paho-mqtt in a venv: https://pypi.org/project/paho-mqtt/#installation
insert your own sensor addresses (see below line 125+)
your MQTT connection settings and credentials (line 65+)

Recommended:
```
ssh to your pi
screen
source /path/to/ds18b20-datalogger/.venv/bin/activate
ds18b20-datalogger
```

Ursprünglicher code zur Datenverarbeitung auf dem Pi:
https://community.element14.com/products/raspberry-pi/raspberrypi_projects/b/blog/posts/multiple-ds18b20-temp-sensors-interfacing-with-raspberry-pi?CommentId=9470e4e9-b054-4dd3-9a3f-ac9d1fe38087
"""  # noqa: E501

import glob
import json
import os

import paho.mqtt.client as mqtt


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
    lines = read_temp_raw(device_file + "/w1_slave")
    if len(lines) == 2:
        if lines[0].strip()[-3:] == "YES":
            equals_pos = lines[1].find("t=")
            temp_string = lines[1][equals_pos + 2 :]
            temp_c = float(temp_string) / 1000.0
    return temp_c


def send_measurement_mqtt(matrix):
    """
    Publish measurement to MQTT topic in JSON format.
    """
    # The MQTT host
    mqtt_host = "swarm.hiveeyes.org"
    mqtt_port = 1883
    mqtt_user = "username"
    mqtt_pass = "some_safe_password"  # noqa: S105
    # The MQTT topic
    mqtt_topic = "{realm}/{network}/{gateway}/{node}/data.json".format(
        # Beekeeper collective
        realm="hiveeyes",
        # Beekeeper-ID
        network="testdrive",
        # Beehive location
        gateway="area42",
        # In my case: Not a hive but the gateway.
        node="array01",
    )
    # Define measurement for 30 sensors in 5x6 matrix
    measurement = {
        "temp-ir-1-1": matrix[0][0],
        "temp-ir-1-2": matrix[0][1],
        "temp-ir-1-3": matrix[0][2],
        "temp-ir-1-4": matrix[0][3],
        "temp-ir-1-5": matrix[0][4],
        "temp-ir-2-1": matrix[1][0],
        "temp-ir-2-2": matrix[1][1],
        "temp-ir-2-3": matrix[1][2],
        "temp-ir-2-4": matrix[1][3],
        "temp-ir-2-5": matrix[1][4],
        "temp-ir-3-1": matrix[2][0],
        "temp-ir-3-2": matrix[2][1],
        "temp-ir-3-3": matrix[2][2],
        "temp-ir-3-4": matrix[2][3],
        "temp-ir-3-5": matrix[2][4],
        "temp-ir-4-1": matrix[3][0],
        "temp-ir-4-2": matrix[3][1],
        "temp-ir-4-3": matrix[3][2],
        "temp-ir-4-4": matrix[3][3],
        "temp-ir-4-5": matrix[3][4],
        "temp-ir-5-1": matrix[4][0],
        "temp-ir-5-2": matrix[4][1],
        "temp-ir-5-3": matrix[4][2],
        "temp-ir-5-4": matrix[4][3],
        "temp-ir-5-5": matrix[4][4],
        "temp-ir-6-1": matrix[5][0],
        "temp-ir-6-2": matrix[5][1],
        "temp-ir-6-3": matrix[5][2],
        "temp-ir-6-4": matrix[5][3],
        "temp-ir-6-5": matrix[5][4],
    }
    # Serialize data as JSON
    payload = json.dumps(measurement)
    # Publish to MQTT
    pid = os.getpid()
    client_id = "{}:{}".format("mois-temp-matrix", str(pid))
    backend = mqtt.Client(client_id=client_id, clean_session=True)
    backend.username_pw_set(mqtt_user, mqtt_pass)
    backend.connect(mqtt_host, mqtt_port)
    backend.publish(mqtt_topic, payload)
    backend.disconnect()


def read_ds18b20_sensor_matrix():
    """
    Acquire measurement reading from an array matrix of DS18B20 sensors, connected to a Raspberry Pi machine.

    Make sure to use the correct configuration for your sensor setup.
    In order to research into it, use, for example:

        ls -la /sys/bus/w1/devices/
    """

    temp_ir_1_1 = temp_ir_1_2 = temp_ir_1_3 = temp_ir_1_4 = temp_ir_1_5 = None
    temp_ir_2_1 = temp_ir_2_2 = temp_ir_2_3 = temp_ir_2_4 = temp_ir_2_5 = None
    temp_ir_3_1 = temp_ir_3_2 = temp_ir_3_3 = temp_ir_3_4 = temp_ir_3_5 = None
    temp_ir_4_1 = temp_ir_4_2 = temp_ir_4_3 = temp_ir_4_4 = temp_ir_4_5 = None
    temp_ir_5_1 = temp_ir_5_2 = temp_ir_5_3 = temp_ir_5_4 = temp_ir_5_5 = None
    temp_ir_6_1 = temp_ir_6_2 = temp_ir_6_3 = temp_ir_6_4 = temp_ir_6_5 = None

    # Mount the device.
    os.system("modprobe w1-gpio")  # noqa: S605, S607
    os.system("modprobe w1-therm")  # noqa: S605, S607

    # Get all the filenames begin with 28 in the path base_dir.
    base_dir = "/sys/bus/w1/devices/"
    device_folders = glob.glob(base_dir + "28*")

    # print device_folders  # DEBUG

    for folder in device_folders:
        tc = read_temp(folder)
        label = "no_known_label"
        if folder == "/sys/bus/w1/devices/28-0346d4430b06":
            label = "temp-ir-1-1"
            temp_ir_1_1 = tc
        if folder == "/sys/bus/w1/devices/28-0cf3d443ba40":
            label = "temp-ir-1-2"
            temp_ir_1_2 = tc
        if folder == "/sys/bus/w1/devices/28-0e49d44343bd":
            label = "temp-ir-1-3"
            temp_ir_1_3 = tc
        if folder == "/sys/bus/w1/devices/28-11c1d443f241":
            label = "temp-ir-1-4"
            temp_ir_1_4 = tc
        if folder == "/sys/bus/w1/devices/28-1937d443bed6":
            label = "temp-ir-1-5"
            temp_ir_1_5 = tc
        if folder == "/sys/bus/w1/devices/28-2231d443d266":
            label = "temp-ir-2-1"
            temp_ir_2_1 = tc
        if folder == "/sys/bus/w1/devices/28-282bd4430f5e":
            label = "temp-ir-2-2"
            temp_ir_2_2 = tc
        if folder == "/sys/bus/w1/devices/28-2846d443e4f2":
            label = "temp-ir-2-3"
            temp_ir_2_3 = tc
        if folder == "/sys/bus/w1/devices/28-297ad443f622":
            label = "temp-ir-2-4"
            temp_ir_2_4 = tc
        if folder == "/sys/bus/w1/devices/28-2c6cd443ccf7":
            label = "temp-ir-2-5"
            temp_ir_2_5 = tc
        if folder == "/sys/bus/w1/devices/28-304ad4436d1a":
            label = "temp-ir-3-1"
            temp_ir_3_1 = tc
        if folder == "/sys/bus/w1/devices/28-32c9d443b51b":
            label = "temp-ir-3-2"
            temp_ir_3_2 = tc
        if folder == "/sys/bus/w1/devices/28-3ce1d443d148":
            label = "temp-ir-3-3"
            temp_ir_3_3 = tc
        if folder == "/sys/bus/w1/devices/28-400bd4439156":
            label = "temp-ir-3-4"
            temp_ir_3_4 = tc
        if folder == "/sys/bus/w1/devices/28-450ed4430afe":
            label = "temp-ir-3-5"
            temp_ir_3_5 = tc
        if folder == "/sys/bus/w1/devices/28-4694d44325ca":
            label = "temp-ir-4-1"
            temp_ir_4_1 = tc
        if folder == "/sys/bus/w1/devices/28-5196d4434d53":
            label = "temp-ir-4-2"
            temp_ir_4_2 = tc
        if folder == "/sys/bus/w1/devices/28-550cd4434596":
            label = "temp-ir-4-3"
            temp_ir_4_3 = tc
        if folder == "/sys/bus/w1/devices/28-57b6d44367cb":
            label = "temp-ir-4-4"
            temp_ir_4_4 = tc
        if folder == "/sys/bus/w1/devices/28-5821d44339c2":
            label = "temp-ir-4-5"
            temp_ir_4_5 = tc
        if folder == "/sys/bus/w1/devices/28-65f2d4434f51":
            label = "temp-ir-5-1"
            temp_ir_5_1 = tc
        if folder == "/sys/bus/w1/devices/28-6723d443b9ea":
            label = "temp-ir-5-2"
            temp_ir_5_2 = tc
        if folder == "/sys/bus/w1/devices/28-6755d443de81":
            label = "temp-ir-5-3"
            temp_ir_5_3 = tc
        if folder == "/sys/bus/w1/devices/28-6950d443323f":
            label = "temp-ir-5-4"
            temp_ir_5_4 = tc
        if folder == "/sys/bus/w1/devices/28-6ae6d4434899":
            label = "temp-ir-5-5"
            temp_ir_5_5 = tc
        if folder == "/sys/bus/w1/devices/28-6b2ad4437e19":
            label = "temp-ir-6-1"
            temp_ir_6_1 = tc
        if folder == "/sys/bus/w1/devices/28-6f8ad443a557":
            label = "temp-ir-6-2"
            temp_ir_6_2 = tc
        if folder == "/sys/bus/w1/devices/28-72d1d44362f0":
            label = "temp-ir-6-3"
            temp_ir_6_3 = tc
        if folder == "/sys/bus/w1/devices/28-72d8d44397f7":
            label = "temp-ir-6-4"
            temp_ir_6_4 = tc
        if folder == "/sys/bus/w1/devices/28-79d2d4430cf1":
            label = "temp-ir-6-5"  # noqa: F841
            temp_ir_6_5 = tc
    #    print ('%s %3.1f deg C %s' % (folder, tc, label))  # noqa: ERA001
    #    print ('%s %3.1f' % (label, tc))                   # noqa: ERA001
    matrix = [
        [temp_ir_1_1, temp_ir_1_2, temp_ir_1_3, temp_ir_1_4, temp_ir_1_5],
        [temp_ir_2_1, temp_ir_2_2, temp_ir_2_3, temp_ir_2_4, temp_ir_2_5],
        [temp_ir_3_1, temp_ir_3_2, temp_ir_3_3, temp_ir_3_4, temp_ir_3_5],
        [temp_ir_4_1, temp_ir_4_2, temp_ir_4_3, temp_ir_4_4, temp_ir_4_5],
        [temp_ir_5_1, temp_ir_5_2, temp_ir_5_3, temp_ir_5_4, temp_ir_5_5],
        [temp_ir_6_1, temp_ir_6_2, temp_ir_6_3, temp_ir_6_4, temp_ir_6_5],
    ]
    #  print (matrix)                                       # noqa: ERA001
    return matrix
