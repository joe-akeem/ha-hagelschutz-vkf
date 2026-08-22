"""Tests for diagnostics."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.hagelschutz_vkf.diagnostics import async_get_config_entry_diagnostics
from homeassistant.core import HomeAssistant


async def test_device_id_is_redacted(init_integration: MockConfigEntry, hass: HomeAssistant) -> None:
    """The device serial is redacted; the hardware-type ID is not."""
    diagnostics = await async_get_config_entry_diagnostics(hass, init_integration)

    assert diagnostics["entry"]["data"]["device_id"] == "**REDACTED**"
    assert diagnostics["entry"]["data"]["hwtype_id"] == 0
    assert diagnostics["coordinator"]["data"]["state"] == "no_hail"
