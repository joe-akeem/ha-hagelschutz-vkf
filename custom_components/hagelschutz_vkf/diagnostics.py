"""
Diagnostics support for hagelschutz_vkf.

https://developers.home-assistant.io/docs/core/integration_diagnostics
"""

import dataclasses
from typing import TYPE_CHECKING, Any

from custom_components.hagelschutz_vkf.const import CONF_DEVICE_ID
from homeassistant.helpers.redact import async_redact_data

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import HagelschutzVkfConfigEntry

TO_REDACT = {CONF_DEVICE_ID}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: HagelschutzVkfConfigEntry,
) -> dict[str, Any]:
    """
    Return diagnostics for a config entry.

    Returns:
        The redacted entry configuration and the current coordinator state.

    """
    coordinator = entry.runtime_data.coordinator

    return {
        "entry": {
            "version": entry.version,
            "minor_version": entry.minor_version,
            "state": str(entry.state),
            "data": async_redact_data(entry.data, TO_REDACT),
        },
        "coordinator": {
            "last_update_success": coordinator.last_update_success,
            "update_interval": str(coordinator.update_interval),
            "last_exception": str(coordinator.last_exception) if coordinator.last_exception else None,
            "data": dataclasses.asdict(coordinator.data) if coordinator.data else None,
        },
    }
