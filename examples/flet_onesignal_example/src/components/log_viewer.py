"""
Log viewer component for displaying event logs.
"""

import flet as ft
from context import AppCtx

LOG_COLORS = {
    "info": ft.Colors.GREY_800,
    "success": ft.Colors.GREEN_700,
    "warning": ft.Colors.ORANGE_700,
    "error": ft.Colors.RED_700,
    "debug": ft.Colors.BLUE_700,
}


@ft.component
def LogViewer(height: int = 200):
    """
    Component for viewing application logs.

    Args:
        height: Height of the log viewer container
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state

    def clear_logs(e):
        state.clear_logs()

    def copy_logs(e):
        logs_text = "\n".join(
            f"[{log['time']}] [{log['level'].upper()}] {log['message']}" for log in state.logs
        )
        if logs_text:
            e.page.set_clipboard(logs_text)
            state.add_log("Logs copied to clipboard", "success")

    # Build log entries
    log_entries = []
    for log in state.logs:
        color = LOG_COLORS.get(log["level"], ft.Colors.GREY_800)
        log_entries.append(
            ft.Text(
                f"[{log['time']}] {log['message']}",
                size=12,
                color=color,
                selectable=True,
            )
        )

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Result", weight=ft.FontWeight.W_600),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.COPY,
                                tooltip="Copy logs",
                                on_click=copy_logs,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                tooltip="Clear logs",
                                on_click=clear_logs,
                            ),
                        ],
                        spacing=0,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Container(
                content=ft.Column(
                    controls=log_entries
                    if log_entries
                    else [
                        ft.Text(
                            "No logs yet. Execute an action to see results.",
                            size=12,
                            italic=True,
                            color=ft.Colors.GREY_500,
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    auto_scroll=True,
                    spacing=4,
                ),
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=8,
                padding=12,
                height=height,
                bgcolor=ft.Colors.GREY_50,
            ),
        ]
    )
