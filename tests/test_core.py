from ds18b20_datalogger.core import read_ds18b20_sensor_matrix, send_measurement_mqtt


def test_sensors():
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
