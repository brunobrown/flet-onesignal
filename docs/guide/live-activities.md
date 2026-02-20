# Live Activities

> **Official docs:** [OneSignal Live Activities](https://documentation.onesignal.com/docs/en/live-activities)

Update iOS Live Activities in real-time (iOS 16.1+).

!!! note
    Live Activities are an **iOS-only** feature that displays real-time information
    on the Lock Screen and in the Dynamic Island.

## Enter a Live Activity

```python
await onesignal.live_activities.enter(
    activity_id="delivery_12345",
    token="live_activity_push_token",
)
```

## Exit a Live Activity

```python
await onesignal.live_activities.exit("delivery_12345")
```

## Push-to-Start Token

Set a push-to-start token to allow OneSignal to start a Live Activity via push:

```python
await onesignal.live_activities.set_push_to_start_token(
    activity_type="DeliveryActivityAttributes",
    token="push_to_start_token",
)

# Remove the token
await onesignal.live_activities.remove_push_to_start_token(
    "DeliveryActivityAttributes"
)
```

## Default Setup

```python
await onesignal.live_activities.setup_default()
```
