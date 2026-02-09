"""User Language page."""

import flet as ft
from components.log_viewer import LogViewer
from context import AppCtx


@ft.component
def UserLanguagePage():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    language, set_language = ft.use_state("en")

    async def handle_set_language(e):
        try:
            await onesignal.user.set_language(language)
            state.add_log(f"Language set: {language}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return ft.Column(
        [
            ft.Text("User - Language", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Set the user's preferred language.",
                size=14,
                color=ft.Colors.GREY_700,
            ),
            ft.TextButton(
                "Documentation: Mobile SDK Reference",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://documentation.onesignal.com/docs/mobile-sdk-reference",
            ),
            ft.Divider(height=20),
            ft.Dropdown(
                label="Language",
                value=language,
                on_select=lambda e: set_language(e.control.value),
                options=[
                    ft.DropdownOption("pt", "Portuguese"),
                    ft.DropdownOption("en", "English"),
                    ft.DropdownOption("es", "Spanish"),
                ],
                width=200,
            ),
            ft.FilledButton(
                "Set Language", icon=ft.Icons.LANGUAGE, on_click=handle_set_language
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
