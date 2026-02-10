"""User Tags page."""

import flet as ft
from components.log_viewer import LogViewer
from context import AppCtx


@ft.component
def UserTagsPage():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    tag_key, set_tag_key = ft.use_state("")
    tag_value, set_tag_value = ft.use_state("")

    async def handle_add_tag(e):
        if not tag_key or not tag_value:
            state.add_log("Enter key and value", "warning")
            return
        try:
            await onesignal.user.add_tag(tag_key, tag_value)
            state.add_log(f"Tag added: {tag_key}={tag_value}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_remove_tag(e):
        if not tag_key:
            state.add_log("Enter the key", "warning")
            return
        try:
            await onesignal.user.remove_tag(tag_key)
            state.add_log(f"Tag removed: {tag_key}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_get_tags(e):
        try:
            tags = await onesignal.user.get_tags()
            state.add_log(f"Tags: {tags}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return ft.Column(
        [
            ft.Text("User - Tags", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Tags allow you to segment users for targeted notifications.",
                size=14,
                color=ft.Colors.GREY_700,
            ),
            ft.TextButton(
                "Documentation: Data Tags",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://documentation.onesignal.com/docs/add-user-data-tags",
            ),
            ft.Divider(height=20),
            ft.Row(
                [
                    ft.TextField(
                        label="Key",
                        hint_text="Ex: plan",
                        width=150,
                        value=tag_key,
                        on_change=lambda e: set_tag_key(e.control.value),
                    ),
                    ft.TextField(
                        label="Value",
                        hint_text="Ex: premium",
                        width=150,
                        value=tag_value,
                        on_change=lambda e: set_tag_value(e.control.value),
                    ),
                ],
                spacing=10,
            ),
            ft.Row(
                [
                    ft.FilledButton("Add", icon=ft.Icons.ADD, on_click=handle_add_tag),
                    ft.OutlinedButton("Remove", icon=ft.Icons.REMOVE, on_click=handle_remove_tag),
                    ft.OutlinedButton("Get All", icon=ft.Icons.LIST, on_click=handle_get_tags),
                ],
                spacing=10,
                wrap=True,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
