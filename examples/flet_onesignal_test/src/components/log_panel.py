"""Log panel component with colored output, auto-scroll, and copy button."""

import flet as ft
from context import AppCtx

LOG_COLORS = {
    "info": ft.Colors.GREY_800,
    "pass": ft.Colors.GREEN_700,
    "fail": ft.Colors.RED_700,
    "warn": ft.Colors.ORANGE_700,
    "skip": ft.Colors.ORANGE_600,
    "debug": ft.Colors.BLUE_700,
}


@ft.component
def LogPanel():
    ctx = ft.use_context(AppCtx)
    state = ctx.state

    async def on_copy(e):
        text = "\n".join(f"[{log.time}] {log.message}" for log in state.logs)
        await ctx.clipboard.set(text)

    log_controls = []
    for log in state.logs:
        color = LOG_COLORS.get(log.level, ft.Colors.GREY_800)
        log_controls.append(
            ft.Text(
                f"[{log.time}] {log.message}",
                size=11,
                color=color,
                font_family="monospace",
            )
        )

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "Logs",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_600,
                        ),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CONTENT_COPY,
                            icon_size=16,
                            tooltip="Copy logs",
                            on_click=on_copy,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.ListView(
                    controls=log_controls,
                    spacing=1,
                    padding=ft.Padding.only(left=8, right=8, bottom=8),
                    auto_scroll=True,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        ),
        expand=1,
        border=ft.Border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        bgcolor=ft.Colors.GREY_50,
        padding=ft.Padding.only(left=4, right=4, top=2),
    )
