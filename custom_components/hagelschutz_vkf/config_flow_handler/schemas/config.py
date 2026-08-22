"""Config flow schemas for the user and reconfigure steps."""

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from custom_components.hagelschutz_vkf.const import CONF_DEVICE_ID, CONF_HWTYPE_ID
from homeassistant.helpers import selector

_DEVICE_ID_SELECTOR = selector.TextSelector(
    selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT),
)
_HWTYPE_ID_SELECTOR = selector.NumberSelector(
    selector.NumberSelectorConfig(min=0, step=1, mode=selector.NumberSelectorMode.BOX),
)


def get_user_schema(defaults: Mapping[str, Any] | None = None) -> vol.Schema:
    """
    Build the schema for the user step.

    Args:
        defaults: Previously submitted values, used to pre-fill the form.

    Returns:
        The voluptuous schema for the device form.

    """
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_DEVICE_ID,
                default=defaults.get(CONF_DEVICE_ID, vol.UNDEFINED),
            ): _DEVICE_ID_SELECTOR,
            vol.Required(
                CONF_HWTYPE_ID,
                default=defaults.get(CONF_HWTYPE_ID, 0),
            ): _HWTYPE_ID_SELECTOR,
        },
    )


def get_reconfigure_schema(device_id: str, hwtype_id: int) -> vol.Schema:
    """
    Build the schema for the reconfigure step.

    Args:
        device_id: The entry's current device serial, used to pre-fill the form.
        hwtype_id: The entry's current hardware-type code, used to pre-fill the form.

    Returns:
        The voluptuous schema for the reconfigure form.

    """
    return vol.Schema(
        {
            vol.Required(CONF_DEVICE_ID, default=device_id): _DEVICE_ID_SELECTOR,
            vol.Required(CONF_HWTYPE_ID, default=hwtype_id): _HWTYPE_ID_SELECTOR,
        },
    )


__all__ = [
    "get_reconfigure_schema",
    "get_user_schema",
]
