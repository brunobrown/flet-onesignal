"""
Types, enums, and dataclasses for flet-onesignal.
"""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional

import flet as ft

if TYPE_CHECKING:
    pass


class OSLogLevel(Enum):
    """OneSignal SDK log levels."""

    NONE = "none"
    FATAL = "fatal"
    ERROR = "error"
    WARN = "warn"
    INFO = "info"
    DEBUG = "debug"
    VERBOSE = "verbose"


# -----------------------------------------------------------------------------
# Notification Events
# -----------------------------------------------------------------------------


@dataclass
class OSNotificationClickEvent(ft.Event["OneSignal"]):
    """Event fired when a user clicks on a notification."""

    notification: dict
    action_id: Optional[str] = None


@dataclass
class OSNotificationWillDisplayEvent(ft.Event["OneSignal"]):
    """Event fired when a notification is about to be displayed in foreground."""

    notification: dict
    notification_id: Optional[str] = None


@dataclass
class OSPermissionChangeEvent(ft.Event["OneSignal"]):
    """Event fired when notification permission status changes."""

    permission: bool = False


# -----------------------------------------------------------------------------
# User Events
# -----------------------------------------------------------------------------


@dataclass
class OSUserState:
    """Represents the current OneSignal user state."""

    onesignal_id: Optional[str] = None
    external_id: Optional[str] = None


@dataclass
class OSUserChangedEvent(ft.Event["OneSignal"]):
    """Event fired when the user state changes."""

    onesignal_id: Optional[str] = None
    external_id: Optional[str] = None

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
    token: Optional[str] = None
    opted_in: bool = False


# -----------------------------------------------------------------------------
# In-App Message Events
# -----------------------------------------------------------------------------


@dataclass
class OSInAppMessageClickResult:
    """Result of an in-app message click."""

    action_id: Optional[str] = None
    url: Optional[str] = None
    url_target: Optional[str] = None
    closing_message: bool = False


@dataclass
class OSInAppMessageClickEvent(ft.Event["OneSignal"]):
    """Event fired when a user clicks on an in-app message."""

    message: dict = None
    action_id: Optional[str] = None
    url: Optional[str] = None
    url_target: Optional[str] = None
    closing_message: bool = False

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


@dataclass
class OSInAppMessageDidDisplayEvent(ft.Event["OneSignal"]):
    """Event fired after an in-app message is displayed."""

    message: dict = None


@dataclass
class OSInAppMessageWillDismissEvent(ft.Event["OneSignal"]):
    """Event fired before an in-app message is dismissed."""

    message: dict = None


@dataclass
class OSInAppMessageDidDismissEvent(ft.Event["OneSignal"]):
    """Event fired after an in-app message is dismissed."""

    message: dict = None


# -----------------------------------------------------------------------------
# Error Event
# -----------------------------------------------------------------------------


@dataclass
class OSErrorEvent(ft.Event["OneSignal"]):
    """Event fired when an error occurs."""

    method: Optional[str] = None
    message: Optional[str] = None
    stack_trace: Optional[str] = None
