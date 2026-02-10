"""Event Logs page."""

import flet as ft
from config import LOG_COLORS
from context import AppCtx


@ft.component
def EventLogsPage():
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
        ft.Container(
            content=ft.Row(
                [
                    ft.Text(f"[{log.time}]", size=11, color=ft.Colors.GREY_600),
                    ft.Text(
                        log.message,
                        size=12,
                        color=LOG_COLORS.get(log.level, ft.Colors.GREY_800),
                        selectable=True,
                        expand=True,
                    ),
                ],
                spacing=8,
            ),
            padding=ft.Padding.symmetric(vertical=4),
        )
        for log in state.logs
    ]

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Event Logs", size=24, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            ft.IconButton(icon=ft.Icons.COPY, tooltip="Copy", on_click=copy_logs),
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
                    ft.Text(
                        "View all OneSignal events in real-time.",
                        size=14,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.TextButton(
                        "SDK Reference",
                        icon=ft.Icons.OPEN_IN_NEW,
                        url="https://documentation.onesignal.com/docs/mobile-sdk-reference",
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(height=20),
            ft.Container(
                content=ft.Column(
                    controls=log_entries
                    if log_entries
                    else [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Icon(ft.Icons.INBOX, size=48, color=ft.Colors.GREY_400),
                                    ft.Text("No events yet.", color=ft.Colors.GREY_500),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            alignment=ft.Alignment.CENTER,
                            padding=40,
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    auto_scroll=True,
                ),
                border=ft.Border.all(1, ft.Colors.GREY_300),
                border_radius=8,
                bgcolor=ft.Colors.GREY_50,
                expand=True,
                padding=12,
            ),
            ft.Text(f"Total: {len(state.logs)} events", size=12, color=ft.Colors.GREY_600),
        ],
        spacing=12,
        expand=True,
    )
