# In-App Messages

> **Official docs:** [OneSignal In-App Messages Quickstart](https://documentation.onesignal.com/docs/en/in-app-messages-setup)

In-App Messages (IAMs) are messages displayed within your app based on triggers.

## Triggers

Triggers determine when IAMs are displayed:

```python
# Add a trigger
await onesignal.in_app_messages.add_trigger("level_completed", "5")

# Add multiple triggers
await onesignal.in_app_messages.add_triggers({
    "screen": "checkout",
    "cart_value": "50",
})

# Remove a trigger
await onesignal.in_app_messages.remove_trigger("old_trigger")

# Remove multiple triggers
await onesignal.in_app_messages.remove_triggers(["trigger1", "trigger2"])

# Clear all triggers
await onesignal.in_app_messages.clear_triggers()
```

## Pausing In-App Messages

Temporarily prevent IAMs from displaying:

```python
# Pause IAM display
await onesignal.in_app_messages.pause()

# Resume IAM display
await onesignal.in_app_messages.resume()

# Check if paused
is_paused = await onesignal.in_app_messages.is_paused()
```

## Event Handlers

```python
import flet_onesignal as fos


def on_iam_click(e: fos.OSInAppMessageClickEvent):
    """Called when user interacts with an IAM."""
    print(f"IAM clicked - Action: {e.result.action_id}")
    print(f"URL: {e.result.url}")
    print(f"Closing message: {e.result.closing_message}")


def on_iam_will_display(e: fos.OSInAppMessageWillDisplayEvent):
    """Called before an IAM is displayed."""
    print(f"IAM will display: {e.message}")


def on_iam_did_display(e: fos.OSInAppMessageDidDisplayEvent):
    """Called after an IAM is displayed."""
    print("IAM displayed")


def on_iam_will_dismiss(e: fos.OSInAppMessageWillDismissEvent):
    """Called before an IAM is dismissed."""
    print("IAM will dismiss")


def on_iam_did_dismiss(e: fos.OSInAppMessageDidDismissEvent):
    """Called after an IAM is dismissed."""
    print("IAM dismissed")


onesignal = fos.OneSignal(
    app_id=ONESIGNAL_APP_ID,
    on_iam_click=on_iam_click,
    on_iam_will_display=on_iam_will_display,
    on_iam_did_display=on_iam_did_display,
    on_iam_will_dismiss=on_iam_will_dismiss,
    on_iam_did_dismiss=on_iam_did_dismiss,
)
```
