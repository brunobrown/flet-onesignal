"""
Notifications page - Permission and notification management.
"""

import flet as ft
from components.log_viewer import LogViewer
from components.page_layout import PageLayout
from context import AppCtx


@ft.component
def NotificationsPage():
    """
    Page for managing notification permissions and lifecycle.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    # Local state
    notification_id, set_notification_id = ft.use_state("")
    group_key, set_group_key = ft.use_state("")
    foreground_id, set_foreground_id = ft.use_state("")
    permission_status, set_permission_status = ft.use_state("")
    can_request, set_can_request = ft.use_state("")

    async def handle_request_permission(e):
        try:
            result = await onesignal.notifications.request_permission()
            set_permission_status("Granted" if result else "Denied")
            state.add_log(f"Permission: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error requesting permission: {ex}", "error")

    async def handle_can_request(e):
        try:
            result = await onesignal.notifications.can_request_permission()
            set_can_request("Yes" if result else "No")
            state.add_log(f"Can request permission: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_get_permission(e):
        try:
            result = await onesignal.notifications.get_permission()
            set_permission_status("Granted" if result else "Denied")
            state.add_log(f"Permission status: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_provisional_auth(e):
        try:
            result = await onesignal.notifications.register_for_provisional_authorization()
            state.add_log(f"Provisional authorization: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_clear_all(e):
        try:
            await onesignal.notifications.clear_all()
            state.add_log("All notifications cleared", "success")
        except Exception as ex:
            state.add_log(f"Error clearing: {ex}", "error")

    async def handle_remove_notification(e):
        if not notification_id:
            state.add_log("Enter the notification ID", "warning")
            return
        try:
            await onesignal.notifications.remove_notification(int(notification_id))
            state.add_log(f"Notification {notification_id} removed", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_remove_grouped(e):
        if not group_key:
            state.add_log("Enter the group key", "warning")
            return
        try:
            await onesignal.notifications.remove_grouped_notifications(group_key)
            state.add_log(f"Group {group_key} removed", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_prevent_default(e):
        if not foreground_id:
            state.add_log("Enter the notification ID", "warning")
            return
        try:
            await onesignal.notifications.prevent_default(foreground_id)
            state.add_log(f"Notification {foreground_id} suppressed", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_display(e):
        if not foreground_id:
            state.add_log("Enter the notification ID", "warning")
            return
        try:
            await onesignal.notifications.display(foreground_id)
            state.add_log(f"Notification {foreground_id} displayed", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return PageLayout(
        title="Notifications",
        description=(
            "Manage permissions and notifications. System permission is required "
            "to display notifications. You can also manage displayed notifications, "
            "removing them individually or in groups (Android). "
            "Provisional authorization (iOS) allows sending silent notifications."
        ),
        code_example="""# Request permission
granted = await onesignal.notifications.request_permission()

# Check if can request
can_request = await onesignal.notifications.can_request_permission()

# Get current status
has_permission = await onesignal.notifications.get_permission()

# Provisional authorization (iOS)
await onesignal.notifications.register_for_provisional_authorization()

# Clear all notifications
await onesignal.notifications.clear_all()

# Remove specific notification (Android)
await onesignal.notifications.remove_notification(123)

# Remove notification group (Android)
await onesignal.notifications.remove_grouped_notifications("promo")

# Foreground display control (use in on_notification_foreground handler)
await onesignal.notifications.prevent_default(notification_id)  # Suppress
await onesignal.notifications.display(notification_id)  # Display""",
        children=[
            ft.Text("Permission", weight=ft.FontWeight.W_500, size=16),
            ft.Row(
                [
                    ft.TextField(
                        label="Status",
                        value=permission_status,
                        read_only=True,
                        width=150,
                    ),
                    ft.TextField(
                        label="Can Request",
                        value=can_request,
                        read_only=True,
                        width=150,
                    ),
                ],
                spacing=10,
            ),
            ft.Row(
                [
                    ft.FilledButton(
                        "Request Permission",
                        icon=ft.Icons.NOTIFICATIONS,
                        on_click=handle_request_permission,
                    ),
                    ft.OutlinedButton("Check Status", on_click=handle_get_permission),
                    ft.OutlinedButton("Can Request?", on_click=handle_can_request),
                ],
                spacing=10,
                wrap=True,
            ),
            ft.OutlinedButton(
                "Provisional Authorization (iOS)",
                icon=ft.Icons.NOTIFICATIONS_PAUSED,
                on_click=handle_provisional_auth,
            ),
            ft.Divider(height=20),
            ft.Text("Management", weight=ft.FontWeight.W_500, size=16),
            ft.FilledButton(
                "Clear All",
                icon=ft.Icons.CLEAR_ALL,
                on_click=handle_clear_all,
            ),
            ft.Divider(height=10),
            ft.Text("Remove Notification (Android)", size=14),
            ft.Row(
                [
                    ft.TextField(
                        label="Notification ID",
                        hint_text="Ex: 123",
                        value=notification_id,
                        on_change=lambda e: set_notification_id(e.control.value),
                        width=150,
                        keyboard_type=ft.KeyboardType.NUMBER,
                    ),
                    ft.OutlinedButton("Remove", on_click=handle_remove_notification),
                ],
                spacing=10,
            ),
            ft.Text("Remove Group (Android)", size=14),
            ft.Row(
                [
                    ft.TextField(
                        label="Group Key",
                        hint_text="Ex: promo",
                        value=group_key,
                        on_change=lambda e: set_group_key(e.control.value),
                        width=150,
                    ),
                    ft.OutlinedButton("Remove Group", on_click=handle_remove_grouped),
                ],
                spacing=10,
            ),
            ft.Divider(height=20),
            ft.Text("Foreground Control", weight=ft.FontWeight.W_500, size=16),
            ft.Text(
                "Use with the ID received in on_notification_foreground event",
                size=12,
                color=ft.Colors.GREY_600,
            ),
            ft.Row(
                [
                    ft.TextField(
                        label="Notification ID",
                        hint_text="Foreground event ID",
                        value=foreground_id,
                        on_change=lambda e: set_foreground_id(e.control.value),
                        width=200,
                    ),
                    ft.OutlinedButton("Suppress", on_click=handle_prevent_default),
                    ft.OutlinedButton("Display", on_click=handle_display),
                ],
                spacing=10,
                wrap=True,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
    )
