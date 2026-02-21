"""OneSignal REST API client for sending push notifications."""

import asyncio
import json
import urllib.request


def _send_push_sync(
    app_id: str,
    rest_api_key: str,
    onesignal_id: str,
    title: str,
    body: str,
) -> dict:
    url = "https://api.onesignal.com/notifications"
    payload = json.dumps(
        {
            "app_id": app_id,
            "target_channel": "push",
            "include_aliases": {"onesignal_id": [onesignal_id]},
            "contents": {"en": body},
            "headings": {"en": title},
        }
    ).encode()

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Key {rest_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


async def send_push_notification(
    app_id: str,
    rest_api_key: str,
    onesignal_id: str,
    title: str = "Test Push",
    body: str = "Automated test notification",
) -> dict:
    return await asyncio.to_thread(_send_push_sync, app_id, rest_api_key, onesignal_id, title, body)


def _delete_alias_sync(
    app_id: str,
    rest_api_key: str,
    onesignal_id: str,
    alias_label: str,
) -> int:
    url = (
        f"https://api.onesignal.com/apps/{app_id}"
        f"/users/by/onesignal_id/{onesignal_id}/identity/{alias_label}"
    )
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Key {rest_api_key}",
            "Content-Type": "application/json",
        },
        method="DELETE",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.status


async def delete_alias(
    app_id: str,
    rest_api_key: str,
    onesignal_id: str,
    alias_label: str,
) -> int:
    """Delete an alias via REST API (requires server-side auth)."""
    return await asyncio.to_thread(
        _delete_alias_sync, app_id, rest_api_key, onesignal_id, alias_label
    )
