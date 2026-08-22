"""Base entity class for hagelschutz_vkf."""

from typing import TYPE_CHECKING

from custom_components.hagelschutz_vkf.const import ATTRIBUTION, CONF_HWTYPE_ID
from custom_components.hagelschutz_vkf.coordinator import HagelschutzVkfDataUpdateCoordinator
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription


class HagelschutzVkfEntity(CoordinatorEntity[HagelschutzVkfDataUpdateCoordinator]):
    """
    Base entity providing device info, unique ID and attribution.

    The vendor API exposes no device metadata beyond `currentState`, so device info
    is built entirely from the config entry: the serial (`device_id`) is the unique
    ID, and `hwtype_id` is the only other identifying value the vendor gives us.
    """

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: HagelschutzVkfDataUpdateCoordinator,
        entity_description: EntityDescription,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        entry = coordinator.config_entry
        self._attr_unique_id = f"{entry.entry_id}_{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(entry.domain, entry.entry_id)},
            name=entry.title,
            serial_number=entry.unique_id,
            model_id=str(entry.data[CONF_HWTYPE_ID]),
            entry_type=DeviceEntryType.SERVICE,
        )
