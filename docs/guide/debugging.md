# Debugging

## Log Levels

Configure SDK logging for development:

```python
import flet_onesignal as fos

# Set log level during initialization
onesignal = fos.OneSignal(
    app_id=ONESIGNAL_APP_ID,
    log_level=fos.OSLogLevel.VERBOSE,
)

# Or change it dynamically
await onesignal.debug.set_log_level(fos.OSLogLevel.DEBUG)

# Set alert level (visual alerts for errors, iOS only)
await onesignal.debug.set_alert_level(fos.OSLogLevel.ERROR)
```

**Available log levels:**

| Level     | Description                             |
|-----------|-----------------------------------------|
| `NONE`    | No logging                              |
| `FATAL`   | Only fatal errors                       |
| `ERROR`   | Errors and fatal errors                 |
| `WARN`    | Warnings and above                      |
| `INFO`    | Informational messages and above        |
| `DEBUG`   | Debug messages and above                |
| `VERBOSE` | All messages including verbose details  |

## Error Handling

```python
def on_error(e: fos.OSErrorEvent):
    """Called when an error occurs in the SDK."""
    print(f"Error in {e.method}: {e.message}")
    if e.stack_trace:
        print(f"Stack trace: {e.stack_trace}")


onesignal = fos.OneSignal(
    app_id=ONESIGNAL_APP_ID,
    on_error=on_error,
)
```

## Debug Console

A built-in visual console for viewing application logs during development:

```python
import flet as ft
import flet_onesignal as fos

# Setup file-based logging
logger = fos.setup_logging()


async def main(page: ft.Page):
    debug_console = fos.DebugConsole()

    page.appbar = ft.AppBar(
        title=ft.Text("My App"),
        actions=[debug_console.icon],  # Bug icon opens the console
    )

    # Or use a floating action button instead
    # page.floating_action_button = debug_console.fab

    logger.info("App started")
    page.add(ft.Text("Hello World"))


ft.run(main)
```

The `DebugConsole` reads log entries written by `setup_logging()` and displays them in a filterable dialog with color-coded levels.

## Android Logcat Scripts

The [`scripts/`](https://github.com/brunobrown/flet-onesignal/tree/main/scripts) directory includes two logcat viewer scripts that display Android logs with **Android Studio-style colors and formatting**. They auto-detect the focused app, filter by its PID, and highlight Flet/Flutter, Python errors and exceptions.

**Bash version** (Linux/macOS — requires `adb` in PATH):

```bash
# Default filter (flutter, python, Error, Exception, Traceback)
./scripts/flet_log.sh

# Add extra filters
./scripts/flet_log.sh "OneSignal|Firebase"
```

**Python version** (cross-platform):

```bash
python scripts/flet_log.py

python scripts/flet_log.py "OneSignal|Firebase"
```

!!! info "Requirement"
    A device or emulator connected via `adb`. The scripts clear the logcat buffer on each app restart so you only see fresh output.
