"""
User Push page - Manage push notification subscription.
"""

import flet as ft
from components.log_viewer import LogViewer
from components.page_layout import PageLayout
from context import AppCtx


@ft.component
def UserPushPage():
    """
    Page for managing push notification subscription.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    # Local state for displaying info
    push_id, set_push_id = ft.use_state("")
    push_token, set_push_token = ft.use_state("")
    opted_in, set_opted_in = ft.use_state("")

    async def handle_opt_in(e):
        try:
            await onesignal.user.opt_in_push()
            state.add_log("Opt-in completed successfully", "success")
        except Exception as ex:
            state.add_log(f"Error on opt-in: {ex}", "error")

    async def handle_opt_out(e):
        try:
            await onesignal.user.opt_out_push()
            state.add_log("Opt-out completed successfully", "success")
        except Exception as ex:
            state.add_log(f"Error on opt-out: {ex}", "error")

    async def handle_check_opted_in(e):
        try:
            result = await onesignal.user.is_push_opted_in()
            set_opted_in("Yes" if result else "No")
            state.add_log(f"Opted in: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error checking opt-in: {ex}", "error")

    async def handle_get_subscription_id(e):
        try:
            result = await onesignal.user.get_push_subscription_id()
            set_push_id(result or "Not available")
            state.add_log(f"Push Subscription ID: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error getting ID: {ex}", "error")

    async def handle_get_token(e):
        try:
            result = await onesignal.user.get_push_subscription_token()
            set_push_token(result or "Not available")
            state.add_log(f"Push Token: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error getting token: {ex}", "error")

    async def handle_get_all(e):
        await handle_check_opted_in(e)
        await handle_get_subscription_id(e)
        await handle_get_token(e)

    return PageLayout(
        title="User - Push Subscription",
        description=(
            "Control user subscription for push notifications. "
            "Opt-in/opt-out is independent of system permission - "
            "even with permission granted, the user can choose not to "
            "receive notifications via opt-out. Use this to give users "
            "more control over their preferences."
        ),
        code_example="""# Opt-in to receive notifications
await onesignal.user.opt_in_push()

# Opt-out to stop receiving
await onesignal.user.opt_out_push()

# Check if opted-in
is_opted = await onesignal.user.is_push_opted_in()

# Get Push Subscription ID
push_id = await onesignal.user.get_push_subscription_id()

# Get Push Token
token = await onesignal.user.get_push_subscription_token()""",
        children=[
            ft.Text("Subscription Control", weight=ft.FontWeight.W_500, size=16),
            ft.Row(
                [
                    ft.FilledButton(
                        "Opt-In",
                        icon=ft.Icons.NOTIFICATIONS_ACTIVE,
                        on_click=handle_opt_in,
                    ),
                    ft.OutlinedButton(
                        "Opt-Out",
                        icon=ft.Icons.NOTIFICATIONS_OFF,
                        on_click=handle_opt_out,
                    ),
                ],
                spacing=10,
            ),
            ft.Divider(height=20),
            ft.Text("Subscription Information", weight=ft.FontWeight.W_500, size=16),
            ft.TextField(
                label="Opted In",
                value=opted_in,
                read_only=True,
                width=150,
            ),
            ft.TextField(
                label="Push Subscription ID",
                value=push_id,
                read_only=True,
            ),
            ft.TextField(
                label="Push Token",
                value=push_token,
                read_only=True,
                multiline=True,
                min_lines=2,
                max_lines=4,
            ),
            ft.Row(
                [
                    ft.FilledButton(
                        "Get All",
                        icon=ft.Icons.REFRESH,
                        on_click=handle_get_all,
                    ),
                    ft.OutlinedButton("Check Opt-In", on_click=handle_check_opted_in),
                    ft.OutlinedButton("Get ID", on_click=handle_get_subscription_id),
                    ft.OutlinedButton("Get Token", on_click=handle_get_token),
                ],
                spacing=10,
                wrap=True,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
    )
