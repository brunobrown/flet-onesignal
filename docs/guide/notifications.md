# Push Notifications

> **Official docs:** [OneSignal Push Notification Guide](https://documentation.onesignal.com/docs/en/push)

## Requesting Permission

You must request permission before sending push notifications:

```python
# Request permission with fallback to settings
granted = await onesignal.notifications.request_permission(
    fallback_to_settings=True  # Opens settings if previously denied
)

if granted:
    print("User granted notification permission!")
else:
    print("User denied notification permission")
```

## Check Permission Status

```python
# Check if permission can be requested (not yet prompted)
can_request = await onesignal.notifications.can_request_permission()

# Check current permission status
has_permission = await onesignal.notifications.get_permission()
```

## iOS Provisional Authorization

Request provisional (quiet) authorization on iOS 12+:

```python
# Notifications will be delivered quietly to Notification Center
authorized = await onesignal.notifications.register_for_provisional_authorization()
```

## Managing Notifications

```python
# Clear all notifications from the notification center
await onesignal.notifications.clear_all()

# Remove a specific notification (Android only)
await onesignal.notifications.remove_notification(notification_id)

# Remove a group of notifications (Android only)
await onesignal.notifications.remove_grouped_notifications("group_key")
```

## Foreground Display Control

Control whether notifications are shown when the app is in the foreground:

```python
async def on_foreground(e: fos.OSNotificationWillDisplayEvent):
    # Prevent a notification from being displayed
    await onesignal.notifications.prevent_default(e.notification_id)

    # Process notification data...

    # Later, allow display if needed
    await onesignal.notifications.display(e.notification_id)
```

## Event Handlers

```python
import flet_onesignal as fos


def on_notification_click(e: fos.OSNotificationClickEvent):
    """Called when user taps on a notification."""
    print(f"Notification clicked: {e.notification}")
    print(f"Action ID: {e.action_id}")


def on_notification_foreground(e: fos.OSNotificationWillDisplayEvent):
    """Called when notification received while app is in foreground."""
    print(f"Notification received: {e.notification}")
    print(f"Notification ID: {e.notification_id}")


def on_permission_change(e: fos.OSPermissionChangeEvent):
    """Called when notification permission status changes."""
    print(f"Permission granted: {e.permission}")


onesignal = fos.OneSignal(
    app_id=ONESIGNAL_APP_ID,
    on_notification_click=on_notification_click,
    on_notification_foreground=on_notification_foreground,
    on_permission_change=on_permission_change,
)
```
