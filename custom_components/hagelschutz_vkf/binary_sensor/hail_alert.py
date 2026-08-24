"""The hail-alert binary sensor description."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from .entity import HagelschutzVkfBinarySensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[HagelschutzVkfBinarySensorEntityDescription, ...] = (
    HagelschutzVkfBinarySensorEntityDescription(
        key="hail_alert",
        translation_key="hail_alert",
        device_class=BinarySensorDeviceClass.SAFETY,
        value_fn=lambda data: data.raw_state not in (0, None),
    ),
)
