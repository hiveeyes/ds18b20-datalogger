# Development Sandbox

## Install
Acquire the source code from the repository, install a Python virtualenv,
and install the package in development mode.
```shell
git clone https://github.com/hiveeyes/ds18b20-datalogger
cd ds18b20-datalogger
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade --editable='.[develop,docs,release,test]'
```

We recommend to install the program into a Python virtualenv.
In this spirit, you keep the installation separate from your system Python, so
you can easily nuke it and start from scratch in case anything goes south.


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
