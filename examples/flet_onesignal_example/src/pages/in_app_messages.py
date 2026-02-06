"""
In-App Messages page - Triggers and lifecycle control.
"""

import flet as ft
from components.log_viewer import LogViewer
from components.page_layout import PageLayout
from context import AppCtx


@ft.component
def InAppMessagesPage():
    """
    Page for managing in-app message triggers and display control.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    # Local state
    trigger_key, set_trigger_key = ft.use_state("")
    trigger_value, set_trigger_value = ft.use_state("")
    triggers_json, set_triggers_json = ft.use_state("")
    is_paused, set_is_paused = ft.use_state("")

    async def handle_add_trigger(e):
        if not trigger_key or not trigger_value:
            state.add_log("Enter key and value for the trigger", "warning")
            return
        try:
            await onesignal.in_app_messages.add_trigger(trigger_key, trigger_value)
            state.add_log(f"Trigger added: {trigger_key}={trigger_value}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_add_triggers(e):
        if not triggers_json:
            state.add_log("Enter triggers in JSON format", "warning")
            return
        try:
            import json

            triggers = json.loads(triggers_json)
            await onesignal.in_app_messages.add_triggers(triggers)
            state.add_log(f"Triggers added: {triggers}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_remove_trigger(e):
        if not trigger_key:
            state.add_log("Enter the trigger key", "warning")
            return
        try:
            await onesignal.in_app_messages.remove_trigger(trigger_key)
            state.add_log(f"Trigger removed: {trigger_key}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_remove_triggers(e):
        if not trigger_key:
            state.add_log("Enter keys separated by comma", "warning")
            return
        try:
            keys = [k.strip() for k in trigger_key.split(",")]
            await onesignal.in_app_messages.remove_triggers(keys)
            state.add_log(f"Triggers removed: {keys}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_clear_triggers(e):
        try:
            await onesignal.in_app_messages.clear_triggers()
            state.add_log("All triggers cleared", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_pause(e):
        try:
            await onesignal.in_app_messages.pause()
            state.add_log("In-App Messages paused", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_resume(e):
        try:
            await onesignal.in_app_messages.resume()
            state.add_log("In-App Messages resumed", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_check_paused(e):
        try:
            result = await onesignal.in_app_messages.is_paused()
            set_is_paused("Yes" if result else "No")
            state.add_log(f"Paused: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return PageLayout(
        title="In-App Messages",
        description=(
            "Control in-app message display through triggers. "
            "Triggers are conditions that, when met, display a message "
            "configured in the OneSignal dashboard. You can also temporarily "
            "pause message display."
        ),
        code_example="""# Add trigger
await onesignal.in_app_messages.add_trigger("show_promo", "true")

# Add multiple triggers
await onesignal.in_app_messages.add_triggers({
    "show_promo": "true",
    "user_level": "5"
})

# Remove trigger
await onesignal.in_app_messages.remove_trigger("show_promo")

# Clear all triggers
await onesignal.in_app_messages.clear_triggers()

# Pause/Resume messages
await onesignal.in_app_messages.pause()
await onesignal.in_app_messages.resume()

# Check if paused
is_paused = await onesignal.in_app_messages.is_paused()""",
        children=[
            ft.Text("Triggers", weight=ft.FontWeight.W_500, size=16),
            ft.Row(
                [
                    ft.TextField(
                        label="Key",
                        hint_text="E.g.: show_promo",
                        value=trigger_key,
                        on_change=lambda e: set_trigger_key(e.control.value),
                        width=150,
                    ),
                    ft.TextField(
                        label="Value",
                        hint_text="E.g.: true",
                        value=trigger_value,
                        on_change=lambda e: set_trigger_value(e.control.value),
                        width=150,
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
                    ft.OutlinedButton("Remove Multiple", on_click=handle_remove_triggers),
                ],
                spacing=10,
                wrap=True,
            ),
            ft.TextField(
                label="Multiple Triggers (JSON)",
                hint_text='{"key1": "value1", "key2": "value2"}',
                value=triggers_json,
                on_change=lambda e: set_triggers_json(e.control.value),
                multiline=True,
                min_lines=2,
                max_lines=3,
            ),
            ft.Row(
                [
                    ft.FilledButton("Add Multiple", on_click=handle_add_triggers),
                    ft.OutlinedButton(
                        "Clear All", icon=ft.Icons.CLEAR_ALL, on_click=handle_clear_triggers
                    ),
                ],
                spacing=10,
            ),
            ft.Divider(height=20),
            ft.Text("Display Control", weight=ft.FontWeight.W_500, size=16),
            ft.TextField(
                label="Paused",
                value=is_paused,
                read_only=True,
                width=100,
            ),
            ft.Row(
                [
                    ft.FilledButton("Pause", icon=ft.Icons.PAUSE, on_click=handle_pause),
                    ft.FilledButton("Resume", icon=ft.Icons.PLAY_ARROW, on_click=handle_resume),
                    ft.OutlinedButton("Check Status", on_click=handle_check_paused),
                ],
                spacing=10,
                wrap=True,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
    )
