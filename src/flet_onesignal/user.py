"""
OneSignal User module for flet-onesignal.
"""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from flet_onesignal.onesignal import OneSignal


class OneSignalUser:
    """
    OneSignal User namespace.

    Provides methods for managing user identity, tags, aliases, email, SMS, and language.
    """

    def __init__(self, service: "OneSignal"):
        self._service = service

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    async def get_onesignal_id(self, timeout: float = 25) -> Optional[str]:
        """
        Get the OneSignal ID for the current user.

        Returns:
            The OneSignal ID, or None if not available.
        """
        result = await self._service._invoke_method(
            "user_get_onesignal_id",
            timeout=timeout,
        )
        return result if result else None

    async def get_external_id(self, timeout: float = 25) -> Optional[str]:
        """
        Get the external ID for the current user.

        Returns:
            The external ID, or None if not set.
        """
        result = await self._service._invoke_method(
            "user_get_external_id",
            timeout=timeout,
        )
        return result if result else None

    # -------------------------------------------------------------------------
    # Tags
    # -------------------------------------------------------------------------

    async def add_tag(self, key: str, value: str) -> None:
        """
        Add a single tag to the current user.

        Args:
            key: The tag key.
            value: The tag value.
        """
        await self._service._invoke_method(
            "user_add_tag",
            {"key": key, "value": value},
        )

    async def add_tags(self, tags: dict[str, str]) -> None:
        """
        Add multiple tags to the current user.

        Args:
            tags: A dictionary of tag key-value pairs.
        """
        await self._service._invoke_method(
            "user_add_tags",
            {"tags": tags},
        )

    async def remove_tag(self, key: str) -> None:
        """
        Remove a single tag from the current user.

        Args:
            key: The tag key to remove.
        """
        await self._service._invoke_method(
            "user_remove_tag",
            {"key": key},
        )

    async def remove_tags(self, keys: list[str]) -> None:
        """
        Remove multiple tags from the current user.

        Args:
            keys: A list of tag keys to remove.
        """
        await self._service._invoke_method(
            "user_remove_tags",
            {"keys": keys},
        )

    async def get_tags(self, timeout: float = 25) -> dict[str, str]:
        """
        Get all tags for the current user.

        Returns:
            A dictionary of tag key-value pairs.
        """
        result = await self._service._invoke_method(
            "user_get_tags",
            timeout=timeout,
        )
        if isinstance(result, dict):
            return result
        return {}

    # -------------------------------------------------------------------------
    # Aliases
    # -------------------------------------------------------------------------

    async def add_alias(self, label: str, id: str) -> None:
        """
        Add a single alias to the current user.

        Args:
            label: The alias label.
            id: The alias ID.
        """
        await self._service._invoke_method(
            "user_add_alias",
            {"label": label, "id": id},
        )

    async def add_aliases(self, aliases: dict[str, str]) -> None:
        """
        Add multiple aliases to the current user.

        Args:
            aliases: A dictionary of alias label-ID pairs.
        """
        await self._service._invoke_method(
            "user_add_aliases",
            {"aliases": aliases},
        )

    async def remove_alias(self, label: str) -> None:
        """
        Remove a single alias from the current user.

        Args:
            label: The alias label to remove.
        """
        await self._service._invoke_method(
            "user_remove_alias",
            {"label": label},
        )

    async def remove_aliases(self, labels: list[str]) -> None:
        """
        Remove multiple aliases from the current user.

        Args:
            labels: A list of alias labels to remove.
        """
        await self._service._invoke_method(
            "user_remove_aliases",
            {"labels": labels},
        )

    # -------------------------------------------------------------------------
    # Email
    # -------------------------------------------------------------------------

    async def add_email(self, email: str) -> None:
        """
        Add an email address to the current user.

        Args:
            email: The email address to add.
        """
        await self._service._invoke_method(
            "user_add_email",
            {"email": email},
        )

    async def remove_email(self, email: str) -> None:
        """
        Remove an email address from the current user.

        Args:
            email: The email address to remove.
        """
        await self._service._invoke_method(
            "user_remove_email",
            {"email": email},
        )

    # -------------------------------------------------------------------------
    # SMS
    # -------------------------------------------------------------------------

    async def add_sms(self, phone: str) -> None:
        """
        Add an SMS number to the current user.

        Args:
            phone: The phone number to add (E.164 format recommended).
        """
        await self._service._invoke_method(
            "user_add_sms",
            {"phone": phone},
        )

    async def remove_sms(self, phone: str) -> None:
        """
        Remove an SMS number from the current user.

        Args:
            phone: The phone number to remove.
        """
        await self._service._invoke_method(
            "user_remove_sms",
            {"phone": phone},
        )

    # -------------------------------------------------------------------------
    # Language
    # -------------------------------------------------------------------------

    async def set_language(self, language_code: str) -> None:
        """
        Set the language for the current user.

        This also applies to email and SMS subscriptions.

        Args:
            language_code: The ISO 639-1 language code (e.g., "en", "pt", "es").
        """
        await self._service._invoke_method(
            "user_set_language",
            {"language": language_code},
        )

    # -------------------------------------------------------------------------
    # Push Subscription
    # -------------------------------------------------------------------------

    async def opt_in_push(self) -> None:
        """
        Opt the user in to push notifications.

        Call this to receive push notifications on the device or to resume
        receiving notifications after calling opt_out_push().
        """
        await self._service._invoke_method("user_push_opt_in")

    async def opt_out_push(self) -> None:
        """
        Opt the user out of push notifications.

        The user will stop receiving push notifications on the current device.
        """
        await self._service._invoke_method("user_push_opt_out")

    async def get_push_subscription_id(self, timeout: float = 25) -> Optional[str]:
        """
        Get the push subscription ID.

        Returns:
            The push subscription ID, or None if not available.
        """
        result = await self._service._invoke_method(
            "user_get_push_subscription_id",
            timeout=timeout,
        )
        return result if result else None

    async def get_push_subscription_token(self, timeout: float = 25) -> Optional[str]:
        """
        Get the push subscription token.

        Returns:
            The push subscription token, or None if not available.
        """
        result = await self._service._invoke_method(
            "user_get_push_subscription_token",
            timeout=timeout,
        )
        return result if result else None

    async def is_push_opted_in(self, timeout: float = 25) -> bool:
        """
        Check if the user is opted in to push notifications.

        Returns:
            True if opted in, False otherwise.
        """
        result = await self._service._invoke_method(
            "user_is_push_opted_in",
            timeout=timeout,
        )
        return result == "true"
