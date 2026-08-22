"""The hail-status sensor description."""

from custom_components.hagelschutz_vkf.const import HAIL_STATES
from homeassistant.components.sensor import SensorDeviceClass

from .entity import HagelschutzVkfSensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[HagelschutzVkfSensorEntityDescription, ...] = (
    HagelschutzVkfSensorEntityDescription(
        key="hail_status",
        translation_key="hail_status",
        device_class=SensorDeviceClass.ENUM,
        options=list(HAIL_STATES),
        value_fn=lambda data: data.state,
    ),
)
