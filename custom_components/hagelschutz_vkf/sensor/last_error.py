"""The last-error diagnostic sensor descriptions."""

from homeassistant.const import EntityCategory

from .diagnostic_entity import HagelschutzVkfDiagnosticSensorEntityDescription

_NO_ERROR = "OK"

ENTITY_DESCRIPTIONS: tuple[HagelschutzVkfDiagnosticSensorEntityDescription, ...] = (
    HagelschutzVkfDiagnosticSensorEntityDescription(
        key="last_error_type",
        translation_key="last_error_type",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda coordinator: coordinator.last_error_type or _NO_ERROR,
    ),
    HagelschutzVkfDiagnosticSensorEntityDescription(
        key="last_error_message",
        translation_key="last_error_message",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda coordinator: coordinator.last_error_message or _NO_ERROR,
    ),
)
