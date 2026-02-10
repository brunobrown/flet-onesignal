"""
OneSignal Session module for flet-onesignal.
"""

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from flet_onesignal.onesignal import OneSignal


class OneSignalSession:
    """
    OneSignal Session namespace.

    Provides methods for tracking outcomes and session-related analytics.
    """

    def __init__(self, service: "OneSignal"):
        self._service = service

    async def add_outcome(self, name: str) -> None:
        """
        Add an outcome event.

        Outcomes are used to track user actions that result from a notification
        or in-app message.

        Args:
            name: The outcome name.
        """
        await self._service._invoke_method(
            "session_add_outcome",
            {"name": name},
        )

    async def add_unique_outcome(self, name: str) -> None:
        """
        Add a unique outcome event.

        Unique outcomes are only counted once per notification or in-app message
        that influenced the user.

        Args:
            name: The outcome name.
        """
        await self._service._invoke_method(
            "session_add_unique_outcome",
            {"name": name},
        )

    async def add_outcome_with_value(self, name: str, value: Union[int, float]) -> None:
        """
        Add an outcome event with a numeric value.

        This is useful for tracking monetary values or quantities associated
        with user actions.

        Args:
            name: The outcome name.
            value: The numeric value to associate with the outcome.
        """
        await self._service._invoke_method(
            "session_add_outcome_with_value",
            {"name": name, "value": value},
        )
