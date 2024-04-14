from ds18b20_datalogger.core import read_ds18b20_sensor_matrix, send_measurement_mqtt


def main():
    reading = read_ds18b20_sensor_matrix()
    send_measurement_mqtt(reading)
    # print(strftime("%Y-%m-%d %H:%M:%S", time.localtime())," Done sending. Going to sleep for 15min.")   # noqa: ERA001
