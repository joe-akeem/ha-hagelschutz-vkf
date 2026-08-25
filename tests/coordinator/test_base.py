"""Tests for the data update coordinator."""

from datetime import timedelta
from unittest.mock import AsyncMock

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.hagelschutz_vkf.api import (
    HagelschutzVkfApiClientCommunicationError,
    HagelschutzVkfApiClientDeviceNotFoundError,
    HagelschutzVkfApiClientVendorError,
)
from custom_components.hagelschutz_vkf.const import UPDATE_INTERVAL
from homeassistant.core import HomeAssistant


async def test_update_interval_is_180_seconds(init_integration: MockConfigEntry) -> None:
    """The poll interval leaves headroom under the vendor's daily quota."""
    assert timedelta(seconds=180) == UPDATE_INTERVAL
    assert init_integration.runtime_data.coordinator.update_interval == timedelta(seconds=180)


async def test_last_error_is_none_after_a_successful_poll(init_integration: MockConfigEntry) -> None:
    """A successful poll leaves no error behind."""
    coordinator = init_integration.runtime_data.coordinator

    assert coordinator.last_error_type is None
    assert coordinator.last_error_message is None


async def test_last_error_captures_vendor_exception(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
    mock_api: AsyncMock,
) -> None:
    """A vendor error stores the vendor's exception name and message verbatim."""
    mock_api.side_effect = HagelschutzVkfApiClientVendorError("TooManyPollsException", "Too many polls today")

    await init_integration.runtime_data.coordinator.async_refresh()
    await hass.async_block_till_done()

    coordinator = init_integration.runtime_data.coordinator
    assert coordinator.last_error_type == "TooManyPollsException"
    assert coordinator.last_error_message == "Too many polls today"


async def test_last_error_captures_communication_error(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
    mock_api: AsyncMock,
) -> None:
    """A communication error stores the client exception's class name."""
    mock_api.side_effect = HagelschutzVkfApiClientCommunicationError("Timeout error fetching information")

    await init_integration.runtime_data.coordinator.async_refresh()
    await hass.async_block_till_done()

    assert init_integration.runtime_data.coordinator.last_error_type == "HagelschutzVkfApiClientCommunicationError"


async def test_last_error_captures_device_not_found(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
    mock_api: AsyncMock,
) -> None:
    """A device-not-found error on a later poll still records the error, even though it doesn't stop polling."""
    mock_api.side_effect = HagelschutzVkfApiClientDeviceNotFoundError("Unknown device")

    await init_integration.runtime_data.coordinator.async_refresh()
    await hass.async_block_till_done()

    assert init_integration.runtime_data.coordinator.last_error_type == "HagelschutzVkfApiClientDeviceNotFoundError"


async def test_last_error_clears_on_recovery(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
    mock_api: AsyncMock,
) -> None:
    """A successful poll after a failure clears the last error."""
    coordinator = init_integration.runtime_data.coordinator
    mock_api.side_effect = HagelschutzVkfApiClientVendorError("TooManyPollsException", "Too many polls today")
    await coordinator.async_refresh()
    await hass.async_block_till_done()
    assert coordinator.last_error_type is not None

    mock_api.side_effect = None
    mock_api.return_value = {"currentState": 0}
    await coordinator.async_refresh()
    await hass.async_block_till_done()

    assert coordinator.last_error_type is None
    assert coordinator.last_error_message is None
