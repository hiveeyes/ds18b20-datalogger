# Production Setup

A walkthrough how to install the program on a Raspberry Pi machine running
Linux. In order to learn about more details, please also consult the [README]
document.

## Installation
```shell
sudo su -
python3 -m venv /opt/ds18b20-datalogger
/opt/ds18b20-datalogger/bin/pip install ds18b20-datalogger
/opt/ds18b20-datalogger/bin/ds18b20-datalogger make-config > /etc/ds18b20-datalogger/config.yaml
/opt/ds18b20-datalogger/bin/ds18b20-datalogger run /etc/ds18b20-datalogger/config.yaml
```

We recommend to install the program into a Python virtualenv.
In this spirit, you keep the installation separate from your system Python, so
you can easily nuke it and start from scratch in case anything goes south.

## Periodic Measurements
If you want to run the program periodically, for example each five minutes, use
Cron or, alternatively, Systemd Timers.

### Cron
This should go into `/etc/cron.d/ds18b20-datalogger`.
```
*/5 * * * *  root  /opt/ds18b20-datalogger/bin/ds18b20-datalogger run /etc/ds18b20-datalogger/config.yaml
```

### Systemd Timers

This should go into `/etc/systemd/system/ds18b20-datalogger.service`.
```ini
# Systemd service unit file for ds18b20-datalogger.
# https://github.com/hiveeyes/ds18b20-datalogger

[Unit]
Description=DS18B20 data logger
Wants=ds18b20-datalogger.timer

[Service]
Type=oneshot
ExecStart=/opt/ds18b20-datalogger/bin/ds18b20-datalogger run /etc/ds18b20-datalogger/config.yaml

[Install]
WantedBy=multi-user.target
```

This should go into `/etc/systemd/system/ds18b20-datalogger.timer`.
```ini
# Systemd timer unit file for ds18b20-datalogger.
# https://github.com/hiveeyes/ds18b20-datalogger

[Unit]
Description=DS18B20 data logger
Requires=ds18b20-datalogger.service

[Timer]
Unit=ds18b20-datalogger.service
OnCalendar=*-*-* *:0/5

[Install]
WantedBy=timers.target
```

Start and enable the service and the timer units.
```shell
systemctl start ds18b20-datalogger.service
systemctl enable ds18b20-datalogger.timer
systemctl list-timers
```


[README]: https://github.com/hiveeyes/ds18b20-datalogger/blob/main/README.md
[Systemd Timers]: https://opensource.com/article/20/7/systemd-timers
