"""Coordinator data shape for hagelschutz_vkf."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, kw_only=True)
class HagelschutzVkfPollResult:
    """
    One parsed poll response.

    `state` is the mapped hail status, or `None` if `currentState` was missing or
    held a value the integration does not recognize yet. `extra_attributes` carries
    any keys besides `currentState` the vendor payload may add in the future, so a
    new field never crashes the integration.
    """

    state: str | None
    raw_state: int | None
    extra_attributes: dict[str, Any]
