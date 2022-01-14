"""Platform for cover integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.cover import (
    ATTR_CURRENT_POSITION,
    DEVICE_CLASS_GARAGE,
    STATE_CLOSED,
    STATE_CLOSING,
    STATE_OPEN,
    STATE_OPENING,
    SUPPORT_CLOSE,
    SUPPORT_OPEN,
    SUPPORT_SET_POSITION,
    CoverEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

# Import the device class from the component that you want to support
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONTROLLER
from .controller import ZimiController

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Zimi Cover platform."""

    controller: ZimiController = hass.data[CONTROLLER]

    entities = []

    # for key, device in controller.api.devices.items():
    for device in controller.controller.doors:
        entities.append(ZimiCover(device))

    async_add_entities(entities)


class ZimiCover(CoverEntity):
    """Representation of an Awesome cover."""

    def __init__(self, cover) -> None:
        """Initialize an Zimicover."""
        self._attr_unique_id = cover.identifier
        self._attr_should_poll = True
        self._attr_device_class = DEVICE_CLASS_GARAGE
        self._attr_supported_features = (
            SUPPORT_SET_POSITION & SUPPORT_CLOSE & SUPPORT_OPEN
        )
        self._cover = cover
        self._state = STATE_CLOSED
        self._position = None
        self.update()
        _LOGGER.info("ZimiCover.__init__() for %s", self.name)

    def close_cover(self, **kwargs: Any) -> None:
        """Close the cover/door."""
        _LOGGER.info("ZimiCover.close_cover() for %s", self.name)
        self._cover.close_door()

    @property
    def current_cover_position(self) -> int | None:
        """Return the current cover/door position."""
        return self._position

    @property
    def is_closed(self) -> bool | None:
        """Return true if cover is closed."""
        return True if self._state == STATE_CLOSED else False

    @property
    def is_closing(self) -> bool | None:
        """Return true if cover is closing."""
        return True if self._state == STATE_CLOSING else False

    @property
    def is_opening(self) -> bool | None:
        """Return true if cover is opening."""
        return True if self._state == STATE_OPENING else False

    @property
    def is_open(self) -> bool | None:
        """Return true if cover is open."""
        return True if self._state == STATE_OPEN else False

    @property
    def name(self) -> str:
        """Return the display name of this cover."""
        return self._name

    def open_cover(self, **kwargs: Any) -> None:
        """Open the cover/door."""
        _LOGGER.info("ZimiCover.open_cover() for %s", self.name)
        self._cover.open_door()

    def set_cover_position(self, **kwargs):
        """Open the cover/door to a specified percentage."""
        position = kwargs.get(ATTR_CURRENT_POSITION, None)
        if position:
            _LOGGER.info("ZimiCover.set_cover_position(%d) for %s", position, self.name)
            self._cover.open_to_percentage(position)

    def update(self) -> None:
        """Fetch new state data for this cover."""

        self._name = (
            self._cover.properties.get("name", "-")
            + "/"
            + self._cover.properties.get("roomName", "-")
        )
        self._position = self._cover.percentage
        if self._cover.is_closed:
            self._state = STATE_CLOSED
        elif self._cover.is_open:
            self._state = STATE_OPEN
        elif self._cover.is_opening:
            self._state = STATE_OPENING
        else:
            self._state = STATE_CLOSING
