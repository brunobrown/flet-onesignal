"""Debug page."""

import flet as ft
from components.log_viewer import LogViewer
from context import AppCtx

import flet_onesignal as fos


@ft.component
def DebugPage():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    log_level, set_log_level = ft.use_state("debug")
    alert_level, set_alert_level = ft.use_state("none")

    def get_level(level_str):
        levels = {
            "none": fos.OSLogLevel.NONE,
            "error": fos.OSLogLevel.ERROR,
            "warn": fos.OSLogLevel.WARN,
            "info": fos.OSLogLevel.INFO,
            "debug": fos.OSLogLevel.DEBUG,
            "verbose": fos.OSLogLevel.VERBOSE,
        }
        return levels.get(level_str, fos.OSLogLevel.DEBUG)

    async def handle_set_log_level(e):
        try:
            await onesignal.debug.set_log_level(get_level(log_level))
            state.add_log(f"Log level: {log_level}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_set_alert_level(e):
        try:
            await onesignal.debug.set_alert_level(get_level(alert_level))
            state.add_log(f"Alert level: {alert_level}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return ft.Column(
        [
            ft.Text("Debug", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Configure SDK log levels.", size=14, color=ft.Colors.GREY_700),
            ft.TextButton(
                "Documentation: Mobile SDK Reference",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://documentation.onesignal.com/docs/mobile-sdk-reference",
            ),
            ft.Divider(height=20),
            ft.Dropdown(
                label="Log Level",
                value=log_level,
                on_select=lambda e: set_log_level(e.control.value),
                options=[
                    ft.DropdownOption("none", "None"),
                    ft.DropdownOption("error", "Error"),
                    ft.DropdownOption("warn", "Warn"),
                    ft.DropdownOption("info", "Info"),
                    ft.DropdownOption("debug", "Debug"),
                    ft.DropdownOption("verbose", "Verbose"),
                ],
                width=200,
            ),
            ft.FilledButton("Apply Log Level", on_click=handle_set_log_level),
            ft.Divider(height=10),
            ft.Dropdown(
                label="Alert Level",
                value=alert_level,
                on_select=lambda e: set_alert_level(e.control.value),
                options=[
                    ft.DropdownOption("none", "None"),
                    ft.DropdownOption("error", "Error"),
                    ft.DropdownOption("warn", "Warn"),
                    ft.DropdownOption("info", "Info"),
                ],
                width=200,
            ),
            ft.FilledButton("Apply Alert Level", on_click=handle_set_alert_level),
            ft.Divider(height=20),
            LogViewer(),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
