"""
User Identity page - Get OneSignal ID and External ID.
"""

import flet as ft
from components.log_viewer import LogViewer
from components.page_layout import PageLayout
from context import AppCtx


@ft.component
def UserIdentityPage():
    """
    Page for viewing user identity information.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    # Local state for displaying IDs
    onesignal_id, set_onesignal_id = ft.use_state("")
    external_id, set_external_id = ft.use_state("")

    async def handle_get_onesignal_id(e):
        try:
            result = await onesignal.user.get_onesignal_id()
            set_onesignal_id(result or "Not available")
            state.add_log(f"OneSignal ID: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error getting OneSignal ID: {ex}", "error")

    async def handle_get_external_id(e):
        try:
            result = await onesignal.user.get_external_id()
            set_external_id(result or "Not set")
            state.add_log(f"External ID: {result}", "success")
        except Exception as ex:
            state.add_log(f"Error getting External ID: {ex}", "error")

    async def handle_get_both(e):
        await handle_get_onesignal_id(e)
        await handle_get_external_id(e)

    return PageLayout(
        title="User - Identity",
        description=(
            "OneSignal ID is a unique identifier automatically generated for "
            "each user. External ID is the identifier you set when logging in. "
            "Use these IDs to identify users in your integrations and dashboards."
        ),
        code_example="""# Get OneSignal ID (automatically generated)
onesignal_id = await onesignal.user.get_onesignal_id()

# Get External ID (set via login)
external_id = await onesignal.user.get_external_id()""",
        children=[
            ft.TextField(
                label="OneSignal ID",
                value=onesignal_id,
                read_only=True,
                expand=True,
            ),
            ft.TextField(
                label="External ID",
                value=external_id,
                read_only=True,
                expand=True,
            ),
            ft.Row(
                [
                    ft.FilledButton(
                        "Get Both",
                        icon=ft.Icons.REFRESH,
                        on_click=handle_get_both,
                    ),
                    ft.OutlinedButton(
                        "OneSignal ID",
                        on_click=handle_get_onesignal_id,
                    ),
                    ft.OutlinedButton(
                        "External ID",
                        on_click=handle_get_external_id,
                    ),
                ],
                spacing=10,
                wrap=True,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
    )
