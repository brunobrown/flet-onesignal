"""User Push page."""

import flet as ft
from components.log_viewer import LogViewer
from context import AppCtx


@ft.component
def UserPushPage():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    async def handle_opt_in(e):
        try:
            await onesignal.user.opt_in_push()
            state.add_log("Opt-in successful", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_opt_out(e):
        try:
            await onesignal.user.opt_out_push()
            state.add_log("Opt-out successful", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_is_opted_in(e):
        try:
            result = await onesignal.user.is_push_opted_in()
            state.add_log(f"Opted in: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_get_id(e):
        try:
            result = await onesignal.user.get_push_subscription_id()
            state.add_log(f"Push ID: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_get_token(e):
        try:
            result = await onesignal.user.get_push_subscription_token()
            state.add_log(f"Push Token: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return ft.Column(
        [
            ft.Text("User - Push Subscription", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Control the user's push notification subscription.",
                size=14,
                color=ft.Colors.GREY_700,
            ),
            ft.TextButton(
                "Documentation: Subscriptions",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://documentation.onesignal.com/docs/subscriptions",
            ),
            ft.Divider(height=20),
            ft.Row(
                [
                    ft.FilledButton(
                        "Opt-In", icon=ft.Icons.NOTIFICATIONS_ACTIVE, on_click=handle_opt_in
                    ),
                    ft.OutlinedButton(
                        "Opt-Out", icon=ft.Icons.NOTIFICATIONS_OFF, on_click=handle_opt_out
                    ),
                ],
                spacing=10,
            ),
            ft.Divider(height=10),
            ft.Row(
                [
                    ft.OutlinedButton("Check Opt-In", on_click=handle_is_opted_in),
                    ft.OutlinedButton("Get ID", on_click=handle_get_id),
                    ft.OutlinedButton("Get Token", on_click=handle_get_token),
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
