"""
flet-onesignal - OneSignal integration for Flet applications.

This package provides a complete integration with the OneSignal SDK
for push notifications, in-app messaging, and user management.

Example:
    ```python
    import flet as ft
    import flet_onesignal as fos

    async def main(page: ft.Page):
        onesignal = fos.OneSignal(app_id="your-app-id")
        page.services.append(onesignal)  # Use services, NOT overlay!

        # Request notification permission
        granted = await onesignal.notifications.request_permission()

    ft.run(main)
    ```
"""

# Debug console for development
from flet_onesignal.console import (
    DebugConsole,
    LogLevel,
    setup_logging,
)

# Main service
# Sub-modules (can also be accessed via OneSignal instance)
from flet_onesignal.debug import OneSignalDebug
from flet_onesignal.in_app_messages import OneSignalInAppMessages

# Language codes
from flet_onesignal.languages import Language
from flet_onesignal.live_activities import OneSignalLiveActivities
from flet_onesignal.location import OneSignalLocation
from flet_onesignal.notifications import OneSignalNotifications
from flet_onesignal.onesignal import OneSignal
from flet_onesignal.session import OneSignalSession

# Types, enums, and events
from flet_onesignal.types import (
    OSErrorEvent,
    OSInAppMessageClickEvent,
    OSInAppMessageClickResult,
    OSInAppMessageDidDismissEvent,
    OSInAppMessageDidDisplayEvent,
    OSInAppMessageWillDismissEvent,
    OSInAppMessageWillDisplayEvent,
    OSLogLevel,
    OSNotificationClickEvent,
    OSNotificationWillDisplayEvent,
    OSPermissionChangeEvent,
    OSPushSubscriptionChangedEvent,
    OSUserChangedEvent,
    OSUserState,
)
from flet_onesignal.user import OneSignalUser

__all__ = [
    # Main service
    "OneSignal",
    # Sub-modules
    "OneSignalDebug",
    "OneSignalUser",
    "OneSignalNotifications",
    "OneSignalInAppMessages",
    "OneSignalLocation",
    "OneSignalSession",
    "OneSignalLiveActivities",
    # Debug console
    "DebugConsole",
    "LogLevel",
    "setup_logging",
    # Types and enums
    "OSLogLevel",
    "OSUserState",
    # Notification events
    "OSNotificationClickEvent",
    "OSNotificationWillDisplayEvent",
    "OSPermissionChangeEvent",
    # User events
    "OSUserChangedEvent",
    "OSPushSubscriptionChangedEvent",
    # In-App Message events
    "OSInAppMessageClickEvent",
    "OSInAppMessageClickResult",
    "OSInAppMessageWillDisplayEvent",
    "OSInAppMessageDidDisplayEvent",
    "OSInAppMessageWillDismissEvent",
    "OSInAppMessageDidDismissEvent",
    # Error event
    "OSErrorEvent",
    # Language
    "Language",
]

__version__ = "0.4.0"
