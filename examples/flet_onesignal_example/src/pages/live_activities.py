"""
Live Activities page - iOS Live Activities management.
"""

import flet as ft
from components.log_viewer import LogViewer
from components.page_layout import PageLayout
from context import AppCtx


@ft.component
def LiveActivitiesPage():
    """
    Page for managing iOS Live Activities.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    # Local state
    activity_id, set_activity_id = ft.use_state("")
    activity_token, set_activity_token = ft.use_state("")
    activity_type, set_activity_type = ft.use_state("")

    async def handle_setup_default(e):
        try:
            await onesignal.live_activities.setup_default()
            state.add_log("Live Activities configured with default options", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_enter(e):
        if not activity_id or not activity_token:
            state.add_log("Enter the activity ID and token", "warning")
            return
        try:
            await onesignal.live_activities.enter(activity_id, activity_token)
            state.add_log(f"Entered Live Activity: {activity_id}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_exit(e):
        if not activity_id:
            state.add_log("Enter the activity ID", "warning")
            return
        try:
            await onesignal.live_activities.exit(activity_id)
            state.add_log(f"Exited Live Activity: {activity_id}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_set_push_to_start(e):
        if not activity_type or not activity_token:
            state.add_log("Enter type and token", "warning")
            return
        try:
            await onesignal.live_activities.set_push_to_start_token(activity_type, activity_token)
            state.add_log(f"Push-to-start token set for: {activity_type}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_remove_push_to_start(e):
        if not activity_type:
            state.add_log("Enter the activity type", "warning")
            return
        try:
            await onesignal.live_activities.remove_push_to_start_token(activity_type)
            state.add_log(f"Push-to-start token removed: {activity_type}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return PageLayout(
        title="Live Activities (iOS)",
        description=(
            "Live Activities are an iOS-exclusive feature that displays real-time "
            "information on the Lock Screen and Dynamic Island. Use them to show "
            "delivery status, sports scores, timers, and other frequently updating "
            "information. Requires iOS 16.1 or later."
        ),
        code_example="""# Configure Live Activities with default options
await onesignal.live_activities.setup_default()

# Enter a Live Activity
await onesignal.live_activities.enter("activity-123", "push-token-abc")

# Exit a Live Activity
await onesignal.live_activities.exit("activity-123")

# Set push-to-start token
await onesignal.live_activities.set_push_to_start_token(
    "DeliveryActivity",
    "push-to-start-token"
)

# Remove push-to-start token
await onesignal.live_activities.remove_push_to_start_token("DeliveryActivity")""",
        children=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.LIVE_TV, size=48, color=ft.Colors.PRIMARY),
                        ft.Text(
                            "iOS 16.1+ exclusive feature. Displays real-time info on the Lock Screen.",
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ]
                ),
                alignment=ft.alignment.center,
                padding=20,
            ),
            ft.FilledButton(
                "Setup Default",
                icon=ft.Icons.SETTINGS,
                on_click=handle_setup_default,
            ),
            ft.Divider(height=20),
            ft.Text("Manage Activity", weight=ft.FontWeight.W_500, size=16),
            ft.TextField(
                label="Activity ID",
                hint_text="E.g.: delivery-123",
                value=activity_id,
                on_change=lambda e: set_activity_id(e.control.value),
            ),
            ft.TextField(
                label="Token",
                hint_text="Activity push token",
                value=activity_token,
                on_change=lambda e: set_activity_token(e.control.value),
            ),
            ft.Row(
                [
                    ft.FilledButton("Enter", icon=ft.Icons.LOGIN, on_click=handle_enter),
                    ft.OutlinedButton("Exit", icon=ft.Icons.LOGOUT, on_click=handle_exit),
                ],
                spacing=10,
            ),
            ft.Divider(height=20),
            ft.Text("Push-to-Start", weight=ft.FontWeight.W_500, size=16),
            ft.TextField(
                label="Activity Type",
                hint_text="E.g.: DeliveryActivity",
                value=activity_type,
                on_change=lambda e: set_activity_type(e.control.value),
            ),
            ft.Row(
                [
                    ft.FilledButton("Set Token", on_click=handle_set_push_to_start),
                    ft.OutlinedButton("Remove Token", on_click=handle_remove_push_to_start),
                ],
                spacing=10,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
    )
