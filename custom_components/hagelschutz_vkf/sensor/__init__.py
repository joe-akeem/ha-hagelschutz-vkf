"""Sensor platform for hagelschutz_vkf."""

from itertools import chain
from typing import TYPE_CHECKING

from .diagnostic_entity import HagelschutzVkfDiagnosticSensor
from .entity import HagelschutzVkfSensor
from .hail_status import ENTITY_DESCRIPTIONS as HAIL_STATUS_DESCRIPTIONS
from .last_error import ENTITY_DESCRIPTIONS as LAST_ERROR_DESCRIPTIONS

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
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        chain(
            (HagelschutzVkfSensor(coordinator, description) for description in HAIL_STATUS_DESCRIPTIONS),
            (HagelschutzVkfDiagnosticSensor(coordinator, description) for description in LAST_ERROR_DESCRIPTIONS),
        )
    )
