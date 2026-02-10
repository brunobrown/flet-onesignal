"""User Email/SMS page."""

import flet as ft
from components.log_viewer import LogViewer
from context import AppCtx


@ft.component
def UserEmailSmsPage():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    email, set_email = ft.use_state("")
    phone, set_phone = ft.use_state("")

    async def handle_add_email(e):
        if not email:
            state.add_log("Enter an email", "warning")
            return
        try:
            await onesignal.user.add_email(email)
            state.add_log(f"Email added: {email}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_remove_email(e):
        if not email:
            state.add_log("Enter the email", "warning")
            return
        try:
            await onesignal.user.remove_email(email)
            state.add_log(f"Email removed: {email}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_add_sms(e):
        if not phone:
            state.add_log("Enter a phone number", "warning")
            return
        try:
            await onesignal.user.add_sms(phone)
            state.add_log(f"SMS added: {phone}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    async def handle_remove_sms(e):
        if not phone:
            state.add_log("Enter the phone number", "warning")
            return
        try:
            await onesignal.user.remove_sms(phone)
            state.add_log(f"SMS removed: {phone}", "success")
        except Exception as ex:
            state.add_log(f"Error: {ex}", "error")

    return ft.Column(
        [
            ft.Text("User - Email / SMS", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Add alternative communication channels.",
                size=14,
                color=ft.Colors.GREY_700,
            ),
            ft.TextButton(
                "Documentation: Subscriptions",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://documentation.onesignal.com/docs/subscriptions",
            ),
            ft.Divider(height=20),
            ft.Text("Email", weight=ft.FontWeight.W_500),
            ft.TextField(
                label="Email",
                hint_text="user@example.com",
                value=email,
                on_change=lambda e: set_email(e.control.value),
            ),
            ft.Row(
                [
                    ft.FilledButton("Add Email", on_click=handle_add_email),
                    ft.OutlinedButton("Remove Email", on_click=handle_remove_email),
                ],
                spacing=10,
            ),
            ft.Divider(height=10),
            ft.Text("SMS", weight=ft.FontWeight.W_500),
            ft.TextField(
                label="Phone",
                hint_text="+15551234567",
                value=phone,
                on_change=lambda e: set_phone(e.control.value),
            ),
            ft.Row(
                [
                    ft.FilledButton("Add SMS", on_click=handle_add_sms),
                    ft.OutlinedButton("Remove SMS", on_click=handle_remove_sms),
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
