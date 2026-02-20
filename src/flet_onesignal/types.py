"""
Types, enums, and dataclasses for flet-onesignal.

This module defines all event types, enums, and data structures used
throughout the flet-onesignal SDK.
"""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional

import flet as ft

if TYPE_CHECKING:
    pass


class OSLogLevel(Enum):
    """OneSignal SDK log levels.

    Controls the verbosity of SDK console/logcat output.

    Example:
        ```python
        onesignal = fos.OneSignal(
            app_id="your-app-id",
            log_level=fos.OSLogLevel.DEBUG,
        )
        ```
    """

    NONE = "none"
    """No logging."""

    FATAL = "fatal"
    """Only fatal errors."""

    ERROR = "error"
    """Errors and fatal errors."""

    WARN = "warn"
    """Warnings and above."""

    INFO = "info"
    """Informational messages and above."""

    DEBUG = "debug"
    """Debug messages and above."""

    VERBOSE = "verbose"
    """All messages including verbose details."""


# -----------------------------------------------------------------------------
# Notification Events
# -----------------------------------------------------------------------------


@dataclass
class OSNotificationClickEvent(ft.Event["OneSignal"]):
    """Event fired when a user clicks on a notification.

    Example:
        ```python
        def on_click(e: fos.OSNotificationClickEvent):
            print(f"Clicked: {e.notification}")
            print(f"Action: {e.action_id}")

        onesignal = fos.OneSignal(
            app_id="...",
            on_notification_click=on_click,
        )
        ```
    """

    notification: dict
    """The notification payload as a dictionary."""

    action_id: Optional[str] = None
    """The action button ID if the user tapped an action button, or `None`."""


@dataclass
class OSNotificationWillDisplayEvent(ft.Event["OneSignal"]):
    """Event fired when a notification is about to be displayed in foreground.

    Use this to intercept and optionally suppress notification display
    when the app is in the foreground.

    Example:
        ```python
        async def on_foreground(e: fos.OSNotificationWillDisplayEvent):
            # Suppress display
            await onesignal.notifications.prevent_default(e.notification_id)

        onesignal = fos.OneSignal(
            app_id="...",
            on_notification_foreground=on_foreground,
        )
        ```
    """

    notification: dict
    """The notification payload as a dictionary."""

    notification_id: Optional[str] = None
    """The notification ID, used with `prevent_default()` and `display()`."""


@dataclass
class OSPermissionChangeEvent(ft.Event["OneSignal"]):
    """Event fired when notification permission status changes."""

    permission: bool = False
    """`True` if notifications are now permitted, `False` otherwise."""


# -----------------------------------------------------------------------------
# User Events
# -----------------------------------------------------------------------------


@dataclass
class OSUserState:
    """Represents the current OneSignal user state."""

    onesignal_id: Optional[str] = None
    """The OneSignal-generated user ID."""

    external_id: Optional[str] = None
    """The external user ID set via `login()`."""


@dataclass
class OSUserChangedEvent(ft.Event["OneSignal"]):
    """Event fired when the user state changes."""

    onesignal_id: Optional[str] = None
    """The OneSignal-generated user ID."""

    external_id: Optional[str] = None
    """The external user ID set via `login()`."""

    @property
    def state(self) -> OSUserState:
        """Get the user state as an OSUserState object."""
        return OSUserState(
            onesignal_id=self.onesignal_id,
            external_id=self.external_id,
        )


@dataclass
class OSPushSubscriptionChangedEvent(ft.Event["OneSignal"]):
    """Event fired when push subscription state changes."""

    id: Optional[str] = None
    """The push subscription ID."""

    token: Optional[str] = None
    """The push token (FCM/APNs)."""

    opted_in: bool = False
    """`True` if the user is opted in to push notifications."""


# -----------------------------------------------------------------------------
# In-App Message Events
# -----------------------------------------------------------------------------


@dataclass
class OSInAppMessageClickResult:
    """Result of an in-app message click action."""

    action_id: Optional[str] = None
    """The action ID defined in the OneSignal dashboard."""

    url: Optional[str] = None
    """The URL associated with the click action, if any."""

    url_target: Optional[str] = None
    """The URL target (`_blank`, `_self`, etc.)."""

    closing_message: bool = False
    """`True` if the click action closes the in-app message."""


@dataclass
class OSInAppMessageClickEvent(ft.Event["OneSignal"]):
    """Event fired when a user clicks on an in-app message.

    Example:
        ```python
        def on_iam_click(e: fos.OSInAppMessageClickEvent):
            print(f"Action: {e.result.action_id}")
            print(f"URL: {e.result.url}")
        ```
    """

    message: dict = None
    """The in-app message payload."""

    action_id: Optional[str] = None
    """The action ID defined in the OneSignal dashboard."""

    url: Optional[str] = None
    """The URL associated with the click action, if any."""

    url_target: Optional[str] = None
    """The URL target (`_blank`, `_self`, etc.)."""

    closing_message: bool = False
    """`True` if the click action closes the in-app message."""

    @property
    def result(self) -> OSInAppMessageClickResult:
        """Get the click result as an OSInAppMessageClickResult object."""
        return OSInAppMessageClickResult(
            action_id=self.action_id,
            url=self.url,
            url_target=self.url_target,
            closing_message=self.closing_message,
        )


@dataclass
class OSInAppMessageWillDisplayEvent(ft.Event["OneSignal"]):
    """Event fired before an in-app message is displayed."""

    message: dict = None
    """The in-app message payload."""


@dataclass
class OSInAppMessageDidDisplayEvent(ft.Event["OneSignal"]):
    """Event fired after an in-app message is displayed."""

    message: dict = None
    """The in-app message payload."""


@dataclass
class OSInAppMessageWillDismissEvent(ft.Event["OneSignal"]):
    """Event fired before an in-app message is dismissed."""

    message: dict = None
    """The in-app message payload."""


@dataclass
class OSInAppMessageDidDismissEvent(ft.Event["OneSignal"]):
    """Event fired after an in-app message is dismissed."""

    message: dict = None
    """The in-app message payload."""


# -----------------------------------------------------------------------------
# Error Event
# -----------------------------------------------------------------------------


@dataclass
class OSErrorEvent(ft.Event["OneSignal"]):
    """Event fired when an error occurs in the SDK.

    Example:
        ```python
        def on_error(e: fos.OSErrorEvent):
            print(f"Error in {e.method}: {e.message}")
        ```
    """

    method: Optional[str] = None
    """The SDK method that caused the error."""

    message: Optional[str] = None
    """The error message."""

    stack_trace: Optional[str] = None
    """The stack trace, if available."""
