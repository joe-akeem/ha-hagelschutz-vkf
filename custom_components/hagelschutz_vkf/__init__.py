"""
Custom integration to integrate hagelschutz_vkf with Home Assistant.

For more details about this integration, please refer to:
https://github.com/joe-akeem/ha-hagelschutz-vkf
"""

from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.loader import async_get_loaded_integration

from .api import HagelschutzVkfApiClient
from .const import CONF_DEVICE_ID, CONF_HWTYPE_ID, DOMAIN, LOGGER, UPDATE_INTERVAL
from .coordinator import HagelschutzVkfDataUpdateCoordinator
from .data import HagelschutzVkfData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import HagelschutzVkfConfigEntry

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HagelschutzVkfConfigEntry,
) -> bool:
    """
    Set up a config entry.

    Returns:
        True once the coordinator has data and every platform is forwarded.

    """
    client = HagelschutzVkfApiClient(
        device_id=entry.data[CONF_DEVICE_ID],
        hwtype_id=int(entry.data[CONF_HWTYPE_ID]),
        session=async_get_clientsession(hass),
    )

    coordinator = HagelschutzVkfDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        config_entry=entry,
        update_interval=UPDATE_INTERVAL,
        always_update=False,
    )

    entry.runtime_data = HagelschutzVkfData(
        client=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: HagelschutzVkfConfigEntry,
) -> bool:
    """
    Unload a config entry.

    Returns:
        True if every platform unloaded cleanly.

    """
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
