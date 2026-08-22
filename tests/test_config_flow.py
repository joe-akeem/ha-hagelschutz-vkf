"""Tests for the config flow."""

from unittest.mock import AsyncMock

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.hagelschutz_vkf.api import (
    HagelschutzVkfApiClientCommunicationError,
    HagelschutzVkfApiClientDeviceNotFoundError,
    HagelschutzVkfApiClientVendorError,
)
from custom_components.hagelschutz_vkf.const import CONF_DEVICE_ID, CONF_HWTYPE_ID, DOMAIN
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def test_user_flow_creates_entry(hass: HomeAssistant, mock_api: AsyncMock) -> None:
    """A successful test poll creates the config entry."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
        data={CONF_DEVICE_ID: "VKDEMO123456", CONF_HWTYPE_ID: 0},
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "VKDEMO123456"
    assert result["data"] == {CONF_DEVICE_ID: "VKDEMO123456", CONF_HWTYPE_ID: 0}


async def test_user_flow_cannot_connect(hass: HomeAssistant, mock_api: AsyncMock) -> None:
    """A failed test poll re-shows the form with an error."""
    mock_api.side_effect = HagelschutzVkfApiClientCommunicationError("boom")

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
        data={CONF_DEVICE_ID: "VKDEMO123456", CONF_HWTYPE_ID: 0},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}


async def test_user_flow_device_not_found(hass: HomeAssistant, mock_api: AsyncMock) -> None:
    """A serial the vendor does not recognize shows a specific error, not a generic one."""
    mock_api.side_effect = HagelschutzVkfApiClientDeviceNotFoundError("boom")

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
        data={CONF_DEVICE_ID: "UNKNOWN123", CONF_HWTYPE_ID: 0},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "device_not_found"}


async def test_user_flow_vendor_error_shows_vendor_message(hass: HomeAssistant, mock_api: AsyncMock) -> None:
    """An unrecognized vendor exception surfaces the vendor's own message verbatim."""
    mock_api.side_effect = HagelschutzVkfApiClientVendorError("Some server-side glitch")

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
        data={CONF_DEVICE_ID: "VKDEMO123456", CONF_HWTYPE_ID: 0},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "vendor_error"}
    assert result["description_placeholders"]["vendor_message"] == "Some server-side glitch"


async def test_user_flow_aborts_on_duplicate_unique_id(
    hass: HomeAssistant,
    mock_api: AsyncMock,
    init_integration: MockConfigEntry,
) -> None:
    """The same device serial cannot be configured twice."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
        data={CONF_DEVICE_ID: init_integration.unique_id, CONF_HWTYPE_ID: 0},
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_reconfigure_flow_updates_entry(
    hass: HomeAssistant,
    mock_api: AsyncMock,
    init_integration: MockConfigEntry,
) -> None:
    """Reconfigure updates the entry's device serial and hardware-type ID."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": config_entries.SOURCE_RECONFIGURE,
            "entry_id": init_integration.entry_id,
        },
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {CONF_DEVICE_ID: "VKDEMO123456", CONF_HWTYPE_ID: 1},
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"
    assert init_integration.data[CONF_HWTYPE_ID] == 1
