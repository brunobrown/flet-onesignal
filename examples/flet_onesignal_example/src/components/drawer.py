"""Navigation drawer component."""

import flet as ft
from config import NAVIGATION_GROUPS
from context import AppCtx


@ft.component
def AppDrawer():
    ctx = ft.use_context(AppCtx)
    state = ctx.state

    def create_nav_handler(page_id):
        def handler(e):
            state.navigate(page_id)

        return handler

    items = []
    for group in NAVIGATION_GROUPS:
        items.append(
            ft.Container(
                content=ft.Text(
                    group["title"],
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_600,
                ),
                padding=ft.Padding.only(left=16, top=16, bottom=4),
            )
        )
        for item in group["items"]:
            is_selected = state.current_page == item["id"]
            items.append(
                ft.ListTile(
                    leading=ft.Icon(
                        item["icon"],
                        color=ft.Colors.BLUE_700 if is_selected else ft.Colors.GREY_700,
                    ),
                    title=ft.Text(
                        item["label"],
                        weight=ft.FontWeight.W_500 if is_selected else ft.FontWeight.NORMAL,
                        color=ft.Colors.BLUE_700 if is_selected else None,
                    ),
                    selected=is_selected,
                    on_click=create_nav_handler(item["id"]),
                )
            )

    items.append(ft.Divider())
    items.append(
        ft.Container(
            content=ft.TextButton(
                "github.com/brunobrown/flet-onesignal",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://github.com/brunobrown/flet-onesignal",
            ),
            padding=16,
        )
    )

    return ft.Column(controls=items, scroll=ft.ScrollMode.AUTO, spacing=0)
