"""
Example application demonstrating flet-onesignal integration.

This example shows both imperative and event-driven patterns for using
the OneSignal SDK with Flet applications.
"""

import flet as ft

import flet_onesignal as fos

# Replace with your actual OneSignal App ID
ONESIGNAL_APP_ID = "example-123a-12a3-1a23-abcd1ef23g45"


async def main(page: ft.Page):
    """Main application entry point."""

    page.title = "OneSignal Test"
    page.appbar = ft.AppBar(
        title=ft.Text("OneSignal Test"),
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
    )

    # Text fields for displaying data
    onesignal_id_field = ft.TextField(
        label="OneSignal ID",
        read_only=True,
        expand=True,
    )
    external_id_field = ft.TextField(
        label="External User ID",
        read_only=True,
        expand=True,
    )
    external_id_input = ft.TextField(
        label="Set External User ID",
        hint_text="Enter user ID to login",
        expand=True,
    )
    language_input = ft.TextField(
        label="Language Code",
        hint_text="en, pt, es...",
        value="en",
        width=150,
    )
    tag_key_input = ft.TextField(
        label="Tag Key",
        hint_text="key",
        width=150,
    )
    tag_value_input = ft.TextField(
        label="Tag Value",
        hint_text="value",
        width=150,
    )

    # List view for event logs
    log_list = ft.ListView(
        padding=ft.Padding.all(10),
        spacing=5,
        expand=True,
        auto_scroll=True,
    )

    def add_log(message: str):
        """Add a message to the log list."""
        log_list.controls.append(ft.Text(message, size=12, selectable=True))
        page.update()

    # -------------------------------------------------------------------------
    # Event handlers
    # -------------------------------------------------------------------------

    def on_notification_click(e: fos.OSNotificationClickEvent):
        """Handle notification click events."""
        add_log(f"[Notification Click] {e.notification}")

    def on_notification_foreground(e: fos.OSNotificationWillDisplayEvent):
        """Handle foreground notification events."""
        add_log(f"[Notification Foreground] {e.notification}")

    def on_permission_change(e: fos.OSPermissionChangeEvent):
        """Handle permission change events."""
        add_log(f"[Permission Change] Granted: {e.permission}")

    def on_user_change(e: fos.OSUserChangedEvent):
        """Handle user state change events."""
        add_log(
            f"[User Change] OneSignal ID: {e.state.onesignal_id}, External ID: {e.state.external_id}"
        )

    def on_push_subscription_change(e: fos.OSPushSubscriptionChangedEvent):
        """Handle push subscription change events."""
        add_log(f"[Push Subscription] ID: {e.id}, Opted In: {e.opted_in}")

    def on_iam_click(e: fos.OSInAppMessageClickEvent):
        """Handle in-app message click events."""
        add_log(f"[IAM Click] Action: {e.result.action_id}, URL: {e.result.url}")

    def on_iam_will_display(e: fos.OSInAppMessageWillDisplayEvent):
        """Handle in-app message will display events."""
        add_log(f"[IAM Will Display] {e.message}")

    def on_iam_did_display(e: fos.OSInAppMessageDidDisplayEvent):
        """Handle in-app message did display events."""
        add_log("[IAM Did Display]")

    def on_iam_will_dismiss(e: fos.OSInAppMessageWillDismissEvent):
        """Handle in-app message will dismiss events."""
        add_log("[IAM Will Dismiss]")

    def on_iam_did_dismiss(e: fos.OSInAppMessageDidDismissEvent):
        """Handle in-app message did dismiss events."""
        add_log("[IAM Did Dismiss]")

    def on_error(e: fos.OSErrorEvent):
        """Handle error events."""
        add_log(f"[Error] {e.method}: {e.message}")

    # -------------------------------------------------------------------------
    # Create OneSignal service with event handlers
    # -------------------------------------------------------------------------

    onesignal = fos.OneSignal(
        app_id=ONESIGNAL_APP_ID,
        log_level=fos.OSLogLevel.DEBUG,
        visual_alert_level=fos.OSLogLevel.DEBUG,
        on_notification_click=on_notification_click,
        on_notification_foreground=on_notification_foreground,
        on_permission_change=on_permission_change,
        on_user_change=on_user_change,
        on_push_subscription_change=on_push_subscription_change,
        on_iam_click=on_iam_click,
        on_iam_will_display=on_iam_will_display,
        on_iam_did_display=on_iam_did_display,
        on_iam_will_dismiss=on_iam_will_dismiss,
        on_iam_did_dismiss=on_iam_did_dismiss,
        on_error=on_error,
    )

    # Add to page services (NOT overlay - services are not visual controls)
    page.services.append(onesignal)

    # -------------------------------------------------------------------------
    # Button handlers (imperative API usage)
    # -------------------------------------------------------------------------

    async def get_onesignal_id(e):
        """Get the OneSignal ID."""
        result = await onesignal.user.get_onesignal_id()
        onesignal_id_field.value = result or "Not available"
        add_log(f"OneSignal ID: {result}")
        page.update()

    async def get_external_id(e):
        """Get the external user ID."""
        result = await onesignal.user.get_external_id()
        external_id_field.value = result or "Not set"
        add_log(f"External ID: {result}")
        page.update()

    async def login(e):
        """Login with external user ID."""
        user_id = external_id_input.value
        if not user_id:
            add_log("Please enter an external user ID")
            return
        await onesignal.login(user_id)
        add_log(f"Logged in as: {user_id}")

    async def logout(e):
        """Logout the current user."""
        await onesignal.logout()
        external_id_input.value = ""
        add_log("Logged out")
        page.update()

    async def request_permission(e):
        """Request notification permission."""
        result = await onesignal.notifications.request_permission()
        add_log(f"Permission granted: {result}")

    async def set_language(e):
        """Set the user's language."""
        code = language_input.value
        if code:
            await onesignal.user.set_language(code)
            add_log(f"Language set to: {code}")

    async def add_tag(e):
        """Add a tag to the user."""
        key = tag_key_input.value
        value = tag_value_input.value
        if key and value:
            await onesignal.user.add_tag(key, value)
            add_log(f"Tag added: {key}={value}")
        else:
            add_log("Please enter both tag key and value")

    async def remove_tag(e):
        """Remove a tag from the user."""
        key = tag_key_input.value
        if key:
            await onesignal.user.remove_tag(key)
            add_log(f"Tag removed: {key}")
        else:
            add_log("Please enter a tag key to remove")

    async def get_tags(e):
        """Get all tags for the user."""
        tags = await onesignal.user.get_tags()
        add_log(f"Tags: {tags}")

    async def opt_in_push(e):
        """Opt in to push notifications."""
        await onesignal.user.opt_in_push()
        add_log("Opted in to push notifications")

    async def opt_out_push(e):
        """Opt out of push notifications."""
        await onesignal.user.opt_out_push()
        add_log("Opted out of push notifications")

    async def clear_notifications(e):
        """Clear all notifications."""
        await onesignal.notifications.clear_all()
        add_log("Notifications cleared")

    def clear_logs(e):
        """Clear the log list."""
        log_list.controls.clear()
        page.update()

    # -------------------------------------------------------------------------
    # Build UI
    # -------------------------------------------------------------------------

    # ID display row
    id_row = ft.Row(
        controls=[onesignal_id_field, external_id_field],
        spacing=10,
    )

    # ID action buttons
    id_buttons = ft.Row(
        controls=[
            ft.Button("Get OneSignal ID", on_click=get_onesignal_id),
            ft.Button("Get External ID", on_click=get_external_id),
        ],
        spacing=10,
        wrap=True,
    )

    # Login row
    login_row = ft.Row(
        controls=[
            external_id_input,
            ft.Button("Login", on_click=login),
            ft.Button("Logout", on_click=logout),
        ],
        spacing=10,
    )

    # Permission and language row
    settings_row = ft.Row(
        controls=[
            ft.Button("Request Permission", on_click=request_permission),
            language_input,
            ft.Button("Set Language", on_click=set_language),
        ],
        spacing=10,
        wrap=True,
    )

    # Tags row
    tags_row = ft.Row(
        controls=[
            tag_key_input,
            tag_value_input,
            ft.Button("Add Tag", on_click=add_tag),
            ft.Button("Remove Tag", on_click=remove_tag),
            ft.Button("Get Tags", on_click=get_tags),
        ],
        spacing=10,
        wrap=True,
    )

    # Push subscription row
    push_row = ft.Row(
        controls=[
            ft.Button("Opt In Push", on_click=opt_in_push),
            ft.Button("Opt Out Push", on_click=opt_out_push),
            ft.Button("Clear Notifications", on_click=clear_notifications),
        ],
        spacing=10,
        wrap=True,
    )

    # Log section with fixed height for scrollable parent
    log_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Event Logs", weight=ft.FontWeight.BOLD),
                        ft.Button("Clear", on_click=clear_logs),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(
                    content=log_list,
                    border=ft.Border.all(1, ft.Colors.GREY_400),
                    border_radius=5,
                    height=200,
                ),
            ],
        ),
    )

    # Add all controls to page with scroll enabled
    page.add(
        ft.Column(
            controls=[
                id_row,
                id_buttons,
                ft.Divider(),
                login_row,
                ft.Divider(),
                settings_row,
                ft.Divider(),
                tags_row,
                ft.Divider(),
                push_row,
                ft.Divider(),
                log_section,
            ],
            expand=True,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )
    )

    add_log("OneSignal initialized. Ready to test!")


if __name__ == "__main__":
    ft.run(main)