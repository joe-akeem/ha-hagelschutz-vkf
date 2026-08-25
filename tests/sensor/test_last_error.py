"""Tests for the last-error diagnostic sensors."""

from unittest.mock import AsyncMock

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.hagelschutz_vkf.api import HagelschutzVkfApiClientVendorError
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

HAIL_STATUS_ENTITY_ID = "sensor.vkdemo123456_hail_status"
TYPE_ENTITY_ID = "sensor.vkdemo123456_last_error_type"
MESSAGE_ENTITY_ID = "sensor.vkdemo123456_last_error_message"


async def test_shows_ok_after_a_successful_poll(init_integration: MockConfigEntry, hass: HomeAssistant) -> None:
    """Both sensors read OK when the last poll succeeded."""
    assert hass.states.get(TYPE_ENTITY_ID).state == "OK"
    assert hass.states.get(MESSAGE_ENTITY_ID).state == "OK"


async def test_surfaces_vendor_error_and_stays_available(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
    mock_api: AsyncMock,
) -> None:
    """The error sensors stay available and show the vendor error while hail_status goes unavailable."""
    mock_api.side_effect = HagelschutzVkfApiClientVendorError("TooManyPollsException", "Too many polls today")

    await init_integration.runtime_data.coordinator.async_refresh()
    await hass.async_block_till_done()

    assert hass.states.get(HAIL_STATUS_ENTITY_ID).state == STATE_UNAVAILABLE
    assert hass.states.get(TYPE_ENTITY_ID).state == "TooManyPollsException"
    assert hass.states.get(MESSAGE_ENTITY_ID).state == "Too many polls today"


async def test_recovers_to_ok_after_a_successful_poll(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
    mock_api: AsyncMock,
) -> None:
    """The error sensors return to OK once a poll succeeds again."""
    coordinator = init_integration.runtime_data.coordinator
    mock_api.side_effect = HagelschutzVkfApiClientVendorError("TooManyPollsException", "Too many polls today")
    await coordinator.async_refresh()
    await hass.async_block_till_done()

    mock_api.side_effect = None
    mock_api.return_value = {"currentState": 0}
    await coordinator.async_refresh()
    await hass.async_block_till_done()

    assert hass.states.get(TYPE_ENTITY_ID).state == "OK"
    assert hass.states.get(MESSAGE_ENTITY_ID).state == "OK"


async def test_entities_are_diagnostic(init_integration: MockConfigEntry, hass: HomeAssistant) -> None:
    """Both error sensors are registered as diagnostic entities."""
    entity_registry = er.async_get(hass)

    assert entity_registry.async_get(TYPE_ENTITY_ID).entity_category == er.EntityCategory.DIAGNOSTIC
    assert entity_registry.async_get(MESSAGE_ENTITY_ID).entity_category == er.EntityCategory.DIAGNOSTIC
