#!/bin/sh
#
# Setup and optionally run local HA server in virtual environment
# 


PYTHON_HOMEBREW=/opt/homebrew/bin/python3
if [ -e "$PYTHON_HOMEBREW" ]; then
    export PYTHON_BOOTSTRAP=$PYTHON_HOMEBREW
else
    export PYTHON_BOOTSTRAP=/usr/bin/python3
fi

echo "Creating virtual environment for HA"
$PYTHON_BOOTSTRAP -m venv .venv
.venv/bin/python3 -m pip install wheel
.venv/bin/python3 -m pip install homeassistant

echo "Creating config and symlinking custom_components"
.venv/bin/hass --script ensure_config -c .venv/config
(cd .venv/config; ln -s ../../custom_components)

if [ "$1" = "--execute" ]; then
    echo "Starting HA on localhost:8123"
    .venv/bin/hass -c .venv/config
fi