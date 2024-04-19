# Backlog for ds18b20-datalogger

## Iteration +1
- Documentation: How to set up Kotori DAQ
- Documentation: How to provision Grafana Dashboard

## Iteration +2
- By default, probe configuration at `/etc/ds18b20-datalogger/config.yaml`
- Add possibility to connect to MQTT/SSL

## Done
- Better software tests
- Break out sensor mapping configuration from code
  to make it re-usable across different setups
- Publish to PyPI
- Subcommand `make-dashboard`
- Subcommand `read`
- Test coverage 100%
- Improve documentation
