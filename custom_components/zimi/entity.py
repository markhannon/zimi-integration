"""Base entity for zimi integrations."""

from __future__ import annotations

import logging

from zcc import ControlPoint
from zcc.device import ControlPointDevice

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ZimiEntity(Entity):
    """Representation of a Zimi API entity."""

    _attr_should_poll = False
    _attr_has_entity_name = False

    def __init__(self, entity: ControlPointDevice, api: ControlPoint) -> None:
        """Initialize an HA Entity which is a ZimiDevice."""

        self._entity = entity
        self._attr_unique_id = self._entity.identifier
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._entity.manufacture_info.identifier)},
            name=self._entity.manufacture_info.model,
            manufacturer=self._entity.manufacture_info.manufacturer,
            model=f"hwVersion={self._entity.manufacture_info.hwVersion}",
            hw_version=self._entity.manufacture_info.hwVersion,
            sw_version=self._entity.manufacture_info.firmwareVersion,
            suggested_area=self._entity.room,
            via_device=(DOMAIN, api.mac),
        )
        self._attr_name = self._entity.name.strip()
        self._attr_suggested_area = self._entity.room

    @property
    def available(self) -> bool:
        """Return True if Home Assistant is able to read the state and control the underlying device."""
        return self._entity.is_connected

    async def async_added_to_hass(self) -> None:
        """Subscribe to the events."""
        await super().async_added_to_hass()
        self._entity.subscribe(self)

    async def async_will_remove_from_hass(self) -> None:
        """Cleanup ZimiLight with removal of notification prior to removal."""
        self._entity.unsubscribe(self)
        await super().async_will_remove_from_hass()

    def notify(self, _observable: object):
        """Receive notification from device that state has changed.

        No data is fetched for the notification but schedule_update_ha_state is called.
        """

        _LOGGER.debug(
            "Received notification() for %s in %s", self._entity.name, self._entity.room
        )
        self.schedule_update_ha_state(force_refresh=True)
