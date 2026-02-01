<p align="center"><img src="https://github.com/user-attachments/assets/ee3f4caf-10a7-4c58-948d-6a59fda97850" width="300" height="150" alt="Flet OneSignal"></p>


<h1 align="center"> Flet OneSignal </h1>

## Overview

Flet OneSignal is an extension for Flet in Python, integrating the OneSignal Flutter SDK. It enables push notifications, in-app messaging, and user management for mobile apps, making it easier to connect your iOS and Android applications with OneSignal.

**Version 0.4.0** - Updated for Flet 0.80.x with modular architecture mirroring the OneSignal SDK structure.

## Buy Me a Coffee
If you liked this project, please consider supporting its development with a donation. Your contribution will help me maintain and improve it.

<a href="https://www.buymeacoffee.com/brunobrown">
<img src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-1.svg" width="200" alt="Buy Me a Coffee">
</a>

## Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ |
| Flet | 0.80.5+ |
| Flutter | 3.29.0+ |
| OneSignal Flutter SDK | 5.4.0 |
| iOS | 12+ |
| Android | API 24+ (Android 7.0) |

## Installation

You can install `flet-onesignal` using one of the following package managers:

**UV (Recommended)**

```console
uv add flet-onesignal
```

**PIP**

```console
pip install flet-onesignal
```

**POETRY**

```console
poetry add flet-onesignal
```

---

## Configuration

Add `flet-onesignal` to your `pyproject.toml`:

```toml
[project]
name = "my-flet-app"
version = "0.1.0"
requires-python = ">=3.10"

dependencies = [
    "flet>=0.80.5",
    "flet-onesignal>=0.4.0",
]

[tool.flet]
# Your flet build configuration
```

---

## Quick Start

```python
import flet as ft
import flet_onesignal as fos

ONESIGNAL_APP_ID = "your-onesignal-app-id"

async def main(page: ft.Page):
    # Create OneSignal service
    onesignal = fos.OneSignal(app_id=ONESIGNAL_APP_ID)
    page.overlay.append(onesignal)

    # Request notification permission
    granted = await onesignal.notifications.request_permission()
    print(f"Permission granted: {granted}")

    # Login user
    await onesignal.login("user-123")

    page.add(ft.Text("OneSignal initialized!"))

if __name__ == "__main__":
    ft.run(main)
```

---

## Architecture

The package follows the OneSignal SDK's modular architecture:

```
OneSignal (main service)
├── onesignal.debug          # Logging configuration
├── onesignal.user           # User identity, tags, aliases, email, SMS
├── onesignal.notifications  # Push notification management
├── onesignal.in_app_messages # In-app message triggers and lifecycle
├── onesignal.location       # Location sharing
├── onesignal.session        # Outcomes tracking
└── onesignal.live_activities # Live Activities (iOS only)
```

---

## Complete Example

```python
import flet as ft
import flet_onesignal as fos

ONESIGNAL_APP_ID = "your-onesignal-app-id"

async def main(page: ft.Page):
    page.title = "OneSignal Demo"

    # Event log display
    log_list = ft.ListView(expand=True, spacing=5)

    def add_log(message: str):
        log_list.controls.append(ft.Text(message, size=12))
        page.update()

    # Event handlers
    def on_notification_click(e: fos.OSNotificationClickEvent):
        add_log(f"Notification clicked: {e.notification}")

    def on_notification_foreground(e: fos.OSNotificationWillDisplayEvent):
        add_log(f"Notification received: {e.notification}")

    def on_permission_change(e: fos.OSPermissionChangeEvent):
        add_log(f"Permission changed: {e.permission}")

    def on_user_change(e: fos.OSUserChangedEvent):
        add_log(f"User changed - ID: {e.state.onesignal_id}")

    def on_iam_click(e: fos.OSInAppMessageClickEvent):
        add_log(f"IAM clicked: {e.result.action_id}")

    def on_error(e: fos.OSErrorEvent):
        add_log(f"Error: {e.method} - {e.message}")

    # Create OneSignal with event handlers
    onesignal = fos.OneSignal(
        app_id=ONESIGNAL_APP_ID,
        log_level=fos.OSLogLevel.DEBUG,
        on_notification_click=on_notification_click,
        on_notification_foreground=on_notification_foreground,
        on_permission_change=on_permission_change,
        on_user_change=on_user_change,
        on_iam_click=on_iam_click,
        on_error=on_error,
    )
    page.overlay.append(onesignal)

    # Button handlers
    async def request_permission(e):
        result = await onesignal.notifications.request_permission()
        add_log(f"Permission granted: {result}")

    async def get_onesignal_id(e):
        result = await onesignal.user.get_onesignal_id()
        add_log(f"OneSignal ID: {result}")

    async def login_user(e):
        await onesignal.login("user-123")
        add_log("User logged in")

    async def logout_user(e):
        await onesignal.logout()
        add_log("User logged out")

    async def add_tag(e):
        await onesignal.user.add_tag("premium", "true")
        add_log("Tag added: premium=true")

    async def set_language(e):
        await onesignal.user.set_language("pt")
        add_log("Language set to Portuguese")

    # Build UI
    page.add(
        ft.Column([
            ft.Row([
                ft.ElevatedButton("Request Permission", on_click=request_permission),
                ft.ElevatedButton("Get OneSignal ID", on_click=get_onesignal_id),
            ], wrap=True),
            ft.Row([
                ft.ElevatedButton("Login", on_click=login_user),
                ft.ElevatedButton("Logout", on_click=logout_user),
            ], wrap=True),
            ft.Row([
                ft.ElevatedButton("Add Tag", on_click=add_tag),
                ft.ElevatedButton("Set Language", on_click=set_language),
            ], wrap=True),
            ft.Divider(),
            ft.Text("Event Logs:", weight=ft.FontWeight.BOLD),
            ft.Container(content=log_list, expand=True, border=ft.border.all(1)),
        ], expand=True)
    )

    add_log("OneSignal initialized!")

if __name__ == "__main__":
    ft.run(main)
```

---

## API Reference

### OneSignal (Main Service)

```python
onesignal = fos.OneSignal(
    app_id="your-app-id",
    log_level=fos.OSLogLevel.DEBUG,  # Optional
    require_consent=False,            # Optional: GDPR consent
)

# Main methods
await onesignal.login("external-user-id")
await onesignal.logout()
await onesignal.consent_given(True)  # When require_consent=True
```

### User Management

```python
# Identity
onesignal_id = await onesignal.user.get_onesignal_id()
external_id = await onesignal.user.get_external_id()

# Tags
await onesignal.user.add_tag("key", "value")
await onesignal.user.add_tags({"key1": "value1", "key2": "value2"})
await onesignal.user.remove_tag("key")
tags = await onesignal.user.get_tags()

# Aliases
await onesignal.user.add_alias("crm_id", "12345")
await onesignal.user.remove_alias("crm_id")

# Email & SMS
await onesignal.user.add_email("user@example.com")
await onesignal.user.remove_email("user@example.com")
await onesignal.user.add_sms("+5511999999999")
await onesignal.user.remove_sms("+5511999999999")

# Language
await onesignal.user.set_language("pt")

# Push subscription
await onesignal.user.opt_in_push()
await onesignal.user.opt_out_push()
is_opted_in = await onesignal.user.is_push_opted_in()
```

### Notifications

```python
# Permission
granted = await onesignal.notifications.request_permission(fallback_to_settings=True)
can_request = await onesignal.notifications.can_request_permission()
has_permission = await onesignal.notifications.get_permission()

# iOS provisional authorization
await onesignal.notifications.register_for_provisional_authorization()

# Clear notifications
await onesignal.notifications.clear_all()
await onesignal.notifications.remove_notification(notification_id)  # Android
await onesignal.notifications.remove_grouped_notifications("group")  # Android

# Foreground display control
await onesignal.notifications.prevent_default(notification_id)
await onesignal.notifications.display(notification_id)
```

### In-App Messages

```python
# Triggers
await onesignal.in_app_messages.add_trigger("key", "value")
await onesignal.in_app_messages.add_triggers({"key1": "value1"})
await onesignal.in_app_messages.remove_trigger("key")
await onesignal.in_app_messages.clear_triggers()

# Pause/Resume
await onesignal.in_app_messages.pause()
await onesignal.in_app_messages.resume()
is_paused = await onesignal.in_app_messages.is_paused()
```

### Location

```python
granted = await onesignal.location.request_permission()
await onesignal.location.set_shared(True)
is_shared = await onesignal.location.is_shared()
```

### Session (Outcomes)

```python
await onesignal.session.add_outcome("purchase")
await onesignal.session.add_unique_outcome("signup")
await onesignal.session.add_outcome_with_value("revenue", 29.99)
```

### Live Activities (iOS only)

```python
await onesignal.live_activities.enter("activity-id", "token")
await onesignal.live_activities.exit("activity-id")
await onesignal.live_activities.set_push_to_start_token("activity-type", "token")
await onesignal.live_activities.remove_push_to_start_token("activity-type")
```

### Debug

```python
await onesignal.debug.set_log_level(fos.OSLogLevel.VERBOSE)
await onesignal.debug.set_alert_level(fos.OSLogLevel.ERROR)
```

---

## Event Types

| Event | Description |
|-------|-------------|
| `OSNotificationClickEvent` | User clicked a notification |
| `OSNotificationWillDisplayEvent` | Notification will display in foreground |
| `OSPermissionChangeEvent` | Permission status changed |
| `OSUserChangedEvent` | User state changed |
| `OSPushSubscriptionChangedEvent` | Push subscription changed |
| `OSInAppMessageClickEvent` | User clicked in-app message |
| `OSInAppMessageWillDisplayEvent` | IAM will display |
| `OSInAppMessageDidDisplayEvent` | IAM did display |
| `OSInAppMessageWillDismissEvent` | IAM will dismiss |
| `OSInAppMessageDidDismissEvent` | IAM did dismiss |
| `OSErrorEvent` | Error occurred |

---

## Log Levels

```python
class OSLogLevel(Enum):
    NONE = "none"
    FATAL = "fatal"
    ERROR = "error"
    WARN = "warn"
    INFO = "info"
    DEBUG = "debug"
    VERBOSE = "verbose"
```

---

## Migration from v0.3.x

If you're upgrading from version 0.3.x, here are the key changes:

| v0.3.x | v0.4.0 |
|--------|--------|
| `OneSignalSettings(app_id=...)` | `OneSignal(app_id=...)` |
| `onesignal.get_onesignal_id()` | `await onesignal.user.get_onesignal_id()` |
| `onesignal.login(id)` | `await onesignal.login(id)` |
| `onesignal.set_language(code)` | `await onesignal.user.set_language(code)` |
| `onesignal.request_permission()` | `await onesignal.notifications.request_permission()` |
| `on_notification_opened` | `on_notification_click` |
| `on_notification_received` | `on_notification_foreground` |
| `ft.app(target=main)` | `ft.run(main)` |

All methods are now **async-only** (no `_async` suffix).

---

## Contributing
Contributions and feedback are welcome!

#### To contribute:

1. **Fork the repository.**
2. **Create a feature branch.**
3. **Submit a pull request with a detailed explanation of your changes.**

---

## Try **flet-onesignal** today and enhance your Flet apps with push notifications!

<img src="https://logging-discord.readthedocs.io/en/latest/img/proverbs_16_3.jpg" width="500">

[Commit your work to the LORD, and your plans will succeed. Proverbs 16: 3](https://www.bible.com/bible/116/PRO.16.NLT)
