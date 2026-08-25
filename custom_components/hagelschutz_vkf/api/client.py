"""API client for hagelschutz_vkf."""

import asyncio
import contextlib
import socket
from typing import Any

import aiohttp

API_BASE_URL = "https://meteo.netitservices.com/api/v1/devices"
REQUEST_TIMEOUT = 10


class HagelschutzVkfApiClientError(Exception):
    """Base exception to indicate a general API error."""


class HagelschutzVkfApiClientCommunicationError(
    HagelschutzVkfApiClientError,
):
    """Exception to indicate a communication error with the API."""


class HagelschutzVkfApiClientDeviceNotFoundError(
    HagelschutzVkfApiClientError,
):
    """Exception to indicate the vendor does not recognize this device/hwtype combination."""


class HagelschutzVkfApiClientVendorError(HagelschutzVkfApiClientError):
    """
    Exception carrying a vendor-reported error this client has no specific handling for.

    The vendor's error body always has the shape {"exception": <name>, "message": <text>};
    `vendor_exception` and `vendor_message` carry both fields verbatim so the caller can surface
    either — the name for diagnostics, the message (usually English) for the user.
    """

    def __init__(self, vendor_exception: str, vendor_message: str) -> None:
        """Initialize the exception, keeping the vendor's exception name and message verbatim."""
        super().__init__(vendor_message)
        self.vendor_exception = vendor_exception
        self.vendor_message = vendor_message


async def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """
    Verify that the API response is valid.

    Raises:
        HagelschutzVkfApiClientDeviceNotFoundError: If the vendor reports the device/hwtype as unknown.
        HagelschutzVkfApiClientVendorError: For any other vendor-reported error with a message.
        aiohttp.ClientResponseError: For any other unsuccessful status.

    """
    if response.ok:
        return

    payload: Any = None
    with contextlib.suppress(aiohttp.ContentTypeError, ValueError):
        payload = await response.json()

    if isinstance(payload, dict) and isinstance(payload.get("exception"), str):
        message = str(payload.get("message", payload["exception"]))
        if payload["exception"] == "DeviceNotFoundException":
            raise HagelschutzVkfApiClientDeviceNotFoundError(message)
        raise HagelschutzVkfApiClientVendorError(payload["exception"], message)

    response.raise_for_status()


class HagelschutzVkfApiClient:
    """Read-only client for the VKF hail-warning poll endpoint."""

    def __init__(
        self,
        device_id: str,
        hwtype_id: int,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize the API client."""
        self._device_id = device_id
        self._hwtype_id = hwtype_id
        self._session = session

    async def async_get_data(self) -> dict[str, Any]:
        """
        Poll the current hail-warning status.

        Returns:
            The decoded JSON response, unchanged.

        """
        return await self._api_wrapper(
            method="get",
            url=f"{API_BASE_URL}/{self._device_id}/poll",
            params={"hwtypeId": self._hwtype_id},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Perform a request and translate transport errors into client exceptions.

        Returns:
            The decoded JSON response.

        Raises:
            HagelschutzVkfApiClientCommunicationError: If the request does not complete.
            HagelschutzVkfApiClientError: For any other failure.

        """
        try:
            async with asyncio.timeout(REQUEST_TIMEOUT):
                response = await self._session.request(method=method, url=url, params=params)
                await _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise HagelschutzVkfApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise HagelschutzVkfApiClientCommunicationError(msg) from exception
        except HagelschutzVkfApiClientError:
            raise
        except Exception as exception:
            msg = f"Unexpected error talking to the API - {exception}"
            raise HagelschutzVkfApiClientError(msg) from exception
