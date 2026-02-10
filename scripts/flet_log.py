#!/usr/bin/env python3
"""
Flet Logcat - Android Studio Style

A Python script for monitoring Android logcat with Flet/Flutter app filtering.
Automatically detects the focused app and filters relevant logs.

Usage: python flet_log.py [extra_filter]
Example: python flet_log.py "OneSignal|Firebase"
"""

import os
import re
import subprocess
import sys
import threading
import time
from typing import Optional

# Colors by log level (Android Studio style)
COLORS = {
    "V": "\033[0;37m",  # Verbose - Light gray
    "D": "\033[0;36m",  # Debug - Cyan
    "I": "\033[0;32m",  # Info - Green
    "W": "\033[0;33m",  # Warning - Yellow
    "E": "\033[0;31m",  # Error - Red
    "F": "\033[1;31m",  # Fatal - Bold red
    "A": "\033[1;31m",  # Assert - Bold red
}
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

# Default filter
DEFAULT_FILTER = r"flutter|python|Error|Exception|Traceback"

# Global state
current_process: Optional[subprocess.Popen] = None
stop_event = threading.Event()


def run_cmd(cmd: str) -> str:
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return result.stdout.strip()


def get_current_package() -> Optional[str]:
    """Get the currently focused app package name."""
    output = run_cmd("adb shell dumpsys activity activities 2>/dev/null")
    for line in output.splitlines():
        if "mResumedActivity" in line or "mFocusedActivity" in line:
            match = re.search(r"[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z0-9_]+)+", line)
            if match:
                return match.group(0)
    return None


def get_pid(package: str) -> Optional[str]:
    """Get the PID of a package."""
    pid = run_cmd(f"adb shell pidof {package} 2>/dev/null")
    return pid.split()[0] if pid else None


def format_log_line(line: str) -> Optional[str]:
    """Format a log line in Android Studio style."""
    # Format: MM-DD HH:MM:SS.mmm PID TID LEVEL TAG: MESSAGE
    pattern = r"^(\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}\.\d+)\s+(\d+)\s+(\d+)\s+([VDIWEFA])\s+([^:]+):\s+(.*)$"
    match = re.match(pattern, line)

    if match:
        date, time_str, pid, tid, level, tag, msg = match.groups()
        color = COLORS.get(level, RESET)
        # Format: TIME PID-TID TAG LEVEL: MESSAGE
        return f"{DIM}{time_str}{RESET} {DIM}{pid:>5}-{tid:<5}{RESET} {color}{tag:<20} {level}: {msg}{RESET}"
    else:
        # Unformatted line (continuation or different format)
        return f"{DIM}{line}{RESET}" if line.strip() else None


def print_header(pkg: str, pid: Optional[str]) -> None:
    """Print app header."""
    print()
    print(f"{BOLD}━━━ {pkg} {DIM}PID: {pid or '?'}{RESET}")
    print()


def print_usage(extra_filter: Optional[str]) -> None:
    """Print usage instructions."""
    os.system("clear" if os.name == "posix" else "cls")
    print(f"{BOLD}Logcat{RESET} {DIM}| Flet/Flutter{RESET}")
    print()
    print(f"{DIM}Usage: python flet_log.py [extra_filter]{RESET}")
    print(f'{DIM}Example: python flet_log.py "OneSignal|Firebase"{RESET}')
    print()
    print(f"{DIM}Default filter: flutter, python, Error, Exception, Traceback{RESET}")
    if extra_filter:
        print(f"{DIM}Extra filter: {extra_filter}{RESET}")
    print(f"{DIM}Press Ctrl+C to exit{RESET}")


def logcat_thread(pid: Optional[str], pkg: str, filter_pattern: str) -> None:
    """Thread to read and display logcat output."""
    global current_process

    try:
        if pid:
            cmd = ["adb", "logcat", "--pid", pid, "-v", "threadtime"]
        else:
            cmd = ["adb", "logcat", "-v", "threadtime"]

        current_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )

        # Compile filter pattern
        if pid:
            pattern = re.compile(filter_pattern, re.IGNORECASE)
        else:
            pattern = re.compile(f"{pkg}|{filter_pattern}", re.IGNORECASE)

        if current_process.stdout is None:
            return

        for line in current_process.stdout:
            if stop_event.is_set():
                break

            line = line.rstrip()
            if pattern.search(line):
                formatted = format_log_line(line)
                if formatted:
                    print(formatted)

    except Exception:
        pass
    finally:
        if current_process:
            current_process.terminate()
            current_process = None


def main() -> None:
    """Main entry point."""
    global current_process

    # Get extra filter from command line
    extra_filter = sys.argv[1] if len(sys.argv) > 1 else None

    # Build filter pattern
    filter_pattern = DEFAULT_FILTER
    if extra_filter:
        filter_pattern = f"{filter_pattern}|{extra_filter}"

    # Print usage
    print_usage(extra_filter)

    current_pkg = ""
    current_pid = ""
    logcat_thread_handle: Optional[threading.Thread] = None

    try:
        while True:
            pkg = get_current_package()

            if not pkg:
                time.sleep(1)
                continue

            pid = get_pid(pkg)

            if pkg != current_pkg or pid != current_pid:
                # Stop current logcat
                stop_event.set()
                if current_process:
                    current_process.terminate()
                if logcat_thread_handle and logcat_thread_handle.is_alive():
                    logcat_thread_handle.join(timeout=1)

                stop_event.clear()
                current_pkg = pkg
                current_pid = pid or ""

                print_header(pkg, pid)

                # Clear logcat
                run_cmd("adb logcat -c 2>/dev/null")

                # Start new logcat thread
                logcat_thread_handle = threading.Thread(
                    target=logcat_thread,
                    args=(pid, pkg, filter_pattern),
                    daemon=True,
                )
                logcat_thread_handle.start()

            time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        print()
        print(f"{DIM}Stopped{RESET}")
        stop_event.set()
        if current_process:
            current_process.terminate()


if __name__ == "__main__":
    main()
