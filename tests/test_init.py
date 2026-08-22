"""Tests for integration setup and unload."""

from unittest.mock import AsyncMock

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.hagelschutz_vkf.api import HagelschutzVkfApiClientDeviceNotFoundError
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant


async def test_setup_and_unload(init_integration: MockConfigEntry, hass: HomeAssistant) -> None:
    """The entry loads and unloads cleanly."""
    assert init_integration.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(init_integration.entry_id)
    await hass.async_block_till_done()

    assert init_integration.state is ConfigEntryState.NOT_LOADED


async def test_setup_fails_when_device_not_found(
    hass: HomeAssistant,
    mock_api: AsyncMock,
    config_entry: MockConfigEntry,
) -> None:
    """A device the vendor no longer recognizes stops the retry loop instead of spinning forever."""
    mock_api.side_effect = HagelschutzVkfApiClientDeviceNotFoundError("boom")
    config_entry.add_to_hass(hass)

    assert not await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.SETUP_ERROR
