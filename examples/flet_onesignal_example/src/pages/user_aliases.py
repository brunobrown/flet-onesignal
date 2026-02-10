"""User Aliases page."""

import flet as ft
from components.log_viewer import LogViewer
from context import AppCtx


@ft.component
def UserAliasesPage():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    alias_label, set_alias_label = ft.use_state("")
    alias_id, set_alias_id = ft.use_state("")

    async def handle_add_alias(e):
        if not alias_label or not alias_id:
            state.add_log("Enter label and ID", "warning")
            return
        try:
            await onesignal.user.add_alias(alias_label, alias_id)
            state.add_log(f"Alias added: {alias_label}={alias_id}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_remove_alias(e):
        if not alias_label:
            state.add_log("Enter the label", "warning")
            return
        try:
            await onesignal.user.remove_alias(alias_label)
            state.add_log(f"Alias removed: {alias_label}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return ft.Column(
        [
            ft.Text("User - Aliases", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Aliases are alternative identifiers for the same user.",
                size=14,
                color=ft.Colors.GREY_700,
            ),
            ft.TextButton(
                "Documentation: Aliases",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://documentation.onesignal.com/docs/aliases",
            ),
            ft.Divider(height=20),
            ft.Row(
                [
                    ft.TextField(
                        label="Label",
                        hint_text="Ex: crm_id",
                        width=150,
                        value=alias_label,
                        on_change=lambda e: set_alias_label(e.control.value),
                    ),
                    ft.TextField(
                        label="ID",
                        hint_text="Ex: CRM-123",
                        width=150,
                        value=alias_id,
                        on_change=lambda e: set_alias_id(e.control.value),
                    ),
                ],
                spacing=10,
            ),
            ft.Row(
                [
                    ft.FilledButton("Add", icon=ft.Icons.ADD, on_click=handle_add_alias),
                    ft.OutlinedButton("Remove", icon=ft.Icons.REMOVE, on_click=handle_remove_alias),
                ],
                spacing=10,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
