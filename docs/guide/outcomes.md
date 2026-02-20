# Outcomes

> **Official docs:** [OneSignal Outcomes](https://documentation.onesignal.com/docs/en/custom-outcomes)

Track user actions and conversions attributed to notifications.

## Simple Outcome

```python
# Track a simple outcome
await onesignal.session.add_outcome("product_viewed")
```

## Unique Outcome

Unique outcomes are only counted once per notification or in-app message that influenced the user:

```python
await onesignal.session.add_unique_outcome("app_opened")
```

## Outcome with Value

Track monetary values or quantities associated with user actions:

```python
await onesignal.session.add_outcome_with_value("purchase", 29.99)
```
