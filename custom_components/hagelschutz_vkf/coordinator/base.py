"""Data update coordinator for hagelschutz_vkf."""

from typing import TYPE_CHECKING, Any

from custom_components.hagelschutz_vkf.api import (
    HagelschutzVkfApiClientDeviceNotFoundError,
    HagelschutzVkfApiClientError,
)
from custom_components.hagelschutz_vkf.const import CURRENT_STATE_MAP, DOMAIN
from homeassistant.exceptions import ConfigEntryError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .models import HagelschutzVkfPollResult

if TYPE_CHECKING:
    from custom_components.hagelschutz_vkf.data import HagelschutzVkfConfigEntry


def _parse_poll_result(payload: dict[str, Any]) -> HagelschutzVkfPollResult:
    """Map `currentState` to a hail status and pass through any other keys."""
    raw_state = payload.get("currentState")
    state = CURRENT_STATE_MAP.get(raw_state) if isinstance(raw_state, int) else None
    extra_attributes = {key: value for key, value in payload.items() if key != "currentState"}
    return HagelschutzVkfPollResult(state=state, raw_state=raw_state, extra_attributes=extra_attributes)


class HagelschutzVkfDataUpdateCoordinator(DataUpdateCoordinator[HagelschutzVkfPollResult]):
    """Poll the hail-warning status once per interval and hand it to every entity."""

    config_entry: HagelschutzVkfConfigEntry

    async def _async_update_data(self) -> HagelschutzVkfPollResult:
        """
        Fetch and parse the current hail-warning status.

        Returns:
            The parsed poll result entities read from.

        Raises:
            ConfigEntryError: If the vendor no longer recognizes the configured device serial.
            UpdateFailed: If the fetch failed for any other reason.

        """
        try:
            payload = await self.config_entry.runtime_data.client.async_get_data()
        except HagelschutzVkfApiClientDeviceNotFoundError as exception:
            raise ConfigEntryError(
                translation_domain=DOMAIN,
                translation_key="device_not_found",
            ) from exception
        except HagelschutzVkfApiClientError as exception:
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="update_failed",
            ) from exception
        return _parse_poll_result(payload)
