"""Sensor entity for hagelschutz_vkf."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from custom_components.hagelschutz_vkf.coordinator import HagelschutzVkfPollResult
from custom_components.hagelschutz_vkf.entity import HagelschutzVkfEntity
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.typing import StateType


@dataclass(frozen=True, kw_only=True)
class HagelschutzVkfSensorEntityDescription(SensorEntityDescription):
    """Describes a sensor and how to read it from the coordinator's poll result."""

    value_fn: Callable[[HagelschutzVkfPollResult], StateType]


class HagelschutzVkfSensor(SensorEntity, HagelschutzVkfEntity):
    """Sensor backed by the coordinator's parsed poll result."""

    entity_description: HagelschutzVkfSensorEntityDescription

    @property
    def native_value(self) -> StateType:
        """Return the value read from the coordinator's poll result."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """
        Return the raw state plus any keys the vendor payload adds beyond currentState.

        The API contract documents only currentState today; this passes through
        anything else it may add later without needing an integration update.
        """
        data = self.coordinator.data
        return {"raw_state": data.raw_state, **data.extra_attributes}
