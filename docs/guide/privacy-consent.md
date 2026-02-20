# Privacy & Consent

> **Official docs:** [OneSignal Handling Personal Data](https://documentation.onesignal.com/docs/en/handling-personal-data)

For GDPR and other privacy regulations, you can require user consent before the SDK collects data.

## Enable Consent Requirement

```python
import flet_onesignal as fos

# Create OneSignal with consent requirement
onesignal = fos.OneSignal(
    app_id=ONESIGNAL_APP_ID,
    require_consent=True,  # SDK won't collect data until consent is given
)
```

## Give or Revoke Consent

```python
# After user accepts your privacy policy
await onesignal.consent_given(True)

# If user declines or revokes consent
await onesignal.consent_given(False)
```

!!! important
    `require_consent=True` must be set in the constructor for the consent methods
    to work. Without it, the SDK is fully active from initialization and calling
    `consent_given()` has no practical effect.
