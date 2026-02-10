"""
OneSignal Debug module for flet-onesignal.
"""

from typing import TYPE_CHECKING

from flet_onesignal.types import OSLogLevel

if TYPE_CHECKING:
    from flet_onesignal.onesignal import OneSignal


class OneSignalDebug:
    """
    OneSignal Debug namespace.

    Provides methods for configuring SDK logging behavior.
    """

    def __init__(self, service: "OneSignal"):
        self._service = service

    async def set_log_level(self, level: OSLogLevel) -> None:
        """
        Set the logging level of the OneSignal SDK.

        Args:
            level: The log level to set (OSLogLevel enum value).
        """
        await self._service._invoke_method(
            "debug_set_log_level",
            {"level": level.value},
        )

    async def set_alert_level(self, level: OSLogLevel) -> None:
        """
        Set the alert level for the OneSignal SDK.

        This controls which log messages trigger visual alerts (useful for debugging).

        Args:
            level: The alert level to set (OSLogLevel enum value).
        """
        await self._service._invoke_method(
            "debug_set_alert_level",
            {"level": level.value},
        )
