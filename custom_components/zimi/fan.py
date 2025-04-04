"""Platform for fan integration."""

from __future__ import annotations

import logging
import math
from typing import Any

from zcc import ControlPoint
from zcc.device import ControlPointDevice

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.core import HomeAssistant

# Import the device class from the component that you want to support
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.percentage import (
    percentage_to_ranged_value,
    ranged_value_to_percentage,
)
from homeassistant.util.scaling import int_states_in_range

from . import ZimiConfigEntry
from .entity import ZimiEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ZimiConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Zimi Cover platform."""

    api: ControlPoint = config_entry.runtime_data

    fans: list[ZimiFan] = [ZimiFan(device, api) for device in api.fans]

    async_add_entities(fans)


class ZimiFan(ZimiEntity, FanEntity):
    """Representation of a Zimi fan."""

    _attr_supported_features = (
        FanEntityFeature.SET_SPEED
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.TURN_ON
    )

    def __init__(self, device: ControlPointDevice, api: ControlPoint) -> None:
        """Initialize an ZimiFan."""

        super().__init__(device, api)

        _LOGGER.debug(
            "Initialising ZimiFan %s in %s", self._entity.name, self._entity.room
        )

        self._speed = self._entity.fanspeed

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the desired speed for the fan."""
        _LOGGER.debug(
            "Sending async_set_percentage() with percentage %s", percentage)

        if percentage == 0:
            await self.async_turn_off()
            return

        target_speed = math.ceil(
            percentage_to_ranged_value(self._speed_range, percentage)
        )
        _LOGGER.debug(
            "async_set_percentage() converted percentage %s to speed %s",
            percentage,
            target_speed,
        )

        await self._entity.set_fanspeed(target_speed)

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Instruct the fan to turn on."""

        _LOGGER.debug("Sending turn_on() for %s", self.name)
        await self._entity.turn_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the fan to turn off."""

        _LOGGER.debug("Sending turn_off() for %s", self.name)
        await self._entity.turn_off()

    @property
    def percentage(self) -> int:
        """Return the current speed percentage for the fan."""
        if not self._entity.fanspeed:
            return 0
        return ranged_value_to_percentage(self._speed_range, self._entity.fanspeed)

    @property
    def _speed_range(self) -> tuple[int, int]:
        """Return the range of speeds."""
        return (0, 7)

    @property
    def speed_count(self) -> int:
        """Return the number of speeds the fan supports."""
        return int_states_in_range(self._speed_range)
