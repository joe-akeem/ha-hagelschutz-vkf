"""Data update coordinator package for hagelschutz_vkf."""

from .base import HagelschutzVkfDataUpdateCoordinator
from .models import HagelschutzVkfPollResult

__all__ = ["HagelschutzVkfDataUpdateCoordinator", "HagelschutzVkfPollResult"]
