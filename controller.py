"""Zimi Controller wrapper class device."""
import logging
import pprint

from zcc import ControlPoint, ControlPointError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, PLATFORMS


class ZimiController:
    """Manages a single Zimi Controller hub."""

    def __init__(self, hass: HomeAssistant, config: ConfigEntry) -> None:
        """Initialize."""
        self.controller: ControlPoint = None
        self.hass = hass
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.logger.info("ZimiController.__init() %s", pprint.pformat(self.config))

        # store (this) bridge object in hass data
        hass.data.setdefault(DOMAIN, {})[self.config.entry_id] = self

    @property
    def host(self) -> str:
        """Return the host of this hub."""
        return self.config.data[CONF_HOST]

    @property
    def port(self) -> int:
        """Return the host of this hub."""
        return self.config.data[CONF_PORT]

    def connect(self) -> bool:
        """Initialize Connection with the Zimi Controller."""
        try:
            self.logger.info("ControlPoint inititation starting")
            self.controller = ControlPoint(host=self.host, port=self.port)
            self.logger.info("ControlPoint inititation completed")
            self.logger.info("\n%s", self.controller.describe())
        except ControlPointError as error:
            raise ConfigEntryNotReady(
                "ControlPoint initiation failed:" + error
            ) from error

        if self.controller:
            self.hass.config_entries.async_setup_platforms(self.config, PLATFORMS)

        return True
