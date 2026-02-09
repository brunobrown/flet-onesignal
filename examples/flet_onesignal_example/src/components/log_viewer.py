"""Log viewer component."""

import flet as ft
from config import LOG_COLORS
from context import AppCtx


@ft.component
def LogViewer():
    ctx = ft.use_context(AppCtx)
    state = ctx.state

    async def copy_logs(e):
        logs_text = "\n".join(
            f"[{log.time}] [{log.level.upper()}] {log.message}" for log in state.logs
        )
        if logs_text:
            await ctx.clipboard.set(logs_text)
            state.add_log("Logs copied", "success")

    def clear_logs(e):
        state.clear_logs()

    log_entries = [
        ft.Text(
            f"[{log.time}] {log.message}",
            size=12,
            color=LOG_COLORS.get(log.level, ft.Colors.GREY_800),
            selectable=True,
        )
        for log in state.logs
    ]

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Result", weight=ft.FontWeight.W_600),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.COPY,
                                tooltip="Copy",
                                on_click=copy_logs,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                tooltip="Clear",
                                on_click=clear_logs,
                            ),
                        ],
                        spacing=0,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            controls=log_entries
                            if log_entries
                            else [
                                ft.Text(
                                    "No logs yet.",
                                    size=12,
                                    italic=True,
                                    color=ft.Colors.GREY_500,
                                )
                            ],
                            scroll=ft.ScrollMode.AUTO,
                            auto_scroll=True,
                            spacing=4,
                        ),
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                        padding=12,
                        height=200,
                        bgcolor=ft.Colors.GREY_50,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        expand=True,
                    ),
                ],
                expand=True,
            ),
        ],
    )
