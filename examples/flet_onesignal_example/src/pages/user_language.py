"""
User Language page - Set user language preference.
"""

import flet as ft
from components.log_viewer import LogViewer
from components.page_layout import PageLayout
from context import AppCtx

# Common language codes
LANGUAGES = [
    ("en", "English"),
    ("pt", "Portuguese"),
    ("es", "Spanish"),
    ("fr", "French"),
    ("de", "German"),
    ("it", "Italian"),
    ("ja", "Japanese"),
    ("ko", "Korean"),
    ("zh", "Chinese"),
    ("ru", "Russian"),
]


@ft.component
def UserLanguagePage():
    """
    Page for setting user language preference.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    # Local state
    language_code, set_language_code = ft.use_state("en")

    async def handle_set_language(e):
        try:
            await onesignal.user.set_language(language_code)
            state.add_log(f"Language set: {language_code}", "success")
        except Exception as ex:
            state.add_log(f"Error setting language: {ex}", "error")

    def on_language_change(e):
        set_language_code(e.control.value)

    return PageLayout(
        title="User - Language",
        description=(
            "Sets the user's preferred language for receiving localized "
            "notifications and in-app messages. OneSignal uses the language code "
            "to select the correct version of messages when you configure "
            "multi-language notifications in the dashboard."
        ),
        code_example="""# Set user language
await onesignal.user.set_language("en")  # English
await onesignal.user.set_language("pt")  # Portuguese
await onesignal.user.set_language("es")  # Spanish""",
        children=[
            ft.Dropdown(
                label="Language",
                value=language_code,
                on_select=on_language_change,
                options=[
                    ft.dropdown.Option(key=code, text=f"{name} ({code})")
                    for code, name in LANGUAGES
                ],
                width=300,
            ),
            ft.TextField(
                label="Or enter ISO 639-1 code",
                hint_text="E.g.: en, pt, es",
                value=language_code,
                on_change=lambda e: set_language_code(e.control.value),
                width=200,
            ),
            ft.FilledButton(
                "Set Language",
                icon=ft.Icons.LANGUAGE,
                on_click=handle_set_language,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
    )
