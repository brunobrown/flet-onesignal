"""
Consent page - Manage GDPR/privacy consent.
"""

import flet as ft
from components.log_viewer import LogViewer
from components.page_layout import PageLayout
from context import AppCtx


@ft.component
def ConsentPage():
    """
    Page for managing user consent.

    Required when using require_consent=True in OneSignal initialization.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    async def handle_give_consent(e):
        try:
            await onesignal.consent_given(True)
            state.add_log("Consent granted", "success")
        except Exception as ex:
            state.add_log(f"Error granting consent: {ex}", "error")

    async def handle_revoke_consent(e):
        try:
            await onesignal.consent_given(False)
            state.add_log("Consent revoked", "success")
        except Exception as ex:
            state.add_log(f"Error revoking consent: {ex}", "error")

    return PageLayout(
        title="Consent (GDPR)",
        description=(
            "Manages user consent for data collection. "
            "When require_consent=True is used in OneSignal initialization, "
            "the SDK will not collect data until consent is given. "
            "Use this for GDPR and other privacy regulation compliance."
        ),
        code_example="""# Initialize with consent required
onesignal = fos.OneSignal(
    app_id="your-app-id",
    require_consent=True,
)

# After user accepts terms:
await onesignal.consent_given(True)

# If user revokes consent:
await onesignal.consent_given(False)""",
        children=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.PRIVACY_TIP, size=48, color=ft.Colors.PRIMARY),
                        ft.Text(
                            "Consent controls whether OneSignal can collect user data.",
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ]
                ),
                alignment=ft.alignment.center,
                padding=20,
            ),
            ft.Row(
                [
                    ft.FilledButton(
                        "Give Consent",
                        icon=ft.Icons.CHECK_CIRCLE,
                        on_click=handle_give_consent,
                    ),
                    ft.OutlinedButton(
                        "Revoke Consent",
                        icon=ft.Icons.CANCEL,
                        on_click=handle_revoke_consent,
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
    )
