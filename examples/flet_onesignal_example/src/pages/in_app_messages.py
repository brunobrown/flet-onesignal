"""In-App Messages page."""

import flet as ft
from components.log_viewer import LogViewer
from context import AppCtx


@ft.component
def InAppMessagesPage():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    trigger_key, set_trigger_key = ft.use_state("")
    trigger_value, set_trigger_value = ft.use_state("")

    async def handle_add_trigger(e):
        if not trigger_key or not trigger_value:
            state.add_log("Enter key and value", "warning")
            return
        try:
            await onesignal.in_app_messages.add_trigger(trigger_key, trigger_value)
            state.add_log(f"Trigger added: {trigger_key}={trigger_value}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_remove_trigger(e):
        if not trigger_key:
            state.add_log("Enter the key", "warning")
            return
        try:
            await onesignal.in_app_messages.remove_trigger(trigger_key)
            state.add_log(f"Trigger removed: {trigger_key}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_clear_triggers(e):
        try:
            await onesignal.in_app_messages.clear_triggers()
            state.add_log("Triggers cleared", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_pause(e):
        try:
            await onesignal.in_app_messages.pause()
            state.add_log("IAM paused", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_resume(e):
        try:
            await onesignal.in_app_messages.resume()
            state.add_log("IAM resumed", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_is_paused(e):
        try:
            result = await onesignal.in_app_messages.is_paused()
            state.add_log(f"Paused: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return ft.Column(
        [
            ft.Text("In-App Messages", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Control triggers and in-app message display.",
                size=14,
                color=ft.Colors.GREY_700,
            ),
            ft.TextButton(
                "Documentation: In-App Messages & Triggers",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://documentation.onesignal.com/docs/iam-triggers",
            ),
            ft.Divider(height=20),
            ft.Text("Triggers", weight=ft.FontWeight.W_500),
            ft.Row(
                [
                    ft.TextField(
                        label="Key",
                        hint_text="show_promo",
                        width=150,
                        value=trigger_key,
                        on_change=lambda e: set_trigger_key(e.control.value),
                    ),
                    ft.TextField(
                        label="Value",
                        hint_text="true",
                        width=150,
                        value=trigger_value,
                        on_change=lambda e: set_trigger_value(e.control.value),
                    ),
                ],
                spacing=10,
            ),
            ft.Row(
                [
                    ft.FilledButton("Add", icon=ft.Icons.ADD, on_click=handle_add_trigger),
                    ft.OutlinedButton(
                        "Remove", icon=ft.Icons.REMOVE, on_click=handle_remove_trigger
                    ),
                    ft.OutlinedButton("Clear All", on_click=handle_clear_triggers),
                ],
                spacing=10,
                wrap=True,
            ),
            ft.Divider(height=10),
            ft.Text("Control", weight=ft.FontWeight.W_500),
            ft.Row(
                [
                    ft.FilledButton("Pause", icon=ft.Icons.PAUSE, on_click=handle_pause),
                    ft.FilledButton("Resume", icon=ft.Icons.PLAY_ARROW, on_click=handle_resume),
                    ft.OutlinedButton("Check Status", on_click=handle_is_paused),
                ],
                spacing=10,
                wrap=True,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
