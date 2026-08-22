"""Validate a device/hwtype pair by performing one real test poll."""

from custom_components.hagelschutz_vkf.api import HagelschutzVkfApiClient
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession


async def validate_device(hass: HomeAssistant, device_id: str, hwtype_id: int) -> None:
    """
    Poll the vendor endpoint once to confirm the device/hwtype pair is reachable.

    Raises:
        HagelschutzVkfApiClientCommunicationError: If the endpoint cannot be reached.

    """
    client = HagelschutzVkfApiClient(
        device_id=device_id,
        hwtype_id=hwtype_id,
        session=async_get_clientsession(hass),
    )
    await client.async_get_data()
