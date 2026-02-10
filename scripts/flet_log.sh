#!/bin/bash

# ══════════════════════════════════════════════════════════════════════════════
# Flet Logcat - Android Studio Style
# ══════════════════════════════════════════════════════════════════════════════
# Usage: ./flet_log.sh [filter]
# Example: ./flet_log.sh "OneSignal|Firebase"
# ══════════════════════════════════════════════════════════════════════════════

# Colors by log level (Android Studio style)
declare -A COLORS=(
    [V]="\033[0;37m"      # Verbose - Light gray
    [D]="\033[0;36m"      # Debug - Cyan
    [I]="\033[0;32m"      # Info - Green
    [W]="\033[0;33m"      # Warning - Yellow
    [E]="\033[0;31m"      # Error - Red
    [F]="\033[1;31m"      # Fatal - Bold red
    [A]="\033[1;31m"      # Assert - Bold red
)
RESET="\033[0m"
BOLD="\033[1m"
DIM="\033[2m"

EXTRA_FILTER="${1:-}"
FILTER="flutter|python|Error|Exception|Traceback"
[[ -n "$EXTRA_FILTER" ]] && FILTER="$FILTER|$EXTRA_FILTER"

get_package() {
    adb shell dumpsys activity activities 2>/dev/null | \
        grep -E "mResumedActivity|mFocusedActivity" | \
        head -1 | \
        grep -oE '[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z0-9_]+)+' | \
        head -1
}

get_pid() {
    adb shell pidof "$1" 2>/dev/null | tr -d '\r\n' | awk '{print $1}'
}

# Format and colorize in Android Studio style
format_log() {
    while IFS= read -r line; do
        # Format: MM-DD HH:MM:SS.mmm PID TID LEVEL TAG: MESSAGE
        # Regex to extract components
        if [[ "$line" =~ ^([0-9]{2}-[0-9]{2})\ ([0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]+)\ +([0-9]+)\ +([0-9]+)\ ([VDIWEFA])\ ([^:]+):\ (.*)$ ]]; then
            date="${BASH_REMATCH[1]}"
            time="${BASH_REMATCH[2]}"
            pid="${BASH_REMATCH[3]}"
            tid="${BASH_REMATCH[4]}"
            level="${BASH_REMATCH[5]}"
            tag="${BASH_REMATCH[6]}"
            msg="${BASH_REMATCH[7]}"

            # Color based on level
            color="${COLORS[$level]:-$RESET}"

            # Format: TIME PID-TID/TAG LEVEL: MESSAGE
            printf "${DIM}%s${RESET} ${DIM}%5s-%-5s${RESET} ${color}%-20s %s: %s${RESET}\n" \
                "$time" "$pid" "$tid" "$tag" "$level" "$msg"
        else
            # Unformatted line (continuation or different format)
            echo -e "${DIM}$line${RESET}"
        fi
    done
}

print_header() {
    local pkg=$1
    local pid=$2
    echo ""
    echo -e "${BOLD}━━━ $pkg ${DIM}PID: ${pid:-?}${RESET}"
    echo ""
}

cleanup() {
    echo ""
    echo -e "${DIM}Stopped${RESET}"
    pkill -P $$ 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Initial header
clear
echo -e "${BOLD}Logcat${RESET} ${DIM}| Flet/Flutter${RESET}"
echo ""
echo -e "${DIM}Usage: ./flet_log.sh [extra_filter]${RESET}"
echo -e "${DIM}Example: ./flet_log.sh \"OneSignal|Firebase\"${RESET}"
echo ""
echo -e "${DIM}Default filter: flutter, python, Error, Exception, Traceback${RESET}"
[[ -n "$EXTRA_FILTER" ]] && echo -e "${DIM}Extra filter: $EXTRA_FILTER${RESET}"
echo -e "${DIM}Press Ctrl+C to exit${RESET}"

CURRENT_PKG=""
CURRENT_PID=""

while true; do
    PKG=$(get_package)

    [[ -z "$PKG" ]] && { sleep 1; continue; }

    PID=$(get_pid "$PKG")

    if [[ "$PKG" != "$CURRENT_PKG" || "$PID" != "$CURRENT_PID" ]]; then
        pkill -P $$ -f "adb logcat" 2>/dev/null
        sleep 0.2

        CURRENT_PKG="$PKG"
        CURRENT_PID="$PID"

        print_header "$PKG" "$PID"
        adb logcat -c 2>/dev/null

        if [[ -n "$PID" ]]; then
            adb logcat --pid="$PID" -v threadtime 2>/dev/null | \
                grep -E --line-buffered -i "$FILTER" | \
                format_log &
        else
            adb logcat -v threadtime 2>/dev/null | \
                grep -E --line-buffered -i "$PKG|$FILTER" | \
                format_log &
        fi
    fi

    sleep 1
done