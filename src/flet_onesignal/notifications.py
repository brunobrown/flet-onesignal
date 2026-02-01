"""
OneSignal Notifications module for flet-onesignal.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flet_onesignal.onesignal import OneSignal


class OneSignalNotifications:
    """
    OneSignal Notifications namespace.

    Provides methods for managing push notification permissions, display,
    and lifecycle.
    """

    def __init__(self, service: "OneSignal"):
        self._service = service

    # -------------------------------------------------------------------------
    # Permission
    # -------------------------------------------------------------------------

    async def request_permission(
        self,
        fallback_to_settings: bool = True,
        wait_timeout: float = 25,
    ) -> bool:
        """
        Request permission to send push notifications.

        This will display the native system prompt to request push notification
        permission.

        Args:
            fallback_to_settings: If True and permission was previously denied,
                                  opens the app settings instead.
            wait_timeout: Maximum time to wait for user response (in seconds).

        Returns:
            True if permission was granted, False otherwise.
        """
        result = await self._service._invoke_method(
            "notifications_request_permission",
            {"fallback_to_settings": fallback_to_settings},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return result == "true"

    async def can_request_permission(self, wait_timeout: float = 25) -> bool:
        """
        Check if the app can request notification permission.

        Returns True if the device has not been prompted for push notification
        permission already.

        Returns:
            True if permission can be requested, False if already prompted.
        """
        result = await self._service._invoke_method(
            "notifications_can_request_permission",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return result == "true"

    async def get_permission(self, wait_timeout: float = 25) -> bool:
        """
        Get the current notification permission status.

        Returns:
            True if notifications are permitted, False otherwise.
        """
        result = await self._service._invoke_method(
            "notifications_get_permission",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return result == "true"

    async def register_for_provisional_authorization(self, wait_timeout: float = 25) -> bool:
        """
        Request provisional authorization for notifications (iOS only).

        Provisional authorization allows sending notifications quietly to the
        Notification Center without prompting the user first.

        Returns:
            True if authorization was granted, False otherwise.
        """
        result = await self._service._invoke_method(
            "notifications_register_provisional",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return result == "true"

    # -------------------------------------------------------------------------
    # Notification Management
    # -------------------------------------------------------------------------

    async def clear_all(self) -> None:
        """
        Remove all OneSignal notifications from the notification shade.
        """
        await self._service._invoke_method("notifications_clear_all")

    async def remove_notification(self, notification_id: int) -> None:
        """
        Remove a specific notification (Android only).

        Args:
            notification_id: The Android notification ID to remove.
        """
        await self._service._invoke_method(
            "notifications_remove",
            {"notification_id": notification_id},
        )

    async def remove_grouped_notifications(self, group: str) -> None:
        """
        Remove a group of notifications (Android only).

        Args:
            group: The notification group key to remove.
        """
        await self._service._invoke_method(
            "notifications_remove_grouped",
            {"group": group},
        )

    # -------------------------------------------------------------------------
    # Foreground Display Control
    # -------------------------------------------------------------------------

    async def prevent_default(self, notification_id: str) -> None:
        """
        Prevent a notification from being displayed when received in foreground.

        Call this from the on_foreground_will_display event handler to suppress
        the notification display.

        Args:
            notification_id: The notification ID from the event.
        """
        await self._service._invoke_method(
            "notifications_prevent_default",
            {"notification_id": notification_id},
        )

    async def display(self, notification_id: str) -> None:
        """
        Allow a notification to be displayed after calling prevent_default.

        Args:
            notification_id: The notification ID from the event.
        """
        await self._service._invoke_method(
            "notifications_display",
            {"notification_id": notification_id},
        )
