# Zimi Controller

_Component to integrate with Zimi Controller and associated devices.

**This component will set up the following platforms.**

Platform | Description
-- | --
`cover` | Open or close a cover (typically garage door).
`light` | Switch a light on or off.
`switch` | Switch a switch on or off.


## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `integration_blueprint`.
4. Download _all_ the files from the `custom_components/integration_blueprint/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Integration blueprint"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/zimi/translations/en.json
custom_components/zimi/__init__.py
custom_components/zimi/config_flow.py
custom_components/zimi/const.py
custom_components/zimi/cover.py
custom_components/zimi/light.py
custom_components/zimi/manifest.json
custom_components/zimi/strings.json
custom_components/zimi/switch.py
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***
