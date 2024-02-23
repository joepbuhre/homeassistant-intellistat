"""The better_thermostat component."""

import logging
from asyncio import Lock
from random import random
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, Config
from homeassistant.config_entries import ConfigEntry


async def async_setup(hass, config):
    hass.states.async_set("intellistat.world", f"Paulus_{random()}")

    # Return boolean to indicate that initialization was successful.
    return True