"""
Debug page - Configure SDK logging levels.
"""

import flet as ft
from components.log_viewer import LogViewer
from components.page_layout import PageLayout
from context import AppCtx

import flet_onesignal as fos

# Log level options
LOG_LEVELS = [
    ("none", "None - No logs"),
    ("fatal", "Fatal - Fatal errors only"),
    ("error", "Error - Errors"),
    ("warn", "Warn - Warnings"),
    ("info", "Info - General information"),
    ("debug", "Debug - Debug details"),
    ("verbose", "Verbose - All details"),
]


@ft.component
def DebugPage():
    """
    Page for configuring OneSignal SDK debug settings.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    # Local state
    log_level, set_log_level = ft.use_state("debug")
    alert_level, set_alert_level = ft.use_state("none")

    def get_log_level_enum(level_str: str) -> fos.OSLogLevel:
        """Convert string to OSLogLevel enum."""
        level_map = {
            "none": fos.OSLogLevel.NONE,
            "fatal": fos.OSLogLevel.FATAL,
            "error": fos.OSLogLevel.ERROR,
            "warn": fos.OSLogLevel.WARN,
            "info": fos.OSLogLevel.INFO,
            "debug": fos.OSLogLevel.DEBUG,
            "verbose": fos.OSLogLevel.VERBOSE,
        }
        return level_map.get(level_str, fos.OSLogLevel.DEBUG)

    async def handle_set_log_level(e):
        try:
            level = get_log_level_enum(log_level)
            await onesignal.debug.set_log_level(level)
            state.add_log(f"Log level set: {log_level}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_set_alert_level(e):
        try:
            level = get_log_level_enum(alert_level)
            await onesignal.debug.set_alert_level(level)
            state.add_log(f"Alert level set: {alert_level}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return PageLayout(
        title="Debug",
        description=(
            "Configure the OneSignal SDK log level. Log Level controls "
            "what appears in console/logcat. Alert Level controls which logs "
            "trigger visual alerts (iOS toast notifications) - use carefully "
            "as it can generate many popups."
        ),
        code_example="""import flet_onesignal as fos

# Set log level (console/logcat)
await onesignal.debug.set_log_level(fos.OSLogLevel.DEBUG)

# Set visual alert level (iOS)
await onesignal.debug.set_alert_level(fos.OSLogLevel.WARN)

# Available levels:
# OSLogLevel.NONE - No logs
# OSLogLevel.FATAL - Fatal only
# OSLogLevel.ERROR - Errors
# OSLogLevel.WARN - Warnings
# OSLogLevel.INFO - Information
# OSLogLevel.DEBUG - Debug
# OSLogLevel.VERBOSE - Everything""",
        children=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.BUG_REPORT, size=48, color=ft.Colors.PRIMARY),
                        ft.Text(
                            "Configure log levels for SDK debugging.",
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ]
                ),
                alignment=ft.alignment.center,
                padding=20,
            ),
            ft.Text("Log Level (Console/Logcat)", weight=ft.FontWeight.W_500, size=16),
            ft.Dropdown(
                label="Log Level",
                value=log_level,
                on_select=lambda e: set_log_level(e.control.value),
                options=[ft.dropdown.Option(key=level, text=desc) for level, desc in LOG_LEVELS],
                width=300,
            ),
            ft.FilledButton(
                "Apply Log Level",
                icon=ft.Icons.CHECK,
                on_click=handle_set_log_level,
            ),
            ft.Divider(height=20),
            ft.Text("Alert Level (iOS Visual)", weight=ft.FontWeight.W_500, size=16),
            ft.Container(
                content=ft.Text(
                    "Warning: Alert Level can generate many popups on screen!",
                    color=ft.Colors.ORANGE_700,
                    size=12,
                ),
                padding=ft.padding.only(bottom=10),
            ),
            ft.Dropdown(
                label="Alert Level",
                value=alert_level,
                on_select=lambda e: set_alert_level(e.control.value),
                options=[ft.dropdown.Option(key=level, text=desc) for level, desc in LOG_LEVELS],
                width=300,
            ),
            ft.FilledButton(
                "Apply Alert Level",
                icon=ft.Icons.CHECK,
                on_click=handle_set_alert_level,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
    )
