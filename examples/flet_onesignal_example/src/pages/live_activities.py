"""Live Activities page (iOS)."""

import flet as ft
from components.log_viewer import LogViewer
from context import AppCtx


@ft.component
def LiveActivitiesPage():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    activity_id, set_activity_id = ft.use_state("")
    activity_token, set_activity_token = ft.use_state("")

    async def handle_setup(e):
        try:
            await onesignal.live_activities.setup_default()
            state.add_log("Live Activities configured", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_enter(e):
        if not activity_id or not activity_token:
            state.add_log("Enter ID and Token", "warning")
            return
        try:
            await onesignal.live_activities.enter(activity_id, activity_token)
            state.add_log(f"Entered: {activity_id}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_exit(e):
        if not activity_id:
            state.add_log("Enter the ID", "warning")
            return
        try:
            await onesignal.live_activities.exit(activity_id)
            state.add_log(f"Exited: {activity_id}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return ft.Column(
        [
            ft.Text("Live Activities (iOS)", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Manage iOS Live Activities (iOS 16.1+).",
                size=14,
                color=ft.Colors.GREY_700,
            ),
            ft.TextButton(
                "Documentation: Live Activities",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://documentation.onesignal.com/docs/live-activities",
            ),
            ft.Divider(height=20),
            ft.FilledButton("Setup Default", icon=ft.Icons.SETTINGS, on_click=handle_setup),
            ft.Divider(height=10),
            ft.TextField(
                label="Activity ID",
                hint_text="delivery-123",
                value=activity_id,
                on_change=lambda e: set_activity_id(e.control.value),
            ),
            ft.TextField(
                label="Token",
                value=activity_token,
                on_change=lambda e: set_activity_token(e.control.value),
            ),
            ft.Row(
                [
                    ft.FilledButton("Enter", on_click=handle_enter),
                    ft.OutlinedButton("Exit", on_click=handle_exit),
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
