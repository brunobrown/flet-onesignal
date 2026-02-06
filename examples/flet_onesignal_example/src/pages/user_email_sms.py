"""
User Email/SMS page - Manage communication channels.
"""

import flet as ft
from components.log_viewer import LogViewer
from components.page_layout import PageLayout
from context import AppCtx


@ft.component
def UserEmailSmsPage():
    """
    Page for managing user email and SMS subscriptions.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    # Local state
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
            state.add_log(f"Error adding email: {ex}", "error")

    async def handle_remove_email(e):
        if not email:
            state.add_log("Enter the email to remove", "warning")
            return
        try:
            await onesignal.user.remove_email(email)
            state.add_log(f"Email removed: {email}", "success")
        except Exception as ex:
            state.add_log(f"Error removing email: {ex}", "error")

    async def handle_add_sms(e):
        if not phone:
            state.add_log("Enter a phone number", "warning")
            return
        try:
            await onesignal.user.add_sms(phone)
            state.add_log(f"SMS added: {phone}", "success")
        except Exception as ex:
            state.add_log(f"Error adding SMS: {ex}", "error")

    async def handle_remove_sms(e):
        if not phone:
            state.add_log("Enter the phone to remove", "warning")
            return
        try:
            await onesignal.user.remove_sms(phone)
            state.add_log(f"SMS removed: {phone}", "success")
        except Exception as ex:
            state.add_log(f"Error removing SMS: {ex}", "error")

    return PageLayout(
        title="User - Email / SMS",
        description=(
            "Add alternative communication channels for the user. "
            "Email and SMS allow sending messages even when the user "
            "doesn't have the app installed or has disabled push notifications. "
            "Use E.164 format for phone numbers (+15551234567)."
        ),
        code_example="""# Add email
await onesignal.user.add_email("user@example.com")

# Remove email
await onesignal.user.remove_email("user@example.com")

# Add SMS (E.164 format)
await onesignal.user.add_sms("+15551234567")

# Remove SMS
await onesignal.user.remove_sms("+15551234567")""",
        children=[
            ft.Text("Email", weight=ft.FontWeight.W_500, size=16),
            ft.TextField(
                label="Email",
                hint_text="user@example.com",
                value=email,
                on_change=lambda e: set_email(e.control.value),
                keyboard_type=ft.KeyboardType.EMAIL,
            ),
            ft.Row(
                [
                    ft.FilledButton("Add Email", icon=ft.Icons.EMAIL, on_click=handle_add_email),
                    ft.OutlinedButton(
                        "Remove Email", icon=ft.Icons.DELETE, on_click=handle_remove_email
                    ),
                ],
                spacing=10,
            ),
            ft.Divider(height=20),
            ft.Text("SMS", weight=ft.FontWeight.W_500, size=16),
            ft.TextField(
                label="Phone",
                hint_text="+15551234567",
                value=phone,
                on_change=lambda e: set_phone(e.control.value),
                keyboard_type=ft.KeyboardType.PHONE,
            ),
            ft.Row(
                [
                    ft.FilledButton("Add SMS", icon=ft.Icons.SMS, on_click=handle_add_sms),
                    ft.OutlinedButton(
                        "Remove SMS", icon=ft.Icons.DELETE, on_click=handle_remove_sms
                    ),
                ],
                spacing=10,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
    )
