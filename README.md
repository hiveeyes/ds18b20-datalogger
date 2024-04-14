# temp-matrix
Temperature sensor matrix using Raspberry Pi, DS18B20, MQTT, Kotori DAQ,
and Grafana. For bee hive monitoring.

| View from outside | View from inside (sensor tip details) |
|:----:|:----:|
| ![Außen](https://community.hiveeyes.org/uploads/default/optimized/2X/f/f59f0149306b811f793627ec956c3e43c3758e51_2_334x500.jpeg)  | ![Innen](https://community.hiveeyes.org/uploads/default/optimized/2X/1/10f98dd272bd95940b311e22ef756114bd4efa04_2_333x500.jpeg) |


Lab protocol and development details:
https://community.hiveeyes.org/t/laborprotokoll-4x5-temp-matrix-mit-ds18b20/5102


## What's Inside
* README.md - this file
* LICENSE
* temp-matrix_5x6.py - sensor reading and data logging to hiveeyes
* temp-matrix_5x6-grafana_desktop.json - description of [Grafana Dashboard](https://swarm.hiveeyes.org/grafana/d/T49wHSaIk/mois-ex-wtf-test-ds18b20-5x6-temp-matrix-svg-pixmap?orgId=2&from=1712771622514&to=1712807415379)


## Setup
We recommend to install the program into a Python virtualenv.
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install 'ds18b20-datalogger @ git+https://github.com/hiveeyes/temp-matrix.git'
```

In this spirit, you keep the installation separate from your system Python, so
you can easily nuke it and start from scratch in case anything goes south.

Prerequisites: This program needs the `paho-mqtt` package.
https://pypi.org/project/paho-mqtt/#installation


## Operations

### Sensor Wiring
Be aware that you might have to adjust your resistors size.
With 30 sensors i had erratic sensor mapping using a 4.7k resistor.
I am getting valid mapping using a 2.2k resistor.

### Sensor Mapping
https://community.hiveeyes.org/t/ds18b20-temperatur-sensoren-am-one-wire-bus-anordnen/1399

### Data Publishing

    ssh youruser@yourpi
    screen
    cd temp-matrix
    source paho-mqtt/bin/activate
    python temp-matrix_5x6.py`

### MQTT data upload to Hiveeyes
https://community.hiveeyes.org/t/daten-per-mqtt-und-python-ans-backend-auf-swarm-hiveeyes-org-ubertragen/94/6

### Format your array
https://community.hiveeyes.org/t/how-to-visualize-2-dimensional-temperature-data-in-grafana/974/9

     matrix = [[temp_ir_1_1, temp_ir_1_2, temp_ir_1_3, temp_ir_1_4, temp_ir_1_5, temp_ir_1_6], \
          [temp_ir_2_1, temp_ir_2_2, temp_ir_2_3, temp_ir_2_4, temp_ir_2_5, temp_ir_2_6], \
          [temp_ir_3_1, temp_ir_3_2, temp_ir_3_3, temp_ir_3_4, temp_ir_3_5, temp_ir_3_6], \
          [temp_ir_4_1, temp_ir_4_2, temp_ir_4_3, temp_ir_4_4, temp_ir_4_5, temp_ir_4_6], \
          [temp_ir_5_1, temp_ir_5_2, temp_ir_5_3, temp_ir_5_4, temp_ir_5_5, temp_ir_5_6]]

## Data visualization in Grafana
https://swarm.hiveeyes.org/grafana/d/Y9PcgE4Sz/mois-ex-wtf-test-ir-sensor-svg-pixmap-copy

## Bonus: Sensor offsets
https://community.hiveeyes.org/t/temperatursensoren-justieren-kalibrieren/1744/2

## Contributing

In order to learn how to start hacking on this program, please have a look at the
documentation about how to install a [development sandbox](./docs/sandbox.md).

Contributions of any kind are always welcome and appreciated. Thank you.
