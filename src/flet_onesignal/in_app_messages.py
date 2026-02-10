"""
OneSignal In-App Messages module for flet-onesignal.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flet_onesignal.onesignal import OneSignal


class OneSignalInAppMessages:
    """
    OneSignal In-App Messages namespace.

    Provides methods for managing in-app message triggers, pausing,
    and lifecycle events.
    """

    def __init__(self, service: "OneSignal"):
        self._service = service

    # -------------------------------------------------------------------------
    # Triggers
    # -------------------------------------------------------------------------

    async def add_trigger(self, key: str, value: str) -> None:
        """
        Add a trigger that may cause an in-app message to display.

        Args:
            key: The trigger key.
            value: The trigger value.
        """
        await self._service._invoke_method(
            "iam_add_trigger",
            {"key": key, "value": value},
        )

    async def add_triggers(self, triggers: dict[str, str]) -> None:
        """
        Add multiple triggers.

        Args:
            triggers: A dictionary of trigger key-value pairs.
        """
        await self._service._invoke_method(
            "iam_add_triggers",
            {"triggers": triggers},
        )

    async def remove_trigger(self, key: str) -> None:
        """
        Remove a trigger.

        Args:
            key: The trigger key to remove.
        """
        await self._service._invoke_method(
            "iam_remove_trigger",
            {"key": key},
        )

    async def remove_triggers(self, keys: list[str]) -> None:
        """
        Remove multiple triggers.

        Args:
            keys: A list of trigger keys to remove.
        """
        await self._service._invoke_method(
            "iam_remove_triggers",
            {"keys": keys},
        )

    async def clear_triggers(self) -> None:
        """
        Clear all triggers.
        """
        await self._service._invoke_method("iam_clear_triggers")

    # -------------------------------------------------------------------------
    # Pause Control
    # -------------------------------------------------------------------------

    async def set_paused(self, paused: bool) -> None:
        """
        Pause or unpause in-app messages.

        When paused, in-app messages will not be displayed even if triggers
        are met. Messages will be displayed when unpaused if triggers are
        still active.

        Args:
            paused: True to pause, False to unpause.
        """
        await self._service._invoke_method(
            "iam_set_paused",
            {"paused": paused},
        )

    async def is_paused(self, timeout: float = 25) -> bool:
        """
        Check if in-app messages are currently paused.

        Returns:
            True if paused, False otherwise.
        """
        result = await self._service._invoke_method(
            "iam_is_paused",
            timeout=timeout,
        )
        return result == "true"

    # Convenience methods for pause control
    async def pause(self) -> None:
        """
        Pause in-app messages.
        """
        await self.set_paused(True)

    async def resume(self) -> None:
        """
        Resume in-app messages.
        """
        await self.set_paused(False)
