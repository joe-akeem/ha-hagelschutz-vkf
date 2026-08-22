"""Config flow for hagelschutz_vkf — user setup and reconfigure."""

from typing import Any

from custom_components.hagelschutz_vkf.api import (
    HagelschutzVkfApiClientCommunicationError,
    HagelschutzVkfApiClientDeviceNotFoundError,
    HagelschutzVkfApiClientVendorError,
)
from custom_components.hagelschutz_vkf.const import CONF_DEVICE_ID, CONF_HWTYPE_ID, DOMAIN, LOGGER
from homeassistant import config_entries
from homeassistant.loader import async_get_loaded_integration

from .schemas import get_reconfigure_schema, get_user_schema
from .validators import validate_device


class HagelschutzVkfConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for hagelschutz_vkf."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """
        Handle a flow started by the user.

        Returns:
            The form, or the created config entry.

        """
        errors: dict[str, str] = {}
        placeholders: dict[str, str] = {}

        if user_input is not None:
            errors, placeholders = await self._async_validate(user_input)
            if not errors:
                await self.async_set_unique_id(user_input[CONF_DEVICE_ID])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_DEVICE_ID],
                    data=user_input,
                )

        integration = async_get_loaded_integration(self.hass, DOMAIN)

        return self.async_show_form(
            step_id="user",
            data_schema=get_user_schema(user_input),
            errors=errors,
            description_placeholders={
                "documentation_url": integration.documentation or "",
                **placeholders,
            },
        )

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """
        Handle reconfiguration of an existing entry.

        Returns:
            The form, or the abort that follows the entry update.

        """
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}
        placeholders: dict[str, str] = {}

        if user_input is not None:
            errors, placeholders = await self._async_validate(user_input)
            if not errors:
                return self.async_update_reload_and_abort(entry, data_updates=user_input)

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(
                get_reconfigure_schema(
                    entry.data.get(CONF_DEVICE_ID, ""),
                    entry.data.get(CONF_HWTYPE_ID, 0),
                ),
                entry.data,
            ),
            errors=errors,
            description_placeholders=placeholders,
        )

    async def _async_validate(self, user_input: dict[str, Any]) -> tuple[dict[str, str], dict[str, str]]:
        """
        Perform a real test poll against the submitted device.

        Returns:
            An empty errors dict when it succeeds, otherwise the errors and any placeholders
            (e.g. the vendor's own message) their translation needs.

        """
        try:
            await validate_device(
                self.hass,
                device_id=user_input[CONF_DEVICE_ID],
                hwtype_id=int(user_input[CONF_HWTYPE_ID]),
            )
        except HagelschutzVkfApiClientDeviceNotFoundError:
            return {"base": "device_not_found"}, {}
        except HagelschutzVkfApiClientVendorError as exception:
            return {"base": "vendor_error"}, {"vendor_message": exception.vendor_message}
        except HagelschutzVkfApiClientCommunicationError:
            return {"base": "cannot_connect"}, {}
        except Exception:  # noqa: BLE001 - Anything unexpected still has to reach the form.
            LOGGER.exception("Unexpected exception")
            return {"base": "unknown"}, {}

        return {}, {}


__all__ = ["HagelschutzVkfConfigFlowHandler"]
