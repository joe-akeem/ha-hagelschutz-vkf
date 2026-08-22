"""Sensor platform for hagelschutz_vkf."""

from typing import TYPE_CHECKING

from .entity import HagelschutzVkfSensor
from .hail_status import ENTITY_DESCRIPTIONS

# Read-only platform: the coordinator already serializes the fetch.
PARALLEL_UPDATES = 0

if TYPE_CHECKING:
    from custom_components.hagelschutz_vkf.data import HagelschutzVkfConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HagelschutzVkfConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        HagelschutzVkfSensor(entry.runtime_data.coordinator, description) for description in ENTITY_DESCRIPTIONS
    )
