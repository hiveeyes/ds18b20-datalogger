# Measurement reading and publishing for mois

```shell
ssh youruser@yourpi
screen
source /path/to/ds18b20-datalogger/.venv/bin/activate
wget https://github.com/hiveeyes/ds18b20-datalogger/raw/main/etc/mois.yaml
ds18b20-datalogger run mois.yaml
```
