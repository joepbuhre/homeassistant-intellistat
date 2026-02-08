
import logging

from homeassistant.const import (
    ATTR_TEMPERATURE,
    CONF_DOMAIN,
    CONF_SERVICE,
    ATTR_SERVICE_DATA,
    CONF_TARGET,
    CONF_ENTITY_ID,
    SERVICE_TURN_ON,
    SERVICE_TURN_OFF,
    STATE_ON,
    Platform,
)
from homeassistant.components.climate.const import (
    ATTR_HVAC_MODE,
    ATTR_CURRENT_TEMPERATURE,
    ATTR_TARGET_TEMP_LOW,
    ATTR_HVAC_ACTION,
    HVACMode,
    HVACAction,
    SERVICE_SET_HVAC_MODE,
    SERVICE_SET_TEMPERATURE,
)
from homeassistant.core import (
    HomeAssistant,State
)

_LOGGER = logging.getLogger(__name__)


def parse_state(state: State):
    data = {}

    for key in [ATTR_TEMPERATURE, ATTR_TARGET_TEMP_LOW, ATTR_CURRENT_TEMPERATURE, ATTR_HVAC_ACTION]:
        data[key] = state.attributes.get(key) if state and state.attributes else None
    
    if ATTR_TARGET_TEMP_LOW in data and data[ATTR_TARGET_TEMP_LOW] is not None and data[ATTR_TARGET_TEMP_LOW] > 0:
        _LOGGER.debug(f"Found that attr target temp low was in dict changing now")
        data[ATTR_TEMPERATURE] = data[ATTR_TARGET_TEMP_LOW]

    data[ATTR_HVAC_MODE] = state.state if state else None

    if data[ATTR_HVAC_ACTION] is None:
        if (
            data[ATTR_TEMPERATURE] is not None and
            data[ATTR_CURRENT_TEMPERATURE] is not None and
            data[ATTR_HVAC_MODE] in [HVACMode.OFF, HVACMode.HEAT]
        ):
            if data[ATTR_HVAC_MODE] == HVACMode.OFF:
                data[ATTR_HVAC_ACTION] = HVACAction.OFF
            elif data[ATTR_TEMPERATURE] > data[ATTR_CURRENT_TEMPERATURE]:
                data[ATTR_HVAC_ACTION] = HVACAction.HEATING
            else:
                data[ATTR_HVAC_ACTION] = HVACAction.IDLE
        else:
            data[ATTR_HVAC_ACTION] = HVACAction.OFF

    if data[ATTR_TEMPERATURE] is None and data[ATTR_TARGET_TEMP_LOW] is None:
        _LOGGER.debug("\n\nParsed state")
        _LOGGER.debug(state)
        _LOGGER.debug(data)
        _LOGGER.debug(state)
        _LOGGER.debug("\n\n\n")


    return data


async def async_set_hvac_mode(hass: HomeAssistant, entity_ids, hvac_mode: str):
    """helper for setting hvac_mode"""
    params = {
        CONF_DOMAIN: Platform.CLIMATE,
        CONF_SERVICE: SERVICE_SET_HVAC_MODE,
        ATTR_SERVICE_DATA: {
            ATTR_HVAC_MODE: hvac_mode
        },
        CONF_TARGET: {
            CONF_ENTITY_ID: entity_ids
        }
    }
    service_task = hass.async_create_task(
        hass.services.async_call(
            **params,
            blocking=True,
            context={},
        )
    )
    await service_task


async def async_set_temperature(hass: HomeAssistant, entity_ids, temperature: float):
    """helper for setting temperature setpoint"""
    params = {
        CONF_DOMAIN: Platform.CLIMATE,
        CONF_SERVICE: SERVICE_SET_TEMPERATURE,
        ATTR_SERVICE_DATA: {
            ATTR_TEMPERATURE: temperature
        },
        CONF_TARGET: {
            CONF_ENTITY_ID: entity_ids
        }
    }
    service_task = hass.async_create_task(
        hass.services.async_call(
            **params,
            blocking=True,
            context={},
        )
    )
    await service_task


async def async_set_switch_state(hass: HomeAssistant, entity_ids, state: str):
    """helper for setting switch state"""
    params = {
        CONF_DOMAIN: Platform.SWITCH,
        CONF_SERVICE: SERVICE_TURN_ON if state == STATE_ON else SERVICE_TURN_OFF,
        ATTR_SERVICE_DATA: {
        },
        CONF_TARGET: {
            CONF_ENTITY_ID: entity_ids
        }
    }
    service_task = hass.async_create_task(
        hass.services.async_call(
            **params,
            blocking=True,
            context={},
        )
    )
    await service_task


def compute_domain(entity_id: str):
    return entity_id.split(".").pop(0)
