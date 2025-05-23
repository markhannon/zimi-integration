"""Platform for switch integration."""

from __future__ import annotations

import logging
from typing import Any

from zcc import ControlPoint
from zcc.device import ControlPointDevice

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.core import HomeAssistant

# Import the device class from the component that you want to support
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import ZimiConfigEntry
from .entity import ZimiEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ZimiConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Zimi Switch platform."""

    api: ControlPoint = config_entry.runtime_data

    outlets: list[ZimiSwitch] = [ZimiSwitch(
        device, api) for device in api.outlets]

    async_add_entities(outlets)


class ZimiSwitch(ZimiEntity, SwitchEntity):
    """Representation of an Zimi Switch."""

    _attr_device_class = SwitchDeviceClass.SWITCH
    _attr_icon = "mdi:power-socket-au"

    def __init__(self, device: ControlPointDevice, api: ControlPoint) -> None:
        """Initialize an ZimiSwitch."""

        super().__init__(device, api)

        _LOGGER.debug(
            "Initialising ZimiSwitch %s in %s", self._entity.name, self._entity.room
        )

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._entity.is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Instruct the switch to turn on."""

        _LOGGER.debug(
            "Sending turn_on() for %s in %s", self._entity.name, self._entity.room
        )

        await self._entity.turn_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the switch to turn off."""

        _LOGGER.debug(
            "Sending turn_off() for %s in %s", self._entity.name, self._entity.room
        )

        await self._entity.turn_off()
