"""Consent (GDPR) page."""

import flet as ft
from components.log_viewer import LogViewer
from context import AppCtx


@ft.component
def ConsentPage():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    async def handle_give_consent(e):
        try:
            await onesignal.consent_given(True)
            state.add_log("Consent granted", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_revoke_consent(e):
        try:
            await onesignal.consent_given(False)
            state.add_log("Consent revoked", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return ft.Column(
        [
            ft.Text("Consent (GDPR)", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Manage user consent for data collection.",
                size=14,
                color=ft.Colors.GREY_700,
            ),
            ft.TextButton(
                "Documentation: Privacy & Data Handling",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://documentation.onesignal.com/docs/handling-personal-data",
            ),
            ft.Divider(height=20),
            ft.Row(
                [
                    ft.FilledButton(
                        "Give Consent", icon=ft.Icons.CHECK_CIRCLE, on_click=handle_give_consent
                    ),
                    ft.OutlinedButton(
                        "Revoke", icon=ft.Icons.CANCEL, on_click=handle_revoke_consent
                    ),
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
