"""Session Outcomes page."""

import flet as ft
from components.log_viewer import LogViewer
from context import AppCtx


@ft.component
def SessionPage():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    outcome_name, set_outcome_name = ft.use_state("")
    outcome_value, set_outcome_value = ft.use_state("")

    async def handle_add_outcome(e):
        if not outcome_name:
            state.add_log("Enter the name", "warning")
            return
        try:
            await onesignal.session.add_outcome(outcome_name)
            state.add_log(f"Outcome added: {outcome_name}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_add_unique(e):
        if not outcome_name:
            state.add_log("Enter the name", "warning")
            return
        try:
            await onesignal.session.add_unique_outcome(outcome_name)
            state.add_log(f"Unique outcome: {outcome_name}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_add_with_value(e):
        if not outcome_name or not outcome_value:
            state.add_log("Enter name and value", "warning")
            return
        try:
            value = float(outcome_value)
            await onesignal.session.add_outcome_with_value(outcome_name, value)
            state.add_log(f"Outcome with value: {outcome_name}={value}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return ft.Column(
        [
            ft.Text("Session - Outcomes", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Track user conversions and actions.",
                size=14,
                color=ft.Colors.GREY_700,
            ),
            ft.TextButton(
                "Documentation: Outcomes",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://documentation.onesignal.com/docs/outcomes",
            ),
            ft.Divider(height=20),
            ft.TextField(
                label="Outcome Name",
                hint_text="purchase",
                value=outcome_name,
                on_change=lambda e: set_outcome_name(e.control.value),
            ),
            ft.Row(
                [
                    ft.FilledButton("Add", on_click=handle_add_outcome),
                    ft.OutlinedButton("Unique", on_click=handle_add_unique),
                ],
                spacing=10,
            ),
            ft.Divider(height=10),
            ft.Row(
                [
                    ft.TextField(
                        label="Value",
                        hint_text="29.99",
                        width=150,
                        value=outcome_value,
                        on_change=lambda e: set_outcome_value(e.control.value),
                    ),
                    ft.FilledButton("With Value", on_click=handle_add_with_value),
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
