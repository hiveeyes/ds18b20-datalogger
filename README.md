# ds18b20-datalogger

A data logger specializing in reading an array of DS18B20 sensors.

A temperature sensor matrix with heatmap visualization for bee hive monitoring,
using Raspberry Pi, Linux, Python, DS18B20, MQTT, Kotori DAQ, and Grafana.


| View from outside | View from inside (sensor tip details) |
|:----:|:----:|
| ![Außen](https://community.hiveeyes.org/uploads/default/optimized/2X/f/f59f0149306b811f793627ec956c3e43c3758e51_2_334x500.jpeg)  | ![Innen](https://community.hiveeyes.org/uploads/default/optimized/2X/1/10f98dd272bd95940b311e22ef756114bd4efa04_2_333x500.jpeg) |


Lab protocol and development details:
https://community.hiveeyes.org/t/laborprotokoll-4x5-temp-matrix-mit-ds18b20/5102


## Project Information

» [Documentation]
| [Changelog]
| [PyPI]
| [Issues]
| [Source code]
| [License]

[![CI][badge-tests]][project-tests]
[![Coverage Status][badge-coverage]][project-codecov]
[![License][badge-license]][project-license]
[![Downloads per month][badge-downloads-per-month]][project-downloads]

[![Supported Python versions][badge-python-versions]][project-pypi]
[![Status][badge-status]][project-pypi]
[![Package version][badge-package-version]][project-pypi]


## What's Inside

- The `ds18b20-datalogger` program, reading DS18B20 sensors and
  publishing readings to MQTT in JSON format.
- Configuration file in YAML format, like [`datalogger.yaml`].
- JSON representation for a corresponding Grafana Dashboard
  [`grafana-dashboard.json`], when measurement data is submitted
  and acquired through [Kotori DAQ].


## Synopsis
Acquire single reading, and echo it on STDOUT in JSON format.
```shell
ds18b20-datalogger read datalogger.yaml
```

Take a single reading, and publish it to the configured MQTT topic.
```shell
ds18b20-datalogger run datalogger.yaml
```

## Live
In order to see a running system in action, please enjoy inspecting the
[Live Grafana Dashboard].


## Installation
Install the `ds18b20-datalogger` package from PyPI using `pip`.
```shell
pip install --upgrade ds18b20-datalogger
```
See also alternative installation methods and hands-on walkthroughs at
[development sandbox] and [production setup].

## Configuration
In order to operate the data logger successfully, you will need to configure
two important details:

- Sensors: Map one-wire sensor sysfs paths to self-assigned sensor names.
- Telemetry: Adjust MQTT connection settings and MQTT topic.

You can create a blueprint configuration file by using the `make-config`
subcommand.
```shell
ds18b20-datalogger make-config > datalogger.yaml
```

### Appliance: Sensor Wiring and Sensor Mapping

Be aware that you might have to adjust your resistors size.
With 30 sensors i had erratic sensor mapping using a 4.7k resistor.
I am getting valid mapping using a 2.2k resistor.

Please read more about [sensor mapping] on our community forum. In practice,
just edit the `one-wire` section within the configuration file according to
your setup.

### Backend: Telemetry and Visualization

The data logger will publish measurements to an MQTT topic, where [Kotori DAQ]
can pick it up, in order to converge into a timeseries database, and displays
it on a Grafana Dashboard.

The package includes a corresponding Grafana Dashboard, which can be created
by invoking the `make-dashboard` subcommand.

```shell
ds18b20-datalogger make-dashboard > dashboard.json
```

On our community forum, you can find relevant discussions about this topic.

- [MQTT data upload to Hiveeyes]
- [Data visualization in Grafana]
- [Sensor offsets] (optional)


## Acknowledgements

The original code this implementation has been derived from has been discovered
on the element14 community forum at [Multiple DS18B20 Temp sensors interfacing
with Raspberry Pi], shared by [@laluha]. Thanks!


## Contributing

In order to learn how to start hacking on this program, please have a look at the
documentation about how to install a [development sandbox].

Contributions of any kind are always welcome and appreciated. Thank you.



[@laluha]: https://github.com/laluha
[`datalogger.yaml`]: https://github.com/hiveeyes/ds18b20-datalogger/raw/main/ds18b20_datalogger/datalogger.yaml
[Data visualization in Grafana]: https://swarm.hiveeyes.org/grafana/d/Y9PcgE4Sz/mois-ex-wtf-test-ir-sensor-svg-pixmap-copy
[`grafana-dashboard.json`]: https://github.com/hiveeyes/ds18b20-datalogger/raw/main/ds18b20_datalogger/grafana-dashboard.json
[Kotori DAQ]: https://kotori.readthedocs.io
[Live Grafana Dashboard]: https://swarm.hiveeyes.org/grafana/d/T49wHSaIk/mois-ex-wtf-test-ds18b20-5x6-temp-matrix-svg-pixmap?orgId=2&from=1712771622514&to=1712807415379
[MQTT data upload to Hiveeyes]: https://community.hiveeyes.org/t/daten-per-mqtt-und-python-ans-backend-auf-swarm-hiveeyes-org-ubertragen/94/6
[Multiple DS18B20 Temp sensors interfacing with Raspberry Pi]: https://community.element14.com/products/raspberry-pi/raspberrypi_projects/b/blog/posts/multiple-ds18b20-temp-sensors-interfacing-with-raspberry-pi?CommentId=9470e4e9-b054-4dd3-9a3f-ac9d1fe38087
[Sensor offsets]: https://community.hiveeyes.org/t/temperatursensoren-justieren-kalibrieren/1744/2
[sensor mapping]: https://community.hiveeyes.org/t/ds18b20-temperatur-sensoren-am-one-wire-bus-anordnen/1399

[Changelog]: https://github.com/hiveeyes/ds18b20-datalogger/blob/main/CHANGES.md
[development sandbox]: https://github.com/hiveeyes/ds18b20-datalogger/blob/main/docs/sandbox.md
[Documentation]: https://ds18b20-datalogger.readthedocs.io/
[Issues]: https://github.com/hiveeyes/ds18b20-datalogger/issues
[License]: https://github.com/hiveeyes/ds18b20-datalogger/blob/main/LICENSE
[production setup]: https://github.com/hiveeyes/ds18b20-datalogger/blob/main/docs/production.md
[PyPI]: https://pypi.org/project/ds18b20-datalogger/
[Source code]: https://github.com/hiveeyes/ds18b20-datalogger

[badge-coverage]: https://codecov.io/gh/hiveeyes/ds18b20-datalogger/branch/main/graph/badge.svg
[badge-downloads-per-month]: https://pepy.tech/badge/ds18b20-datalogger/month
[badge-license]: https://img.shields.io/github/license/hiveeyes/ds18b20-datalogger.svg
[badge-package-version]: https://img.shields.io/pypi/v/ds18b20-datalogger.svg
[badge-python-versions]: https://img.shields.io/pypi/pyversions/ds18b20-datalogger.svg
[badge-status]: https://img.shields.io/pypi/status/ds18b20-datalogger.svg
[badge-tests]: https://github.com/hiveeyes/ds18b20-datalogger/actions/workflows/tests.yml/badge.svg
[project-codecov]: https://codecov.io/gh/hiveeyes/ds18b20-datalogger
[project-downloads]: https://pepy.tech/project/ds18b20-datalogger/
[project-license]: https://github.com/hiveeyes/ds18b20-datalogger/blob/main/LICENSE
[project-pypi]: https://pypi.org/project/ds18b20-datalogger
[project-tests]: https://github.com/hiveeyes/ds18b20-datalogger/actions/workflows/tests.yml
