
echo "Creating virtual environment for HA"
python -m venv .venv
.venv\Scripts\python.exe -m pip install wheel
.venv\Scripts\python.exe -m pip install homeassistant

echo "Creating config and symlinking custom_components"
.venv/bin/hass --script ensure_config -c .venv/config

cd .venv/config
mklink /d  custom_components ../../custom_components
cd ../..

IF "%1"=="--execute" (
    echo "Starting HA on localhost:8123"
    .venv/bin/hass -c .venv/config
)