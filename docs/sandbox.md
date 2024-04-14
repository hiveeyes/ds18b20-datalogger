# Development Sandbox

## Install
```shell
git clone https://github.com/hiveeyes/ds18b20-datalogger
python3 -m venv .venv
source .venv/bin/activate
pip install --editable='.[develop,docs,release,test]'
```

## Software tests
Run all linters, and invoke the test suite.
```shell
poe check
```

## Format code
Run all code formatters.
```shell
poe format
```
