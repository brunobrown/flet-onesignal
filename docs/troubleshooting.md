# Troubleshooting

## Notifications not appearing

1. Verify your OneSignal App ID is correct
2. Check that you've requested and received notification permission
3. Ensure platform certificates (APNs/FCM) are configured in the OneSignal dashboard
4. Check device logs for any SDK errors
5. Enable debug logging with `log_level=fos.OSLogLevel.VERBOSE`

## App crashes on startup

1. Verify minimum SDK versions are met (Android API 24+, iOS 12+)
2. Check that OneSignal is added to `page.services` (not `page.overlay`)
3. Review the `on_error` handler for any initialization errors

## Tags not syncing

1. Tags are synced asynchronously — allow a few seconds
2. Check your network connection
3. Verify tags in the OneSignal dashboard under Users

## Location not working (Android)

1. Ensure you're building with `fos-build` (not plain `flet build`)
2. Verify `[tool.flet.onesignal.android] location = true` is in `pyproject.toml`
3. Check that location permissions are declared in `[tool.flet.android]`
4. On the device: Request Permission first, then Enable, then Check Status

## FletUnsupportedPlatformException

OneSignal only supports Android and iOS. If you're running on web, desktop, or another
platform, SDK methods will raise `FletUnsupportedPlatformException`. Guard your calls:

```python
try:
    await onesignal.notifications.request_permission()
except ft.FletUnsupportedPlatformException:
    print("OneSignal not supported on this platform")
```
