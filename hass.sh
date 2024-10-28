#!/bin/sh
#
# Setup and optionally run local HA server in virtual environment
# 

echo "Creating virtual environment for HA"
/opt/homebrew/bin/python3 -m venv .venv
.venv/bin/python3 -m pip install wheel
.venv/bin/python3 -m pip install homeassistant

echo "Creating config and symlinking custom_components"
.venv/bin/hass --script ensure_config -c .venv/config
(cd .venv/config; ln -s ../../custom_components)

if [ "$1" == "--execute" ]; then
    echo "Starting HA on localhost:8123"
    .venv/bin/hass -c .venv/config
fi