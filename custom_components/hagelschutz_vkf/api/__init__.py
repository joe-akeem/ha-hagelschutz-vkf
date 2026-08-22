"""
API package for hagelschutz_vkf.

Exception hierarchy:
    HagelschutzVkfApiClientError (base)
    ├── HagelschutzVkfApiClientCommunicationError (network/timeout/HTTP error)
    ├── HagelschutzVkfApiClientDeviceNotFoundError (vendor reports the device/hwtype as unknown)
    └── HagelschutzVkfApiClientVendorError (any other vendor-reported error, message carried verbatim)

The vendor endpoint requires no authentication, so unlike the blueprint's example
client there is no ...AuthenticationError and the coordinator never raises
ConfigEntryAuthFailed for this integration.

The coordinator maps HagelschutzVkfApiClientDeviceNotFoundError onto ConfigEntryError
(a wrong or removed device will not resolve by retrying) and every other
HagelschutzVkfApiClientError onto UpdateFailed; nothing else in the integration
imports this package.
"""

from .client import (
    HagelschutzVkfApiClient,
    HagelschutzVkfApiClientCommunicationError,
    HagelschutzVkfApiClientDeviceNotFoundError,
    HagelschutzVkfApiClientError,
    HagelschutzVkfApiClientVendorError,
)

__all__ = [
    "HagelschutzVkfApiClient",
    "HagelschutzVkfApiClientCommunicationError",
    "HagelschutzVkfApiClientDeviceNotFoundError",
    "HagelschutzVkfApiClientError",
    "HagelschutzVkfApiClientVendorError",
]
