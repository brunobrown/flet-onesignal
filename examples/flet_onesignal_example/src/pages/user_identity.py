"""User Identity page."""

import flet as ft
from components.log_viewer import LogViewer
from context import AppCtx


@ft.component
def UserIdentityPage():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    async def handle_get_onesignal_id(e):
        try:
            result = await onesignal.user.get_onesignal_id()
            state.add_log(f"OneSignal ID: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_get_external_id(e):
        try:
            result = await onesignal.user.get_external_id()
            state.add_log(f"External ID: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return ft.Column(
        [
            ft.Text("User - Identity", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Get the user's IDs.", size=14, color=ft.Colors.GREY_700),
            ft.TextButton(
                "Documentation: Users",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://documentation.onesignal.com/docs/users",
            ),
            ft.Divider(height=20),
            ft.Row(
                [
                    ft.FilledButton("Get OneSignal ID", on_click=handle_get_onesignal_id),
                    ft.FilledButton("Get External ID", on_click=handle_get_external_id),
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
