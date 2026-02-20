# Location

> **Official docs:** [OneSignal Location Data](https://documentation.onesignal.com/docs/en/location-opt-in-prompt)

Share user location for geo-targeted messaging.

## Basic Usage

```python
# Request location permission
granted = await onesignal.location.request_permission()

# Enable location sharing
await onesignal.location.set_shared(True)

# Disable location sharing
await onesignal.location.set_shared(False)

# Check if location is being shared
is_shared = await onesignal.location.is_shared()
```

## Android Setup

On Android, the OneSignal Location module is **not included by default**. Without it, `set_shared(True)` will log `no location dependency found` and location will not work.

To enable it, you need to build your app using the `fos-build` CLI, which automatically injects the required Gradle dependencies.

### 1. Install the CLI

```bash
# Using UV (Recommended)
uv add flet-onesignal[cli]

# Using pip
pip install flet-onesignal[cli]
```

### 2. Add location permissions

Add to your `pyproject.toml`:

```toml
[tool.flet.android]
permission."android.permission.ACCESS_FINE_LOCATION" = true
permission."android.permission.ACCESS_COARSE_LOCATION" = true
```

These permissions are required in the Android Manifest for the app to access the device's GPS.

### 3. Enable the OneSignal Location module

Via `pyproject.toml`:

```toml
[tool.flet.onesignal.android]
location = true
```

Or pass the flag directly:

```bash
fos-build apk --location
```

### 4. Build with fos-build

```bash
fos-build apk
```

!!! warning
    Using `flet build apk` directly (without `fos-build`) will **not** inject the
    location module and the feature will silently fail at runtime.
