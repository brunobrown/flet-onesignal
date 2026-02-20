# Migration from v0.3.x

If upgrading from version 0.3.x, note these breaking changes:

## API Changes

| v0.3.x (Old)                          | v0.4.0 (New)                                      |
|----------------------------------------|---------------------------------------------------|
| `fos.OneSignalSettings(app_id=...)`   | `fos.OneSignal(app_id=...)`                       |
| `onesignal.get_onesignal_id()`        | `await onesignal.user.get_onesignal_id()`         |
| `onesignal.get_external_user_id()`    | `await onesignal.user.get_external_id()`          |
| `onesignal.login(id)`                 | `await onesignal.login(id)`                       |
| `onesignal.logout()`                  | `await onesignal.logout()`                        |
| `onesignal.set_language(code)`        | `await onesignal.user.set_language(code)`         |
| `onesignal.add_alias(alias, id)`      | `await onesignal.user.add_alias(label, id)`       |
| `onesignal.request_permission()`      | `await onesignal.notifications.request_permission()` |
| `onesignal.clear_all_notifications()` | `await onesignal.notifications.clear_all()`       |

## Event Name Changes

| v0.3.x (Old)                | v0.4.0 (New)                 |
|------------------------------|------------------------------|
| `on_notification_opened`     | `on_notification_click`      |
| `on_notification_received`   | `on_notification_foreground`  |
| `on_click_in_app_messages`   | `on_iam_click`               |

## Key Changes

- All methods are now **async-only** (no `_async` suffix)
- Methods are organized into **sub-modules** (`.user`, `.notifications`, etc.)
- Uses `ft.Service` base class instead of `Control`
- New event types with structured data
- Flet 0.80.x required (`ft.run(main)` instead of `ft.app(target=main)`)
