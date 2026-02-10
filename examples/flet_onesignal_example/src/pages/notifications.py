"""Notifications page."""

import flet as ft
from components.log_viewer import LogViewer
from context import AppCtx


@ft.component
def NotificationsPage():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    notification_id, set_notification_id = ft.use_state("")

    async def handle_request_permission(e):
        try:
            result = await onesignal.notifications.request_permission()
            state.add_log(f"Permission: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_get_permission(e):
        try:
            result = await onesignal.notifications.get_permission()
            state.add_log(f"Status: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_can_request(e):
        try:
            result = await onesignal.notifications.can_request_permission()
            state.add_log(f"Can request: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_clear_all(e):
        try:
            await onesignal.notifications.clear_all()
            state.add_log("Notifications cleared", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_remove(e):
        if not notification_id:
            state.add_log("Enter the ID", "warning")
            return
        try:
            await onesignal.notifications.remove_notification(int(notification_id))
            state.add_log(f"Notification removed: {notification_id}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return ft.Column(
        [
            ft.Text("Notifications", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Manage permissions and notifications.",
                size=14,
                color=ft.Colors.GREY_700,
            ),
            ft.TextButton(
                "Documentation: Push Permissions",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://documentation.onesignal.com/docs/prompt-for-push-permissions",
            ),
            ft.Divider(height=20),
            ft.Text("Permission", weight=ft.FontWeight.W_500),
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
            ft.Divider(height=10),
            ft.Text("Management", weight=ft.FontWeight.W_500),
            ft.FilledButton("Clear All", icon=ft.Icons.CLEAR_ALL, on_click=handle_clear_all),
            ft.Row(
                [
                    ft.TextField(
                        label="Notification ID",
                        hint_text="123",
                        width=150,
                        value=notification_id,
                        on_change=lambda e: set_notification_id(e.control.value),
                    ),
                    ft.OutlinedButton("Remove", on_click=handle_remove),
                ],
                spacing=10,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
