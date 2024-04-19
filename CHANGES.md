# Changes for ds18b20-datalogger

## Unreleased
- Tests: Make sensor tests work, using a fake sysfs filesystem
- Tests: Add basic test case for CLI interface
- Remove support for Python 3.7
- Define MQTT and sensor configuration separately from implementation.
  The data logger uses a YAML file now, for example like `etc/mois.yaml`.
- Added subcommand `make-config`, for creating a configuration blueprint
- Added subcommand `make-dashboard`, for creating a Grafana Dashboard

## v0.0.2 - 2024-04-15
- Publish as `ds18b20-datalogger` package

## v0.0.1 - 2024-04-14
- Make it work, and add documentation.
