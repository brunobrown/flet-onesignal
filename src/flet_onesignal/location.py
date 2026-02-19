"""
OneSignal Location module for flet-onesignal.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flet_onesignal.onesignal import OneSignal


class OneSignalLocation:
    """
    OneSignal Location namespace.

    Provides methods for managing location sharing with OneSignal.
    """

    def __init__(self, service: "OneSignal"):
        self._service = service

    async def request_permission(self, timeout: float = 25) -> bool:
        """
        Request permission to access location.

        Returns:
            True if permission was granted, False otherwise.
        """
        result = await self._service._invoke_method(
            "location_request_permission",
            timeout=timeout,
        )
        return result == "true"

    async def get_permission(self, timeout: float = 10) -> bool:
        """
        Check if location permission is currently granted.

        Returns:
            True if permission is granted, False otherwise.
        """
        result = await self._service._invoke_method(
            "location_get_permission",
            timeout=timeout,
        )
        return result == "true"

    async def set_shared(self, shared: bool) -> None:
        """
        Set whether location data should be shared with OneSignal.

        Args:
            shared: True to share location, False to stop sharing.
        """
        await self._service._invoke_method(
            "location_set_shared",
            {"shared": shared},
        )

    async def is_shared(self, timeout: float = 25) -> bool:
        """
        Check if location is currently being shared with OneSignal.

        Returns:
            True if location is shared, False otherwise.
        """
        result = await self._service._invoke_method(
            "location_is_shared",
            timeout=timeout,
        )
        return result == "true"
