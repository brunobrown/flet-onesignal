"""
Session page - Track outcomes and conversions.
"""

import flet as ft
from components.log_viewer import LogViewer
from components.page_layout import PageLayout
from context import AppCtx


@ft.component
def SessionPage():
    """
    Page for tracking session outcomes.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    # Local state
    outcome_name, set_outcome_name = ft.use_state("")
    outcome_value, set_outcome_value = ft.use_state("")

    async def handle_add_outcome(e):
        if not outcome_name:
            state.add_log("Enter the outcome name", "warning")
            return
        try:
            await onesignal.session.add_outcome(outcome_name)
            state.add_log(f"Outcome added: {outcome_name}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_add_unique_outcome(e):
        if not outcome_name:
            state.add_log("Enter the outcome name", "warning")
            return
        try:
            await onesignal.session.add_unique_outcome(outcome_name)
            state.add_log(f"Unique outcome added: {outcome_name}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_add_outcome_with_value(e):
        if not outcome_name or not outcome_value:
            state.add_log("Enter name and value for the outcome", "warning")
            return
        try:
            value = float(outcome_value)
            await onesignal.session.add_outcome_with_value(outcome_name, value)
            state.add_log(f"Outcome with value added: {outcome_name}={value}", "success")
        except ValueError:
            state.add_log("Value must be a number", "warning")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return PageLayout(
        title="Session - Outcomes",
        description=(
            "Track conversions and important user actions. Outcomes allow "
            "measuring the effectiveness of your notifications and in-app messages. "
            "Use simple outcomes for counting, unique for one-time events per notification, "
            "and with value to track monetary values or quantities."
        ),
        code_example="""# Record a simple outcome (can count multiple times)
await onesignal.session.add_outcome("purchase")

# Record a unique outcome (counts only once per notification)
await onesignal.session.add_unique_outcome("app_opened")

# Record outcome with value (for monetary values)
await onesignal.session.add_outcome_with_value("revenue", 29.99)""",
        children=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ANALYTICS, size=48, color=ft.Colors.PRIMARY),
                        ft.Text(
                            "Outcomes help measure the impact of your notifications on user actions.",
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ]
                ),
                alignment=ft.alignment.center,
                padding=20,
            ),
            ft.TextField(
                label="Outcome Name",
                hint_text="E.g.: purchase, signup, level_complete",
                value=outcome_name,
                on_change=lambda e: set_outcome_name(e.control.value),
            ),
            ft.Row(
                [
                    ft.FilledButton(
                        "Add Outcome",
                        icon=ft.Icons.ADD,
                        on_click=handle_add_outcome,
                    ),
                    ft.OutlinedButton(
                        "Add Unique",
                        on_click=handle_add_unique_outcome,
                    ),
                ],
                spacing=10,
            ),
            ft.Divider(height=10),
            ft.Text("Outcome with Value", weight=ft.FontWeight.W_500),
            ft.Row(
                [
                    ft.TextField(
                        label="Value",
                        hint_text="E.g.: 29.99",
                        value=outcome_value,
                        on_change=lambda e: set_outcome_value(e.control.value),
                        width=150,
                        keyboard_type=ft.KeyboardType.NUMBER,
                    ),
                    ft.FilledButton(
                        "Add with Value",
                        on_click=handle_add_outcome_with_value,
                    ),
                ],
                spacing=10,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
    )
