# User Management

> **Official docs:** [OneSignal Users](https://documentation.onesignal.com/docs/en/users)

## Login and Logout

Associate users with their account in your system using an **External User ID**:

```python
# Login - Associates the device with your user ID
await onesignal.login("user_12345")

# Logout - Removes the association, creates anonymous user
await onesignal.logout()
```

!!! tip
    Call `login()` when the user signs into your app and `logout()` when they sign out.

## Get User IDs

```python
# Get the OneSignal-generated user ID
onesignal_id = await onesignal.user.get_onesignal_id()
print(f"OneSignal ID: {onesignal_id}")

# Get the External User ID (set via login)
external_id = await onesignal.user.get_external_id()
print(f"External ID: {external_id}")
```

## Tags

Tags are key-value pairs used for segmentation and personalization:

```python
# Add a single tag
await onesignal.user.add_tag("subscription_type", "premium")

# Add multiple tags at once
await onesignal.user.add_tags({
    "favorite_team": "barcelona",
    "notification_frequency": "daily",
    "app_version": "2.1.0",
})

# Remove a tag
await onesignal.user.remove_tag("old_tag")

# Remove multiple tags
await onesignal.user.remove_tags(["tag1", "tag2", "tag3"])

# Get all tags
tags = await onesignal.user.get_tags()
print(f"User tags: {tags}")
```

## Aliases

Aliases allow you to associate multiple identifiers with a single user:

```python
# Add an alias (e.g., CRM ID, database ID)
await onesignal.user.add_alias("crm_id", "CRM_98765")

# Add multiple aliases
await onesignal.user.add_aliases({
    "database_id": "DB_12345",
    "analytics_id": "GA_67890",
})

# Remove an alias
await onesignal.user.remove_alias("old_alias")
```

## Email Subscriptions

Add email addresses for omnichannel messaging:

```python
# Add an email subscription
await onesignal.user.add_email("user@example.com")

# Remove an email subscription
await onesignal.user.remove_email("user@example.com")
```

## SMS Subscriptions

Add phone numbers for SMS messaging (use E.164 format):

```python
# Add SMS subscription (E.164 format: +[country code][number])
await onesignal.user.add_sms("+5511999999999")

# Remove SMS subscription
await onesignal.user.remove_sms("+5511999999999")
```

## Language

Set the user's preferred language for localized notifications:

```python
# Set language using ISO 639-1 code
await onesignal.user.set_language("pt")  # Portuguese
await onesignal.user.set_language("es")  # Spanish
await onesignal.user.set_language("en")  # English

# You can also use the Language enum for auto-complete support
import flet_onesignal as fos
await onesignal.user.set_language(fos.Language.PORTUGUESE.value)
```

## Push Subscription Control

```python
# Opt user into push notifications
await onesignal.user.opt_in_push()

# Opt user out of push notifications
await onesignal.user.opt_out_push()

# Check if user is opted in
is_opted_in = await onesignal.user.is_push_opted_in()

# Get push subscription details
subscription_id = await onesignal.user.get_push_subscription_id()
push_token = await onesignal.user.get_push_subscription_token()
```

## Event Handlers

```python
def on_user_change(e: fos.OSUserChangedEvent):
    """Called when the user state changes."""
    print(f"OneSignal ID: {e.state.onesignal_id}")
    print(f"External ID: {e.state.external_id}")


def on_push_subscription_change(e: fos.OSPushSubscriptionChangedEvent):
    """Called when push subscription state changes."""
    print(f"Subscription ID: {e.id}")
    print(f"Token: {e.token}")
    print(f"Opted in: {e.opted_in}")


onesignal = fos.OneSignal(
    app_id=ONESIGNAL_APP_ID,
    on_user_change=on_user_change,
    on_push_subscription_change=on_push_subscription_change,
)
```
