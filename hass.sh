#!/bin/sh

# 
# Run local HA server in virtual environment

echo "Creating virtual environment for HA"
/opt/homebrew/bin/python3 -m venv .venv
.venv/bin/python3 -m pip install wheel
.venv/bin/python3 -m pip install homeassistant

echo "Creating config and symlinking custom_components"
.venv/bin/hass --script ensure_config -c .venv/config
(cd .venv/config; ln -s ../../custom_components)

echo "Starting HA"
.venv/bin/hass -c .venv/config