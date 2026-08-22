"""Tests for the hail-status sensor."""

from unittest.mock import AsyncMock

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.hagelschutz_vkf.api import HagelschutzVkfApiClientError
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant

ENTITY_ID = "sensor.vkdemo123456_hail_status"


@pytest.mark.parametrize(
    ("current_state", "expected"),
    [
        (0, "no_hail"),
        (1, "hail"),
        (2, "test_alarm"),
    ],
)
async def test_current_state_is_mapped(
    hass: HomeAssistant,
    mock_api: AsyncMock,
    config_entry: MockConfigEntry,
    current_state: int,
    expected: str,
) -> None:
    """Each documented currentState value maps to its speaking hail status."""
    mock_api.return_value = {"currentState": current_state}
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert hass.states.get(ENTITY_ID).state == expected


async def test_unrecognized_state_is_unknown_not_a_crash(
    hass: HomeAssistant,
    mock_api: AsyncMock,
    config_entry: MockConfigEntry,
) -> None:
    """A currentState value outside the documented range does not crash setup."""
    mock_api.return_value = {"currentState": 99}
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get(ENTITY_ID)
    assert state.state == STATE_UNKNOWN
    assert state.attributes["raw_state"] == 99


async def test_extra_payload_keys_surface_as_attributes(
    hass: HomeAssistant,
    mock_api: AsyncMock,
    config_entry: MockConfigEntry,
) -> None:
    """Unrecognized keys beyond currentState pass through instead of crashing."""
    mock_api.return_value = {"currentState": 0, "futureField": "value"}
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get(ENTITY_ID)
    assert state.state == "no_hail"
    assert state.attributes["futureField"] == "value"


async def test_entity_unavailable_when_poll_fails(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
    mock_api: AsyncMock,
) -> None:
    """A failed refresh makes the entity unavailable rather than stale."""
    mock_api.side_effect = HagelschutzVkfApiClientError("boom")

    await init_integration.runtime_data.coordinator.async_refresh()
    await hass.async_block_till_done()

    assert hass.states.get(ENTITY_ID).state == STATE_UNAVAILABLE
