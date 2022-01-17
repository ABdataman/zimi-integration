"""Platform for switch integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo

# Import the device class from the component that you want to support
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONTROLLER, DOMAIN
from .controller import ZimiController

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Zimi Switch platform."""

    controller: ZimiController = hass.data[CONTROLLER]

    entities = []

    # for key, device in controller.api.devices.items():
    for device in controller.controller.outlets:
        entities.append(ZimiSwitch(device))

    async_add_entities(entities)


class ZimiSwitch(SwitchEntity):
    """Representation of an Awesome Switch."""

    def __init__(self, switch) -> None:
        """Initialize an ZimiSwitch."""
        self._attr_unique_id = switch.identifier
        self._attr_should_poll = True
        self._switch = switch
        self._state = False
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, switch.identifier)},
            name=self._switch.name,
            suggested_area=self._switch.room,
        )
        self.update()
        _LOGGER.info("ZimiSwitch.__init__() for %s", self.name)

    @property
    def name(self) -> str:
        """Return the display name of this switch."""
        return self._name

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._state

    def turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on."""

        _LOGGER.info("ZimiSwitch.turn_on() for %s", self.name)

        self._switch.turn_on()

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""

        _LOGGER.info("ZimiSwitch.turn_off() for %s", self.name)

        self._switch.turn_off()

    def update(self) -> None:
        """Fetch new state data for this light."""

        self._name = self._switch.name
        self._state = self._switch.is_on()
