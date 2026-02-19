## [Unreleased]

## [0.4.2] - 2026-02-19

### Changed
- Replace all `print()` calls with `debugPrint()` in Dart code for cleaner production output
- Improve error handling with `FlutterError.reportError()` in `_handleError()`
- Remove verbose logging from event listeners (events already forwarded via `triggerEvent`)
- Refactor: remove Firebase from CLI; simplify `fos-build` for OneSignal module injection only

### Added
- Unit test suite (60 tests) covering `build`, `console`, `types`, and `languages` modules
- Enable test step with coverage in CI workflows (`main.yml`, `dev.yml`)
- GitHub Actions CI workflows for `main` and `dev` branches (ruff, ty, version bump check)
- Python 3.14 support and classifier
- Note in README about using `page.services.append()` instead of `page.overlay.append()`

### Fixed
- Python 3.10 compatibility — add `tomli` fallback for `tomllib` (stdlib 3.11+)

## [0.4.1] - 2026-02-14

### Fixed
- Move `rich` and `watchdog` to optional `[cli]` dependency to prevent `flet build` from stalling

## [0.4.0] - 2026-02-10

### Changed
- **BREAKING:** Migrate to Flet 0.80.x Extension/Service pattern (`FletExtension` + `FletService`)
- **BREAKING:** Modular API — methods reorganized into sub-modules (`.user`, `.notifications`, `.in_app_messages`, `.location`, `.session`, `.live_activities`, `.debug`)
- **BREAKING:** All methods are now async-only (no `_async` suffix)
- **BREAKING:** Renamed events (`on_notification_opened` -> `on_notification_click`, `on_notification_received` -> `on_notification_foreground`, `on_click_in_app_messages` -> `on_iam_click`)
- **BREAKING:** Constructor changed from `fos.OneSignalSettings(app_id=...)` to `fos.OneSignal(app_id=...)`
- Migrate package manager from Poetry to UV
- Restructure to `src/` layout (`src/flet_onesignal/` + `src/flutter/flet_onesignal/`)
- CLI `fos-build` now supports all 7 Flet platforms (apk, aab, ipa, web, macos, linux, windows)
- CLI output improved with `rich` formatting

### Added
- Full OneSignal SDK coverage: push notifications, in-app messages, user management (tags, aliases, email, SMS), location, session outcomes, live activities (iOS), privacy/consent, debugging
- `fos-build` CLI with `--location` flag for automatic OneSignal Location module injection on Android
- Structured event types (`OSNotificationClickEvent`, `OSPermissionChangeEvent`, `OSInAppMessageClickEvent`, etc.)
- `OSLogLevel` enum for SDK log configuration
- `Language` enum for user language setting
- `DebugConsole` component and `setup_logging()` for visual debug logging
- Android logcat viewer scripts (`flet_log.sh`, `flet_log.py`)
- Complete example app demonstrating all features with Flet declarative UI

### Fixed
- Map type conversion and JSON parsing for tags
- Coroutine error in async return values

## [0.3.3] - 2025-06-03

### Fixed
- Coroutine error in async method returns
- Alias method argument key names

### Added
- Async versions of all SDK methods

### Changed
- Remove unused Flutter packages and comments

## [0.3.1] - 2025-03-09

### Added
- `external_user_id` control for user identification

## [0.2.0] - 2025-02-13

### Changed
- Migrate package manager from Poetry to UV
- Restructure package directories
- Update Flet version dependency
- Move Flutter package directory to project root

### Added
- Build configuration for including Flutter package in wheel
- Example app (`main.py`)

## [0.1.0] - 2024-12-22

### Added
- Initial release
- OneSignal Flutter SDK integration for Flet
- Basic push notification support (permission, click events, foreground events)
- Python API wrapping the OneSignal Flutter SDK
- Poetry-based build system with Flutter package bundled
