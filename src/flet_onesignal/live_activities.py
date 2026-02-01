"""
OneSignal Live Activities module for flet-onesignal.

Live Activities are an iOS-only feature that displays real-time information
on the Lock Screen and in the Dynamic Island.
"""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from flet_onesignal.onesignal import OneSignal


class OneSignalLiveActivities:
    """
    OneSignal Live Activities namespace (iOS only).

    Provides methods for managing Live Activities, which display
    real-time information on the iOS Lock Screen and Dynamic Island.
    """

    def __init__(self, service: "OneSignal"):
        self._service = service

    async def enter(self, activity_id: str, token: str) -> None:
        """
        Enter a Live Activity.

        Call this when the user starts a Live Activity that should receive
        push updates from OneSignal.

        Args:
            activity_id: A unique identifier for the Live Activity.
            token: The push token for the Live Activity.
        """
        await self._service._invoke_method(
            "live_activities_enter",
            {"activity_id": activity_id, "token": token},
        )

    async def exit(self, activity_id: str) -> None:
        """
        Exit a Live Activity.

        Call this when the Live Activity ends or the user dismisses it.

        Args:
            activity_id: The identifier of the Live Activity to exit.
        """
        await self._service._invoke_method(
            "live_activities_exit",
            {"activity_id": activity_id},
        )

    async def set_push_to_start_token(self, activity_type: str, token: str) -> None:
        """
        Set the push-to-start token for a Live Activity type.

        This allows OneSignal to start a Live Activity via push notification.

        Args:
            activity_type: The type identifier of the Live Activity.
            token: The push-to-start token.
        """
        await self._service._invoke_method(
            "live_activities_set_push_to_start_token",
            {"activity_type": activity_type, "token": token},
        )

    async def remove_push_to_start_token(self, activity_type: str) -> None:
        """
        Remove the push-to-start token for a Live Activity type.

        Args:
            activity_type: The type identifier of the Live Activity.
        """
        await self._service._invoke_method(
            "live_activities_remove_push_to_start_token",
            {"activity_type": activity_type},
        )

    async def setup_default(
        self,
        options: Optional[dict] = None,
    ) -> None:
        """
        Setup default Live Activity options.

        Args:
            options: Optional configuration options for Live Activities.
        """
        await self._service._invoke_method(
            "live_activities_setup_default",
            {"options": options or {}},
        )
