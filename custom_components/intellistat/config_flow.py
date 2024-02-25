"""Config flow for the Intellistat component."""
from collections import OrderedDict
import secrets
import logging
from typing import Any, Dict, List
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import UnitOfTemperature
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import selector, entity
from homeassistant.components.climate import (
    ATTR_MIN_TEMP,
    ATTR_MAX_TEMP
)
from homeassistant.const import Platform
from . import const

_LOGGER = logging.getLogger(__name__)




class ConfigFlow(config_entries.ConfigFlow, domain=const.DOMAIN):
    """Config flow for Zoned Heating."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""

        _LOGGER.debug("Currently at: [async_step_user]")

        # Only a single instance of the integration
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        id = secrets.token_hex(6)

        await self.async_set_unique_id(id)
        self._abort_if_unique_id_configured(updates=user_input)

        return self.async_create_entry(title=const.NAME, data={})

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a option flow for Zoned Heating."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        """Initialize options flow."""
        self.config_entry = config_entry
        curr_settings = config_entry.options
        self.curr_settings = config_entry.options

        # Checking if we already have a controller
        self.controller = curr_settings.get(const.CONF_CONTROLLER)
        self.controller_max_step = curr_settings.get(const.CONF_CONTROLLER_MAX_STEP)
        self.zones: List[str] | None  = curr_settings.get(const.CONF_ZONES)
        self.max_setpoint = curr_settings.get(const.CONF_MAX_SETPOINT)
        self.controller_delay_time = curr_settings.get(const.CONF_CONTROLLER_DELAY_TIME)
        self.ignore_controller = curr_settings.get(const.CONF_IGNORE_CONTROLLER)

    def __get_unit_of_measurement(self):
        if self.controller is None:
            return const.DEFAULT_UNIT_OF_MEASURE
        uom = entity.get_unit_of_measurement(self.hass, self.controller)
        
        return UnitOfTemperature.CELSIUS if uom is None else uom

    def __get_climate_step(self):
        if self.controller is None:
            return 1
        step = self.hass.states.get(self.controller).attributes.get('target_temp_step', 1)
        return step

    def __parse_user_input(self, user_input):
        for key in user_input:
            if user_input.get(key):
                self.__setattr__(key,  user_input.get(key))

        pass

    async def async_step_init(self, user_input=None):
        """Handle options flow."""
        _LOGGER.debug('Currently at: [async_step_init]')
        return await self.async_step_user()
        
    async def async_step_user(self, user_input=None):
        _LOGGER.debug("Currently at: [async_step_user]")
        if user_input is not None:
            _LOGGER.debug("Got user input, continuing to controller_settings")
            self.__parse_user_input(user_input)
            return await self.async_step_controller_settings()

        fields = OrderedDict()

        # Setup choosing controller
        fields[
            vol.Required(
                const.CONF_CONTROLLER, default=self.controller
            )
        ] = selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["climate", "switch"],
                    multiple=False
                )
            )
        return self.async_show_form(step_id="user", data_schema=vol.Schema(fields))

    async def async_step_controller_settings(self, user_input: Dict[str, Any] =None):

        if user_input is not None:
            self.__parse_user_input(user_input)
            return await self.async_step_zones()


        fields = OrderedDict()
        
        # Setup max_setupoint for controller
        controller_state = self.hass.states.get(self.controller)
        min_temp = 0
        max_temp = 100
        if self.controller.startswith(Platform.CLIMATE):
            min_temp = round(controller_state.attributes.get(ATTR_MIN_TEMP))
            max_temp = round(controller_state.attributes.get(ATTR_MAX_TEMP))

        default = self.config_entry.options.get(const.CONF_MAX_SETPOINT)
        if not default or default < min_temp or default > max_temp:
            default = round((min_temp + max_temp)/2)

        default = max_temp if max_temp < 100 else const.DEFAULT_MAX_SETPOINT
        default = self.max_setpoint if self.max_setpoint is not None else default

        fields[
            vol.Required(
                const.CONF_MAX_SETPOINT,
                default=default
            )
        ] = selector.NumberSelector(
                selector.NumberSelectorConfig(min=min_temp, max=max_temp, unit_of_measurement=self.__get_unit_of_measurement(), step=self.__get_climate_step())
            )

        # Setup delay time
        fields[
            vol.Required(
                const.CONF_CONTROLLER_DELAY_TIME,
                default=self.controller_delay_time if self.controller_delay_time is not None else const.DEFAULT_CONTROLLER_DELAY_TIME
            )] = selector.NumberSelector(
                        selector.NumberSelectorConfig(min=0, max=10, unit_of_measurement="seconds", step=0.5)
                    )     

        # Setup max step controller
        fields[
            vol.Required(
                const.CONF_CONTROLLER_MAX_STEP,
                default=self.curr_settings.get(const.CONF_CONTROLLER_MAX_STEP, const.DEFAULT_CONTROLLER_MAX_STEP)
            )
        ] = selector.NumberSelector(
            selector.NumberSelectorConfig(
                 min=0
                ,max=self.hass.states.get(self.controller).attributes.get('max_temp', 1) # self .get(const.CONF_CONTROLLER_MAX_STEP,const.DEFAULT_CONTROLLER_MAX_STEP)
                ,unit_of_measurement=self.__get_unit_of_measurement()
                ,step=self.__get_climate_step()
            )
        )
        
        # Ask if controller input should be ignored
        fields[
            vol.Required(
                const.CONF_IGNORE_CONTROLLER,
                default=self.curr_settings.get(const.CONF_IGNORE_CONTROLLER, const.DEFAULT_IGNORE_CONTROLLER)
            )
        ] = selector.BooleanSelector()

        return self.async_show_form(step_id="controller_settings", data_schema=vol.Schema(fields))


    async def async_step_zones(self, user_input=None):
        """Handle options flow."""
        _LOGGER.debug('Currently at: [async_step_zones]')

        if user_input is not None:
            _LOGGER.debug("Got user_input, continuing to finalizing setup")
            self.__parse_user_input(user_input)

            return self.async_create_entry(title="", data={
                const.CONF_ZONES: self.zones,
                const.CONF_CONTROLLER: self.controller,
                const.CONF_MAX_SETPOINT: self.max_setpoint,
                const.CONF_CONTROLLER_DELAY_TIME: self.controller_delay_time,
                const.CONF_IGNORE_CONTROLLER: self.ignore_controller,
                const.CONF_CONTROLLER_MAX_STEP: self.controller_max_step
            })
        

        zone_controllers = OrderedDict()

        zone_controllers[
            vol.Required(
                const.CONF_ZONES,
                default=self.zones
            )
        ] = selector.EntitySelector(
            selector.EntitySelectorConfig(
                domain=["climate"],
                multiple=True,
                exclude_entities=[self.controller]
            )
        )
        return self.async_show_form(step_id=const.CONF_ZONES, data_schema=vol.Schema(zone_controllers))
