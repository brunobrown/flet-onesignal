"""Login/Logout page."""

import flet as ft
from components.log_viewer import LogViewer
from context import AppCtx


@ft.component
def LoginPage():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    external_id, set_external_id = ft.use_state("")

    async def handle_login(e):
        if not external_id:
            state.add_log("Please enter an External ID", "warning")
            return
        try:
            await onesignal.login(external_id)
            state.add_log(f"Login successful: {external_id}", "success")
        except Exception as ex:
            state.add_log(f"Login error: {ex}", "error")

    async def handle_logout(e):
        try:
            await onesignal.logout()
            set_external_id("")
            state.add_log("Logout successful", "success")
        except Exception as ex:
            state.add_log(f"Logout error: {ex}", "error")

    return ft.Column(
        [
            ft.Text("Login / Logout", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Associate the device with a user identified by External ID.",
                size=14,
                color=ft.Colors.GREY_700,
            ),
            ft.TextButton(
                "Documentation: Users",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://documentation.onesignal.com/docs/users",
            ),
            ft.Divider(height=20),
            ft.TextField(
                label="External ID",
                hint_text="Ex: user-123",
                value=external_id,
                on_change=lambda e: set_external_id(e.control.value),
            ),
            ft.Row(
                [
                    ft.FilledButton("Login", icon=ft.Icons.LOGIN, on_click=handle_login),
                    ft.OutlinedButton("Logout", icon=ft.Icons.LOGOUT, on_click=handle_logout),
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
