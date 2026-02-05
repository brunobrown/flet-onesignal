"""
Entry point for running flet-onesignal as a module.

Usage:
    python -m flet_onesignal build apk
    python -m flet_onesignal build aab

    # Or use the fos-build command directly:
    fos-build apk
    fos-build aab
"""

import sys

from flet_onesignal.build import main

if __name__ == "__main__":
    # Remove 'build' from args if present (for `python -m flet_onesignal build apk`)
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        sys.argv.pop(1)
    main()
