"""Diagnostic sensor entity for hagelschutz_vkf, backed by the coordinator instance itself."""

from collections.abc import Callable
from dataclasses import dataclass

from custom_components.hagelschutz_vkf.coordinator import HagelschutzVkfDataUpdateCoordinator
from custom_components.hagelschutz_vkf.entity import HagelschutzVkfEntity
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.typing import StateType


@dataclass(frozen=True, kw_only=True)
class HagelschutzVkfDiagnosticSensorEntityDescription(SensorEntityDescription):
    """Describes a diagnostic sensor read from the coordinator instance, not its poll data."""

    value_fn: Callable[[HagelschutzVkfDataUpdateCoordinator], StateType]


class HagelschutzVkfDiagnosticSensor(SensorEntity, HagelschutzVkfEntity):
    """
    Diagnostic sensor reporting on the coordinator's own error state.

    Overrides `available` instead of inheriting `CoordinatorEntity.available` (last_update_success)
    because this is the entity meant to still work when hail_status does not.
    """

    entity_description: HagelschutzVkfDiagnosticSensorEntityDescription

    @property
    def available(self) -> bool:
        """Return True unconditionally, regardless of the last poll's outcome."""
        return True

    @property
    def native_value(self) -> StateType:
        """Return the value read from the coordinator instance."""
        return self.entity_description.value_fn(self.coordinator)
