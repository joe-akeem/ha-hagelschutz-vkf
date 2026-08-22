"""Constants for hagelschutz_vkf."""

from datetime import timedelta
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "hagelschutz_vkf"
ATTRIBUTION = "Data provided by the VKF hail-warning network (meteo.netitservices.com)"

CONF_DEVICE_ID = "device_id"
CONF_HWTYPE_ID = "hwtype_id"

# Vendor-mandated floor; not user-configurable.
UPDATE_INTERVAL = timedelta(seconds=120)

HAIL_STATE_NO_HAIL = "no_hail"
HAIL_STATE_HAIL = "hail"
HAIL_STATE_TEST_ALARM = "test_alarm"

HAIL_STATES: tuple[str, ...] = (HAIL_STATE_NO_HAIL, HAIL_STATE_HAIL, HAIL_STATE_TEST_ALARM)

CURRENT_STATE_MAP: dict[int, str] = {
    0: HAIL_STATE_NO_HAIL,
    1: HAIL_STATE_HAIL,
    2: HAIL_STATE_TEST_ALARM,
}
