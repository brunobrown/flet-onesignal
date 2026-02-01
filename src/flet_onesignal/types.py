"""
Types, enums, and dataclasses for flet-onesignal.
"""

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.core.control_event import ControlEvent


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
class OSNotificationClickEvent(ControlEvent):
    """Event fired when a user clicks on a notification."""

    notification: dict = field(default_factory=dict)
    action_id: Optional[str] = None

    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        data = json.loads(e.data) if e.data else {}
        self.notification = data.get("notification", {})
        self.action_id = data.get("action_id")


@dataclass
class OSNotificationWillDisplayEvent(ControlEvent):
    """Event fired when a notification is about to be displayed in foreground."""

    notification: dict = field(default_factory=dict)
    notification_id: Optional[str] = None

    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        data = json.loads(e.data) if e.data else {}
        self.notification = data.get("notification", {})
        self.notification_id = data.get("notification_id")


@dataclass
class OSPermissionChangeEvent(ControlEvent):
    """Event fired when notification permission status changes."""

    permission: bool = False

    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        data = json.loads(e.data) if e.data else {}
        self.permission = data.get("permission", False)


# -----------------------------------------------------------------------------
# User Events
# -----------------------------------------------------------------------------


@dataclass
class OSUserState:
    """Represents the current OneSignal user state."""

    onesignal_id: Optional[str] = None
    external_id: Optional[str] = None


@dataclass
class OSUserChangedEvent(ControlEvent):
    """Event fired when the user state changes."""

    state: OSUserState = field(default_factory=OSUserState)

    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        data = json.loads(e.data) if e.data else {}
        self.state = OSUserState(
            onesignal_id=data.get("onesignal_id"),
            external_id=data.get("external_id"),
        )


@dataclass
class OSPushSubscriptionChangedEvent(ControlEvent):
    """Event fired when push subscription state changes."""

    id: Optional[str] = None
    token: Optional[str] = None
    opted_in: bool = False

    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        data = json.loads(e.data) if e.data else {}
        self.id = data.get("id")
        self.token = data.get("token")
        self.opted_in = data.get("opted_in", False)


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
class OSInAppMessageClickEvent(ControlEvent):
    """Event fired when a user clicks on an in-app message."""

    message: dict = field(default_factory=dict)
    result: OSInAppMessageClickResult = field(default_factory=OSInAppMessageClickResult)

    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        data = json.loads(e.data) if e.data else {}
        self.message = data.get("message", {})
        result_data = data.get("result", {})
        self.result = OSInAppMessageClickResult(
            action_id=result_data.get("action_id"),
            url=result_data.get("url"),
            url_target=result_data.get("url_target"),
            closing_message=result_data.get("closing_message", False),
        )


@dataclass
class OSInAppMessageEvent(ControlEvent):
    """Base event for in-app message lifecycle events."""

    message: dict = field(default_factory=dict)

    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        data = json.loads(e.data) if e.data else {}
        self.message = data.get("message", {})


class OSInAppMessageWillDisplayEvent(OSInAppMessageEvent):
    """Event fired before an in-app message is displayed."""

    pass


class OSInAppMessageDidDisplayEvent(OSInAppMessageEvent):
    """Event fired after an in-app message is displayed."""

    pass


class OSInAppMessageWillDismissEvent(OSInAppMessageEvent):
    """Event fired before an in-app message is dismissed."""

    pass


class OSInAppMessageDidDismissEvent(OSInAppMessageEvent):
    """Event fired after an in-app message is dismissed."""

    pass


# -----------------------------------------------------------------------------
# Error Event
# -----------------------------------------------------------------------------


@dataclass
class OSErrorEvent(ControlEvent):
    """Event fired when an error occurs."""

    method: Optional[str] = None
    message: Optional[str] = None
    stack_trace: Optional[str] = None

    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        data = json.loads(e.data) if e.data else {}
        self.method = data.get("method")
        self.message = data.get("message")
        self.stack_trace = data.get("stackTrace")
