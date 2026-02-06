"""
Location page - Location sharing control.
"""

import flet as ft
from components.log_viewer import LogViewer
from components.page_layout import PageLayout
from context import AppCtx


@ft.component
def LocationPage():
    """
    Page for managing location sharing with OneSignal.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    # Local state
    is_shared, set_is_shared = ft.use_state("")

    async def handle_request_permission(e):
        try:
            result = await onesignal.location.request_permission()
            state.add_log(f"Location permission: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_enable_sharing(e):
        try:
            await onesignal.location.set_shared(True)
            set_is_shared("Yes")
            state.add_log("Location sharing enabled", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_disable_sharing(e):
        try:
            await onesignal.location.set_shared(False)
            set_is_shared("No")
            state.add_log("Location sharing disabled", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_check_shared(e):
        try:
            result = await onesignal.location.is_shared()
            set_is_shared("Yes" if result else "No")
            state.add_log(f"Location shared: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return PageLayout(
        title="Location",
        description=(
            "Control location sharing with OneSignal. "
            "When enabled, OneSignal can use the device location "
            "for geographic notification targeting. System permission "
            "is required before enabling sharing."
        ),
        code_example="""# Request location permission
granted = await onesignal.location.request_permission()

# Enable sharing
await onesignal.location.set_shared(True)

# Disable sharing
await onesignal.location.set_shared(False)

# Check status
is_shared = await onesignal.location.is_shared()""",
        children=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.LOCATION_ON, size=48, color=ft.Colors.PRIMARY),
                        ft.Text(
                            "Location enables sending notifications based on the user's geographic position.",
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ]
                ),
                alignment=ft.alignment.center,
                padding=20,
            ),
            ft.FilledButton(
                "Request Permission",
                icon=ft.Icons.LOCATION_SEARCHING,
                on_click=handle_request_permission,
            ),
            ft.Divider(height=20),
            ft.Text("Sharing", weight=ft.FontWeight.W_500, size=16),
            ft.TextField(
                label="Status",
                value=is_shared,
                read_only=True,
                width=100,
            ),
            ft.Row(
                [
                    ft.FilledButton(
                        "Enable",
                        icon=ft.Icons.LOCATION_ON,
                        on_click=handle_enable_sharing,
                    ),
                    ft.OutlinedButton(
                        "Disable",
                        icon=ft.Icons.LOCATION_OFF,
                        on_click=handle_disable_sharing,
                    ),
                    ft.OutlinedButton(
                        "Check Status",
                        on_click=handle_check_shared,
                    ),
                ],
                spacing=10,
                wrap=True,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
    )
