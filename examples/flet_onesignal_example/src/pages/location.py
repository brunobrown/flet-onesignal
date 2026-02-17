"""Location page."""

import flet as ft
from components.log_viewer import LogViewer
from context import AppCtx


@ft.component
def LocationPage():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    async def handle_request_permission(e):
        try:
            result = await onesignal.location.request_permission()
            state.add_log(f"Permission granted: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_check_permission(e):
        try:
            result = await onesignal.location.get_permission()
            state.add_log(f"Permission granted: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_enable(e):
        try:
            await onesignal.location.set_shared(True)
            state.add_log("Sharing enabled", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_disable(e):
        try:
            await onesignal.location.set_shared(False)
            state.add_log("Sharing disabled", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_is_shared(e):
        try:
            result = await onesignal.location.is_shared()
            state.add_log(f"Sharing: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return ft.Column(
        [
            ft.Text("Location", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Control location sharing.", size=14, color=ft.Colors.GREY_700),
            ft.TextButton(
                "Documentation: Location Permissions",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://documentation.onesignal.com/docs/location-opt-in-prompt",
            ),
            ft.Divider(height=20),
            ft.Row(
                [
                    ft.FilledButton(
                        "Request Permission",
                        icon=ft.Icons.LOCATION_SEARCHING,
                        on_click=handle_request_permission,
                    ),
                    ft.OutlinedButton(
                        "Check Permission",
                        icon=ft.Icons.VERIFIED_USER,
                        on_click=handle_check_permission,
                    ),
                ],
                spacing=10,
                wrap=True,
            ),
            ft.Divider(height=10),
            ft.Row(
                [
                    ft.FilledButton("Enable", icon=ft.Icons.LOCATION_ON, on_click=handle_enable),
                    ft.OutlinedButton(
                        "Disable", icon=ft.Icons.LOCATION_OFF, on_click=handle_disable
                    ),
                    ft.OutlinedButton("Check Status", on_click=handle_is_shared),
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
