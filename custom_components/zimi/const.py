"""Constants for the zcc integration."""

from homeassistant.const import Platform

CONTROLLER = "zimi_controller"
DOMAIN = "zimi"
PLATFORMS = [
    Platform.COVER,
    Platform.FAN,
    Platform.LIGHT,
    Platform.SENSOR,
    Platform.SWITCH,
]
TITLE = "ZIMI Controller"
