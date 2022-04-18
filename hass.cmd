
echo "Creating virtual environment for HA"
python -m venv .venv
.venv\Scripts\python.exe -m pip install wheel
.venv\Scripts\python.exe -m pip install homeassistant

echo "Creating config and symlinking custom_components"
.venv/bin/hass --script ensure_config -c .venv/config

cd .venv/config
mklink /d  custom_components ../../custom_components
cd ../..

echo "Starting HA"
.venv/bin/hass -c .venv/config