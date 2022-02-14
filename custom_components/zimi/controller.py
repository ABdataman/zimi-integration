"""Zimi Controller wrapper class device."""
import logging
import pprint

from zcc import ControlPoint, ControlPointError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DEBUG, DOMAIN, PLATFORMS, TIMEOUT


class ZimiController:
    """Manages a single Zimi Controller hub."""

    def __init__(self, hass: HomeAssistant, config: ConfigEntry) -> None:
        """Initialize."""
        self.controller: ControlPoint = None
        self.hass = hass
        self.config = config

        self.logger = logging.getLogger(__name__)
        if config.data.get("debug", False):
            self.logger.setLevel(logging.DEBUG)

        self.logger.debug("__init() %s", pprint.pformat(self.config))

        # store (this) bridge object in hass data
        hass.data.setdefault(DOMAIN, {})[self.config.entry_id] = self

    @property
    def debug(self) -> bool:
        """Return the debug flag for this hub."""
        return self.config.data.get(DEBUG, False)

    @property
    def host(self) -> str:
        """Return the host of this hub."""
        return self.config.data[CONF_HOST]

    @property
    def port(self) -> int:
        """Return the host of this hub."""
        return self.config.data[CONF_PORT]

    @property
    def timeout(self) -> int:
        """Return the timeout of this hub."""
        if self.config.data[TIMEOUT] == 0:
            self.config.data[TIMEOUT] = 3
        return self.config.data[TIMEOUT]

    def connect(self) -> bool:
        """Initialize Connection with the Zimi Controller."""
        try:
            self.logger.info(
                "ControlPoint inititation starting to %s:%d with debug=%s and timeout=%d",
                self.host,
                self.port,
                self.debug,
                self.timeout,
            )
            if self.host != "":
                self.controller = ControlPoint(
                    host=self.host,
                    port=self.port,
                    verbose=True,
                    debug=self.debug,
                    timeout=self.timeout,
                )
            else:
                self.controller = ControlPoint(
                    verbose=True, debug=self.debug, timeout=self.timeout)
            self.logger.info("ControlPoint inititation completed")
            self.logger.info("\n%s", self.controller.describe())
        except ControlPointError as error:
            self.logger.info("ControlPoint initiation failed")
            raise ConfigEntryNotReady(error) from error

        if self.controller:
            self.hass.config_entries.async_setup_platforms(
                self.config, PLATFORMS)

        return True
