"""
Runtime data types for hagelschutz_vkf.

Access pattern: entry.runtime_data.client / entry.runtime_data.coordinator
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import HagelschutzVkfApiClient
    from .coordinator import HagelschutzVkfDataUpdateCoordinator


type HagelschutzVkfConfigEntry = ConfigEntry[HagelschutzVkfData]


@dataclass
class HagelschutzVkfData:
    """Runtime data stored on the config entry after a successful setup."""

    client: HagelschutzVkfApiClient
    coordinator: HagelschutzVkfDataUpdateCoordinator
    integration: Integration
