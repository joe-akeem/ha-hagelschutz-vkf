"""Binary sensor entity for hagelschutz_vkf."""

from collections.abc import Callable
from dataclasses import dataclass

from custom_components.hagelschutz_vkf.coordinator import HagelschutzVkfPollResult
from custom_components.hagelschutz_vkf.entity import HagelschutzVkfEntity
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription


@dataclass(frozen=True, kw_only=True)
class HagelschutzVkfBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes a binary sensor and how to read it from the coordinator's poll result."""

    value_fn: Callable[[HagelschutzVkfPollResult], bool]


class HagelschutzVkfBinarySensor(BinarySensorEntity, HagelschutzVkfEntity):
    """Binary sensor backed by the coordinator's parsed poll result."""

    entity_description: HagelschutzVkfBinarySensorEntityDescription

    @property
    def is_on(self) -> bool:
        """Return the value read from the coordinator's poll result."""
        return self.entity_description.value_fn(self.coordinator.data)
