"""
Login/Logout page - Associate/disassociate user with OneSignal.
"""

import flet as ft
from components.log_viewer import LogViewer
from components.page_layout import PageLayout
from context import AppCtx


@ft.component
def LoginPage():
    """
    Page for login/logout functionality.

    Allows associating a user with an external ID for cross-device tracking.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    # Local state
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

    return PageLayout(
        title="Login / Logout",
        description=(
            "Associates the device with a user identified by External ID. "
            "This allows tracking the user across devices and keeping their "
            "preferences synchronized. Logout disassociates the current user "
            "and creates a new anonymous user."
        ),
        code_example="""# Login - associate user
await onesignal.login("user-123")

# Logout - disassociate user
await onesignal.logout()""",
        children=[
            ft.TextField(
                label="External ID",
                hint_text="E.g.: user-123, email@example.com",
                value=external_id,
                on_change=lambda e: set_external_id(e.control.value),
                expand=True,
            ),
            ft.Row(
                [
                    ft.FilledButton(
                        "Login",
                        icon=ft.Icons.LOGIN,
                        on_click=handle_login,
                    ),
                    ft.OutlinedButton(
                        "Logout",
                        icon=ft.Icons.LOGOUT,
                        on_click=handle_logout,
                    ),
                ],
                spacing=10,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
    )
