"""Platform for cover integration."""

from __future__ import annotations

import logging
from typing import Any

from zcc import ControlPoint
from zcc.device import ControlPointDevice

from homeassistant.components.cover import (
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
)
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
    """Set up the Zimi Cover platform."""

    api: ControlPoint = config_entry.runtime_data

    doors: list[ZimiCover] = [ZimiCover(device, api) for device in api.doors]

    async_add_entities(doors)


class ZimiCover(ZimiEntity, CoverEntity):
    """Representation of a Zimi cover."""

    _attr_device_class = CoverDeviceClass.GARAGE
    _attr_supported_features = (
        CoverEntityFeature.OPEN
        | CoverEntityFeature.CLOSE
        | CoverEntityFeature.SET_POSITION
        | CoverEntityFeature.STOP
    )

    def __init__(self, device: ControlPointDevice, api: ControlPoint) -> None:
        """Initialize an Zimicover."""

        super().__init__(device, api)

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close the cover/door."""
        _LOGGER.debug("Sending close_cover() for %s", self.name)
        await self._entity.close_door()

    @property
    def current_cover_position(self) -> int | None:
        """Return the current cover/door position."""
        _LOGGER.debug("current_cover_position() = %d for %s",
                      self._entity.percentage, self.name)
        return self._entity.percentage

    @property
    def is_closed(self) -> bool | None:
        """Return true if cover is closed."""
        _LOGGER.debug("is_closed() = %d (%d) for %s",
                      self._entity.is_closed, self._entity.percentage, self.name)
        return self._entity.is_closed

    @property
    def is_closing(self) -> bool | None:
        """Return true if cover is closing."""
        _LOGGER.debug("is_closing() = %d (%d) for %s",
                      self._entity.is_closing, self._entity.percentage, self.name)
        return self._entity.is_closing

    @property
    def is_opening(self) -> bool | None:
        """Return true if cover is opening."""
        _LOGGER.debug("is_opening() = %d (%d) for %s",
                      self._entity.is_opening, self._entity.percentage, self.name)
        return self._entity.is_opening

    @property
    def is_open(self) -> bool | None:
        """Return true if cover is open."""
        _LOGGER.debug("is_open() = %d (%d) for %s",
                      self._entity.is_open, self._entity.percentage, self.name)
        return self._entity.is_open

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open the cover/door."""
        _LOGGER.debug("Sending open_cover() for %s", self.name)
        await self._entity.open_door()

    async def async_set_cover_position(self, **kwargs: Any) -> None:
        """Open the cover/door to a specified percentage."""
        if position := kwargs.get("position"):
            _LOGGER.debug("Sending set_cover_position(%d) for %s",
                          position, self.name)
            await self._entity.open_to_percentage(position)

    async def async_stop_cover(self, **kwargs: Any) -> None:
        """Stop the cover."""
        _LOGGER.debug(
            "Stopping open_cover() by setting to current position for %s", self.name
        )
        await self.async_set_cover_position(position=self.current_cover_position)
