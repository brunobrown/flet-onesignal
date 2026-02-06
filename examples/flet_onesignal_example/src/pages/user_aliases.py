"""
User Aliases page - Manage alternative identifiers.
"""

import flet as ft
from components.log_viewer import LogViewer
from components.page_layout import PageLayout
from context import AppCtx


@ft.component
def UserAliasesPage():
    """
    Page for managing user aliases.

    Aliases are alternative identifiers for the same user.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    # Local state
    alias_label, set_alias_label = ft.use_state("")
    alias_id, set_alias_id = ft.use_state("")
    aliases_json, set_aliases_json = ft.use_state("")

    async def handle_add_alias(e):
        if not alias_label or not alias_id:
            state.add_log("Enter label and ID for the alias", "warning")
            return
        try:
            await onesignal.user.add_alias(alias_label, alias_id)
            state.add_log(f"Alias added: {alias_label}={alias_id}", "success")
        except Exception as ex:
            state.add_log(f"Error adding alias: {ex}", "error")

    async def handle_add_aliases(e):
        if not aliases_json:
            state.add_log("Enter aliases in JSON format", "warning")
            return
        try:
            import json

            aliases = json.loads(aliases_json)
            await onesignal.user.add_aliases(aliases)
            state.add_log(f"Aliases added: {aliases}", "success")
        except Exception as ex:
            state.add_log(f"Error adding aliases: {ex}", "error")

    async def handle_remove_alias(e):
        if not alias_label:
            state.add_log("Enter the alias label to remove", "warning")
            return
        try:
            await onesignal.user.remove_alias(alias_label)
            state.add_log(f"Alias removed: {alias_label}", "success")
        except Exception as ex:
            state.add_log(f"Error removing alias: {ex}", "error")

    async def handle_remove_aliases(e):
        if not alias_label:
            state.add_log("Enter labels separated by comma", "warning")
            return
        try:
            labels = [label.strip() for label in alias_label.split(",")]
            await onesignal.user.remove_aliases(labels)
            state.add_log(f"Aliases removed: {labels}", "success")
        except Exception as ex:
            state.add_log(f"Error removing aliases: {ex}", "error")

    return PageLayout(
        title="User - Aliases",
        description=(
            "Aliases are alternative identifiers for the same user. "
            "Use aliases when you need to identify users by different "
            "systems or platforms. For example, a user may have an ID in "
            "your system, another in CRM, and another in the payment system."
        ),
        code_example="""# Add an alias
await onesignal.user.add_alias("crm_id", "CRM-12345")

# Add multiple aliases
await onesignal.user.add_aliases({
    "crm_id": "CRM-12345",
    "payment_id": "PAY-67890"
})

# Remove an alias
await onesignal.user.remove_alias("crm_id")

# Remove multiple aliases
await onesignal.user.remove_aliases(["crm_id", "payment_id"])""",
        children=[
            ft.Text("Single Alias", weight=ft.FontWeight.W_500),
            ft.Row(
                [
                    ft.TextField(
                        label="Label",
                        hint_text="E.g.: crm_id",
                        value=alias_label,
                        on_change=lambda e: set_alias_label(e.control.value),
                        width=150,
                    ),
                    ft.TextField(
                        label="ID",
                        hint_text="E.g.: CRM-12345",
                        value=alias_id,
                        on_change=lambda e: set_alias_id(e.control.value),
                        width=150,
                    ),
                ],
                spacing=10,
            ),
            ft.Row(
                [
                    ft.FilledButton("Add", icon=ft.Icons.ADD, on_click=handle_add_alias),
                    ft.OutlinedButton("Remove", icon=ft.Icons.REMOVE, on_click=handle_remove_alias),
                    ft.OutlinedButton("Remove Multiple", on_click=handle_remove_aliases),
                ],
                spacing=10,
                wrap=True,
            ),
            ft.Divider(height=10),
            ft.Text("Multiple Aliases (JSON)", weight=ft.FontWeight.W_500),
            ft.TextField(
                label="Aliases JSON",
                hint_text='{"label1": "id1", "label2": "id2"}',
                value=aliases_json,
                on_change=lambda e: set_aliases_json(e.control.value),
                multiline=True,
                min_lines=2,
                max_lines=4,
            ),
            ft.FilledButton("Add Aliases", on_click=handle_add_aliases),
            ft.Divider(height=20),
            LogViewer(),
        ],
    )
