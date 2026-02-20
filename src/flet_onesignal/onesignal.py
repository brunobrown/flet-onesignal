"""
OneSignal Service for flet-onesignal.

This module provides the main OneSignal class that integrates with Flet
applications using the Flet 0.80.x extension pattern.
"""

from dataclasses import field
from typing import Any, Optional

import flet as ft

from flet_onesignal.debug import OneSignalDebug
from flet_onesignal.in_app_messages import OneSignalInAppMessages
from flet_onesignal.live_activities import OneSignalLiveActivities
from flet_onesignal.location import OneSignalLocation
from flet_onesignal.notifications import OneSignalNotifications
from flet_onesignal.session import OneSignalSession
from flet_onesignal.types import (
    OSErrorEvent,
    OSInAppMessageClickEvent,
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
)
from flet_onesignal.user import OneSignalUser


@ft.control("OneSignal")
class OneSignal(ft.Service):
    """
    OneSignal integration for Flet applications.

    This is the main entry point for the OneSignal SDK. Add it to your
    page's services list to enable push notifications and in-app messaging.

    Example:
        ```python
        import flet as ft
        import flet_onesignal as fos

        async def main(page: ft.Page):
            onesignal = fos.OneSignal(app_id="your-app-id")
            page.services.append(onesignal)  # Use services, NOT overlay!

            # Request notification permission
            granted = await onesignal.notifications.request_permission()

            # Login a user
            await onesignal.login("user-123")

        ft.run(main)
        ```

    Attributes:
        app_id: Your OneSignal App ID.
        log_level: Optional SDK log level for console/logcat output.
        visual_alert_level: Optional SDK log level for visual alerts (iOS toast notifications).
        require_consent: Whether to require user consent before collecting data.
    """

    app_id: str = ""
    """Your OneSignal App ID from the dashboard."""

    log_level: Optional[OSLogLevel] = None
    """SDK log level for console/logcat output. Defaults to `None` (no logging)."""

    visual_alert_level: Optional[OSLogLevel] = None
    """SDK log level for visual alerts (iOS toast notifications). Defaults to `None`."""

    require_consent: bool = False
    """Whether to require user consent before the SDK collects data (GDPR compliance)."""

    on_notification_click: Optional[ft.EventHandler[OSNotificationClickEvent]] = None
    """Called when the user taps on a notification."""

    on_notification_foreground: Optional[ft.EventHandler[OSNotificationWillDisplayEvent]] = None
    """Called when a notification is received while the app is in the foreground."""

    on_permission_change: Optional[ft.EventHandler[OSPermissionChangeEvent]] = None
    """Called when the notification permission status changes."""

    on_user_change: Optional[ft.EventHandler[OSUserChangedEvent]] = None
    """Called when the OneSignal user state changes."""

    on_push_subscription_change: Optional[ft.EventHandler[OSPushSubscriptionChangedEvent]] = None
    """Called when the push subscription state changes."""

    on_iam_click: Optional[ft.EventHandler[OSInAppMessageClickEvent]] = None
    """Called when the user clicks on an in-app message."""

    on_iam_will_display: Optional[ft.EventHandler[OSInAppMessageWillDisplayEvent]] = None
    """Called before an in-app message is displayed."""

    on_iam_did_display: Optional[ft.EventHandler[OSInAppMessageDidDisplayEvent]] = None
    """Called after an in-app message is displayed."""

    on_iam_will_dismiss: Optional[ft.EventHandler[OSInAppMessageWillDismissEvent]] = None
    """Called before an in-app message is dismissed."""

    on_iam_did_dismiss: Optional[ft.EventHandler[OSInAppMessageDidDismissEvent]] = None
    """Called after an in-app message is dismissed."""

    on_error: Optional[ft.EventHandler[OSErrorEvent]] = None
    """Called when an error occurs in the SDK."""

    # Internal sub-modules (not sent to Flutter)
    _debug: OneSignalDebug = field(default=None, init=False, metadata={"skip": True})
    _user: OneSignalUser = field(default=None, init=False, metadata={"skip": True})
    _notifications: OneSignalNotifications = field(
        default=None, init=False, metadata={"skip": True}
    )
    _in_app_messages: OneSignalInAppMessages = field(
        default=None, init=False, metadata={"skip": True}
    )
    _location: OneSignalLocation = field(default=None, init=False, metadata={"skip": True})
    _session: OneSignalSession = field(default=None, init=False, metadata={"skip": True})
    _live_activities: OneSignalLiveActivities = field(
        default=None, init=False, metadata={"skip": True}
    )

    def init(self):
        """Initialize the service and sub-modules."""
        super().init()
        # Initialize sub-modules
        self._debug = OneSignalDebug(self)
        self._user = OneSignalUser(self)
        self._notifications = OneSignalNotifications(self)
        self._in_app_messages = OneSignalInAppMessages(self)
        self._location = OneSignalLocation(self)
        self._session = OneSignalSession(self)
        self._live_activities = OneSignalLiveActivities(self)

    # -------------------------------------------------------------------------
    # Sub-modules as properties
    # -------------------------------------------------------------------------

    @property
    def debug(self) -> OneSignalDebug:
        """Access the Debug namespace for SDK logging configuration."""
        if self._debug is None:
            self._debug = OneSignalDebug(self)
        return self._debug

    @property
    def user(self) -> OneSignalUser:
        """Access the User namespace for identity, tags, aliases, email, SMS."""
        if self._user is None:
            self._user = OneSignalUser(self)
        return self._user

    @property
    def notifications(self) -> OneSignalNotifications:
        """Access the Notifications namespace for push notification management."""
        if self._notifications is None:
            self._notifications = OneSignalNotifications(self)
        return self._notifications

    @property
    def in_app_messages(self) -> OneSignalInAppMessages:
        """Access the In-App Messages namespace for IAM triggers and control."""
        if self._in_app_messages is None:
            self._in_app_messages = OneSignalInAppMessages(self)
        return self._in_app_messages

    @property
    def location(self) -> OneSignalLocation:
        """Access the Location namespace for location sharing."""
        if self._location is None:
            self._location = OneSignalLocation(self)
        return self._location

    @property
    def session(self) -> OneSignalSession:
        """Access the Session namespace for outcomes tracking."""
        if self._session is None:
            self._session = OneSignalSession(self)
        return self._session

    @property
    def live_activities(self) -> OneSignalLiveActivities:
        """Access the Live Activities namespace (iOS only)."""
        if self._live_activities is None:
            self._live_activities = OneSignalLiveActivities(self)
        return self._live_activities

    # -------------------------------------------------------------------------
    # Main methods
    # -------------------------------------------------------------------------

    async def login(self, external_id: str) -> None:
        """
        Login to OneSignal with an external user ID.

        This switches the user context to the specified user. If the user
        doesn't exist, a new user will be created.

        Args:
            external_id: Your unique identifier for the user.
        """
        await self._invoke_method("login", {"external_id": external_id})

    async def logout(self) -> None:
        """
        Logout the current user.

        After logout, a new anonymous device-scoped user will be created.
        """
        await self._invoke_method("logout")

    async def consent_given(self, given: bool) -> None:
        """
        Indicate whether the user has given consent for data collection.

        This method should be called after the user accepts or declines
        your privacy terms when require_consent is True.

        Args:
            given: True if the user gave consent, False otherwise.
        """
        await self._invoke_method("consent_given", {"given": given})

    # -------------------------------------------------------------------------
    # Internal method for sub-modules
    # -------------------------------------------------------------------------

    def _is_supported_platform(self) -> bool:
        """Check if the current platform supports OneSignal."""
        if not self.page:
            return False
        return self.page.platform in (
            ft.PagePlatform.ANDROID,
            ft.PagePlatform.IOS,
        )

    async def _invoke_method(
        self,
        method_name: str,
        arguments: Optional[dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Internal method for invoking Flutter methods.

        This is used by sub-modules to communicate with the Dart side.

        Args:
            method_name: Name of the method to invoke on the Dart side.
            arguments: Dictionary of arguments to pass to the method.
            timeout: Timeout in seconds. Defaults to 25 if None.

        Raises:
            FletUnsupportedPlatformException: If called on unsupported platform.
        """
        # Validate platform before invoking methods
        if not self._is_supported_platform():
            platform_name = self.page.platform.value if self.page else "unknown"
            raise ft.FletUnsupportedPlatformException(
                f"OneSignal is only supported on Android and iOS platforms. "
                f"Current platform: {platform_name}. "
                f"Method '{method_name}' cannot be executed."
            )

        # Use default timeout if not provided
        effective_timeout = timeout if timeout is not None else 25.0

        # Call parent's _invoke_method from BaseControl
        return await super()._invoke_method(
            method_name=method_name,
            arguments=arguments or {},
            timeout=effective_timeout,
        )
