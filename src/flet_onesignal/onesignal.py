"""
OneSignal Service for flet-onesignal.

This module provides the main OneSignal class that integrates with Flet
applications using the new Flet 0.80.x extension pattern.
"""

from typing import Any, Optional

import flet as ft
from flet.core.event_handler import EventHandler

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


@ft.control("onesignal")
class OneSignal(ft.Service):
    """
    OneSignal integration for Flet applications.

    This is the main entry point for the OneSignal SDK. Add it to your
    page's overlay list to enable push notifications and in-app messaging.

    Example (Imperative):
        ```python
        import flet as ft
        import flet_onesignal as fos

        async def main(page: ft.Page):
            onesignal = fos.OneSignal(app_id="your-app-id")
            page.overlay.append(onesignal)
            await page.update_async()

            # Request notification permission
            granted = await onesignal.notifications.request_permission()

            # Login a user
            await onesignal.login("user-123")

        ft.run(main)
        ```

    Example (Declarative):
        ```python
        import flet as ft
        import flet_onesignal as fos

        def main(page: ft.Page):
            def handle_notification_click(e: fos.OSNotificationClickEvent):
                print(f"Notification clicked: {e.notification}")

            page.overlay.append(
                fos.OneSignal(
                    app_id="your-app-id",
                    on_notification_click=handle_notification_click,
                )
            )

        ft.run(main)
        ```

    Args:
        app_id: Your OneSignal App ID.
        log_level: Optional SDK log level (default: None, uses SDK default).
        require_consent: Whether to require user consent before collecting data.
        on_notification_click: Handler for notification click events.
        on_notification_foreground: Handler for foreground notification events.
        on_permission_change: Handler for permission change events.
        on_user_change: Handler for user state change events.
        on_push_subscription_change: Handler for push subscription change events.
        on_iam_click: Handler for in-app message click events.
        on_iam_will_display: Handler for in-app message will display events.
        on_iam_did_display: Handler for in-app message did display events.
        on_iam_will_dismiss: Handler for in-app message will dismiss events.
        on_iam_did_dismiss: Handler for in-app message did dismiss events.
        on_error: Handler for error events.
    """

    def __init__(
        self,
        app_id: str,
        log_level: Optional[OSLogLevel] = None,
        require_consent: bool = False,
        # Notification events
        on_notification_click: Optional[ft.OptionalEventCallable[OSNotificationClickEvent]] = None,
        on_notification_foreground: Optional[
            ft.OptionalEventCallable[OSNotificationWillDisplayEvent]
        ] = None,
        on_permission_change: Optional[ft.OptionalEventCallable[OSPermissionChangeEvent]] = None,
        # User events
        on_user_change: Optional[ft.OptionalEventCallable[OSUserChangedEvent]] = None,
        on_push_subscription_change: Optional[
            ft.OptionalEventCallable[OSPushSubscriptionChangedEvent]
        ] = None,
        # In-App Message events
        on_iam_click: Optional[ft.OptionalEventCallable[OSInAppMessageClickEvent]] = None,
        on_iam_will_display: Optional[
            ft.OptionalEventCallable[OSInAppMessageWillDisplayEvent]
        ] = None,
        on_iam_did_display: Optional[
            ft.OptionalEventCallable[OSInAppMessageDidDisplayEvent]
        ] = None,
        on_iam_will_dismiss: Optional[
            ft.OptionalEventCallable[OSInAppMessageWillDismissEvent]
        ] = None,
        on_iam_did_dismiss: Optional[
            ft.OptionalEventCallable[OSInAppMessageDidDismissEvent]
        ] = None,
        # Error events
        on_error: Optional[ft.OptionalEventCallable[OSErrorEvent]] = None,
        # Control properties
        ref: Optional[ft.Ref] = None,
        data: Any = None,
    ):
        super().__init__(ref=ref, data=data)

        # Store configuration
        self._app_id = app_id
        self._log_level = log_level
        self._require_consent = require_consent

        # Initialize sub-modules
        self._debug = OneSignalDebug(self)
        self._user = OneSignalUser(self)
        self._notifications = OneSignalNotifications(self)
        self._in_app_messages = OneSignalInAppMessages(self)
        self._location = OneSignalLocation(self)
        self._session = OneSignalSession(self)
        self._live_activities = OneSignalLiveActivities(self)

        # Setup event handlers
        self.__on_notification_click = EventHandler(
            result_converter=lambda e: OSNotificationClickEvent(e)
        )
        self._add_event_handler("notification_click", self.__on_notification_click.get_handler())

        self.__on_notification_foreground = EventHandler(
            result_converter=lambda e: OSNotificationWillDisplayEvent(e)
        )
        self._add_event_handler(
            "notification_foreground", self.__on_notification_foreground.get_handler()
        )

        self.__on_permission_change = EventHandler(
            result_converter=lambda e: OSPermissionChangeEvent(e)
        )
        self._add_event_handler("permission_change", self.__on_permission_change.get_handler())

        self.__on_user_change = EventHandler(result_converter=lambda e: OSUserChangedEvent(e))
        self._add_event_handler("user_change", self.__on_user_change.get_handler())

        self.__on_push_subscription_change = EventHandler(
            result_converter=lambda e: OSPushSubscriptionChangedEvent(e)
        )
        self._add_event_handler(
            "push_subscription_change", self.__on_push_subscription_change.get_handler()
        )

        self.__on_iam_click = EventHandler(result_converter=lambda e: OSInAppMessageClickEvent(e))
        self._add_event_handler("iam_click", self.__on_iam_click.get_handler())

        self.__on_iam_will_display = EventHandler(
            result_converter=lambda e: OSInAppMessageWillDisplayEvent(e)
        )
        self._add_event_handler("iam_will_display", self.__on_iam_will_display.get_handler())

        self.__on_iam_did_display = EventHandler(
            result_converter=lambda e: OSInAppMessageDidDisplayEvent(e)
        )
        self._add_event_handler("iam_did_display", self.__on_iam_did_display.get_handler())

        self.__on_iam_will_dismiss = EventHandler(
            result_converter=lambda e: OSInAppMessageWillDismissEvent(e)
        )
        self._add_event_handler("iam_will_dismiss", self.__on_iam_will_dismiss.get_handler())

        self.__on_iam_did_dismiss = EventHandler(
            result_converter=lambda e: OSInAppMessageDidDismissEvent(e)
        )
        self._add_event_handler("iam_did_dismiss", self.__on_iam_did_dismiss.get_handler())

        self.__on_error = EventHandler(result_converter=lambda e: OSErrorEvent(e))
        self._add_event_handler("error", self.__on_error.get_handler())

        # Set initial handlers
        self.on_notification_click = on_notification_click
        self.on_notification_foreground = on_notification_foreground
        self.on_permission_change = on_permission_change
        self.on_user_change = on_user_change
        self.on_push_subscription_change = on_push_subscription_change
        self.on_iam_click = on_iam_click
        self.on_iam_will_display = on_iam_will_display
        self.on_iam_did_display = on_iam_did_display
        self.on_iam_will_dismiss = on_iam_will_dismiss
        self.on_iam_did_dismiss = on_iam_did_dismiss
        self.on_error = on_error

    def _get_control_name(self):
        return "onesignal"

    def before_update(self):
        super().before_update()
        self._set_attr("appId", self._app_id)
        if self._log_level is not None:
            self._set_attr("logLevel", self._log_level.value)
        self._set_attr("requireConsent", self._require_consent)

    # -------------------------------------------------------------------------
    # Sub-modules as properties
    # -------------------------------------------------------------------------

    @property
    def debug(self) -> OneSignalDebug:
        """Access the Debug namespace for SDK logging configuration."""
        return self._debug

    @property
    def user(self) -> OneSignalUser:
        """Access the User namespace for identity, tags, aliases, email, SMS."""
        return self._user

    @property
    def notifications(self) -> OneSignalNotifications:
        """Access the Notifications namespace for push notification management."""
        return self._notifications

    @property
    def in_app_messages(self) -> OneSignalInAppMessages:
        """Access the In-App Messages namespace for IAM triggers and control."""
        return self._in_app_messages

    @property
    def location(self) -> OneSignalLocation:
        """Access the Location namespace for location sharing."""
        return self._location

    @property
    def session(self) -> OneSignalSession:
        """Access the Session namespace for outcomes tracking."""
        return self._session

    @property
    def live_activities(self) -> OneSignalLiveActivities:
        """Access the Live Activities namespace (iOS only)."""
        return self._live_activities

    # -------------------------------------------------------------------------
    # Configuration properties
    # -------------------------------------------------------------------------

    @property
    def app_id(self) -> str:
        """Get the OneSignal App ID."""
        return self._app_id

    @app_id.setter
    def app_id(self, value: str):
        """Set the OneSignal App ID."""
        self._app_id = value
        self.update()

    @property
    def log_level(self) -> Optional[OSLogLevel]:
        """Get the SDK log level."""
        return self._log_level

    @log_level.setter
    def log_level(self, value: Optional[OSLogLevel]):
        """Set the SDK log level."""
        self._log_level = value
        self.update()

    @property
    def require_consent(self) -> bool:
        """Get whether consent is required before collecting data."""
        return self._require_consent

    @require_consent.setter
    def require_consent(self, value: bool):
        """Set whether consent is required before collecting data."""
        self._require_consent = value
        self.update()

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

    async def _invoke_method(
        self,
        method_name: str,
        arguments: Optional[dict] = None,
        wait_for_result: bool = True,
        wait_timeout: float = 25,
    ) -> Optional[str]:
        """
        Internal method for invoking Flutter methods.

        This is used by sub-modules to communicate with the Dart side.
        """
        return await self.invoke_method_async(
            method_name=method_name,
            arguments=arguments or {},
            wait_for_result=wait_for_result,
            wait_timeout=wait_timeout,
        )

    # -------------------------------------------------------------------------
    # Event handler properties
    # -------------------------------------------------------------------------

    @property
    def on_notification_click(self) -> Optional[ft.OptionalEventCallable[OSNotificationClickEvent]]:
        """Handler called when a notification is clicked."""
        return self.__on_notification_click.handler

    @on_notification_click.setter
    def on_notification_click(
        self, handler: Optional[ft.OptionalEventCallable[OSNotificationClickEvent]]
    ):
        self.__on_notification_click.handler = handler
        self._set_attr("onNotificationClick", True if handler else None)

    @property
    def on_notification_foreground(
        self,
    ) -> Optional[ft.OptionalEventCallable[OSNotificationWillDisplayEvent]]:
        """Handler called when a notification is received in foreground."""
        return self.__on_notification_foreground.handler

    @on_notification_foreground.setter
    def on_notification_foreground(
        self, handler: Optional[ft.OptionalEventCallable[OSNotificationWillDisplayEvent]]
    ):
        self.__on_notification_foreground.handler = handler
        self._set_attr("onNotificationForeground", True if handler else None)

    @property
    def on_permission_change(
        self,
    ) -> Optional[ft.OptionalEventCallable[OSPermissionChangeEvent]]:
        """Handler called when notification permission status changes."""
        return self.__on_permission_change.handler

    @on_permission_change.setter
    def on_permission_change(
        self, handler: Optional[ft.OptionalEventCallable[OSPermissionChangeEvent]]
    ):
        self.__on_permission_change.handler = handler
        self._set_attr("onPermissionChange", True if handler else None)

    @property
    def on_user_change(self) -> Optional[ft.OptionalEventCallable[OSUserChangedEvent]]:
        """Handler called when user state changes."""
        return self.__on_user_change.handler

    @on_user_change.setter
    def on_user_change(self, handler: Optional[ft.OptionalEventCallable[OSUserChangedEvent]]):
        self.__on_user_change.handler = handler
        self._set_attr("onUserChange", True if handler else None)

    @property
    def on_push_subscription_change(
        self,
    ) -> Optional[ft.OptionalEventCallable[OSPushSubscriptionChangedEvent]]:
        """Handler called when push subscription state changes."""
        return self.__on_push_subscription_change.handler

    @on_push_subscription_change.setter
    def on_push_subscription_change(
        self, handler: Optional[ft.OptionalEventCallable[OSPushSubscriptionChangedEvent]]
    ):
        self.__on_push_subscription_change.handler = handler
        self._set_attr("onPushSubscriptionChange", True if handler else None)

    @property
    def on_iam_click(self) -> Optional[ft.OptionalEventCallable[OSInAppMessageClickEvent]]:
        """Handler called when an in-app message is clicked."""
        return self.__on_iam_click.handler

    @on_iam_click.setter
    def on_iam_click(self, handler: Optional[ft.OptionalEventCallable[OSInAppMessageClickEvent]]):
        self.__on_iam_click.handler = handler
        self._set_attr("onIamClick", True if handler else None)

    @property
    def on_iam_will_display(
        self,
    ) -> Optional[ft.OptionalEventCallable[OSInAppMessageWillDisplayEvent]]:
        """Handler called before an in-app message is displayed."""
        return self.__on_iam_will_display.handler

    @on_iam_will_display.setter
    def on_iam_will_display(
        self, handler: Optional[ft.OptionalEventCallable[OSInAppMessageWillDisplayEvent]]
    ):
        self.__on_iam_will_display.handler = handler
        self._set_attr("onIamWillDisplay", True if handler else None)

    @property
    def on_iam_did_display(
        self,
    ) -> Optional[ft.OptionalEventCallable[OSInAppMessageDidDisplayEvent]]:
        """Handler called after an in-app message is displayed."""
        return self.__on_iam_did_display.handler

    @on_iam_did_display.setter
    def on_iam_did_display(
        self, handler: Optional[ft.OptionalEventCallable[OSInAppMessageDidDisplayEvent]]
    ):
        self.__on_iam_did_display.handler = handler
        self._set_attr("onIamDidDisplay", True if handler else None)

    @property
    def on_iam_will_dismiss(
        self,
    ) -> Optional[ft.OptionalEventCallable[OSInAppMessageWillDismissEvent]]:
        """Handler called before an in-app message is dismissed."""
        return self.__on_iam_will_dismiss.handler

    @on_iam_will_dismiss.setter
    def on_iam_will_dismiss(
        self, handler: Optional[ft.OptionalEventCallable[OSInAppMessageWillDismissEvent]]
    ):
        self.__on_iam_will_dismiss.handler = handler
        self._set_attr("onIamWillDismiss", True if handler else None)

    @property
    def on_iam_did_dismiss(
        self,
    ) -> Optional[ft.OptionalEventCallable[OSInAppMessageDidDismissEvent]]:
        """Handler called after an in-app message is dismissed."""
        return self.__on_iam_did_dismiss.handler

    @on_iam_did_dismiss.setter
    def on_iam_did_dismiss(
        self, handler: Optional[ft.OptionalEventCallable[OSInAppMessageDidDismissEvent]]
    ):
        self.__on_iam_did_dismiss.handler = handler
        self._set_attr("onIamDidDismiss", True if handler else None)

    @property
    def on_error(self) -> Optional[ft.OptionalEventCallable[OSErrorEvent]]:
        """Handler called when an error occurs."""
        return self.__on_error.handler

    @on_error.setter
    def on_error(self, handler: Optional[ft.OptionalEventCallable[OSErrorEvent]]):
        self.__on_error.handler = handler
        self._set_attr("onError", True if handler else None)
