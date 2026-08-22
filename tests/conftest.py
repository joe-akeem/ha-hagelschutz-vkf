"""Shared fixtures for the hagelschutz_vkf tests."""

from collections.abc import Generator
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.hagelschutz_vkf.const import CONF_DEVICE_ID, CONF_HWTYPE_ID, DOMAIN
from homeassistant.core import HomeAssistant

# The API's documented success response: {"currentState": <int>}. 0 = no hail.
API_RESPONSE: dict[str, Any] = {"currentState": 0}


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Load custom integrations in every test."""


@pytest.fixture
def mock_api() -> Generator[AsyncMock]:
    """Replace the client's HTTP layer, keeping its request-building logic under test."""
    with patch(
        "custom_components.hagelschutz_vkf.api.client.HagelschutzVkfApiClient._api_wrapper",
        new_callable=AsyncMock,
        return_value=API_RESPONSE,
    ) as api_wrapper:
        yield api_wrapper


@pytest.fixture
def config_entry() -> MockConfigEntry:
    """Return a config entry for this integration."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="VKDEMO123456",
        unique_id="VKDEMO123456",
        data={CONF_DEVICE_ID: "VKDEMO123456", CONF_HWTYPE_ID: 0},
    )


@pytest.fixture
async def init_integration(
    hass: HomeAssistant,
    mock_api: AsyncMock,
    config_entry: MockConfigEntry,
) -> MockConfigEntry:
    """
    Set up the integration from a config entry.

    Returns:
        The config entry, now loaded.

    """
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    return config_entry
