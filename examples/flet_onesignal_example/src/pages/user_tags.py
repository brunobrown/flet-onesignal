"""
User Tags page - Segment users with custom tags.
"""

import flet as ft
from components.log_viewer import LogViewer
from components.page_layout import PageLayout
from context import AppCtx


@ft.component
def UserTagsPage():
    """
    Page for managing user tags.

    Tags allow segmenting users for targeted notifications.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    onesignal = ctx.onesignal

    # Local state
    tag_key, set_tag_key = ft.use_state("")
    tag_value, set_tag_value = ft.use_state("")
    tags_json, set_tags_json = ft.use_state("")

    async def handle_add_tag(e):
        if not tag_key or not tag_value:
            state.add_log("Enter key and value for the tag", "warning")
            return
        try:
            await onesignal.user.add_tag(tag_key, tag_value)
            state.add_log(f"Tag added: {tag_key}={tag_value}", "success")
        except Exception as ex:
            state.add_log(f"Error adding tag: {ex}", "error")

    async def handle_add_tags(e):
        if not tags_json:
            state.add_log("Enter tags in JSON format", "warning")
            return
        try:
            import json

            tags = json.loads(tags_json)
            await onesignal.user.add_tags(tags)
            state.add_log(f"Tags added: {tags}", "success")
        except Exception as ex:
            state.add_log(f"Error adding tags: {ex}", "error")

    async def handle_remove_tag(e):
        if not tag_key:
            state.add_log("Enter the tag key to remove", "warning")
            return
        try:
            await onesignal.user.remove_tag(tag_key)
            state.add_log(f"Tag removed: {tag_key}", "success")
        except Exception as ex:
            state.add_log(f"Error removing tag: {ex}", "error")

    async def handle_remove_tags(e):
        if not tag_key:
            state.add_log("Enter keys separated by comma", "warning")
            return
        try:
            keys = [k.strip() for k in tag_key.split(",")]
            await onesignal.user.remove_tags(keys)
            state.add_log(f"Tags removed: {keys}", "success")
        except Exception as ex:
            state.add_log(f"Error removing tags: {ex}", "error")

    async def handle_get_tags(e):
        try:
            tags = await onesignal.user.get_tags()
            state.add_log(f"Current tags: {tags}", "success")
        except Exception as ex:
            state.add_log(f"Error getting tags: {ex}", "error")

    return PageLayout(
        title="User - Tags",
        description=(
            "Tags allow segmenting users to send targeted notifications. "
            "Use tags to categorize users by preferences, behavior, "
            "subscription level, or any custom attribute. "
            "You can then create segments in the OneSignal dashboard based on these tags."
        ),
        code_example="""# Add a single tag
await onesignal.user.add_tag("plan", "premium")

# Add multiple tags
await onesignal.user.add_tags({
    "plan": "premium",
    "level": "5",
    "preference": "sports"
})

# Remove a tag
await onesignal.user.remove_tag("plan")

# Get all tags
tags = await onesignal.user.get_tags()""",
        children=[
            ft.Text("Single Tag", weight=ft.FontWeight.W_500),
            ft.Row(
                [
                    ft.TextField(
                        label="Key",
                        hint_text="E.g.: plan",
                        value=tag_key,
                        on_change=lambda e: set_tag_key(e.control.value),
                        width=150,
                    ),
                    ft.TextField(
                        label="Value",
                        hint_text="E.g.: premium",
                        value=tag_value,
                        on_change=lambda e: set_tag_value(e.control.value),
                        width=150,
                    ),
                ],
                spacing=10,
            ),
            ft.Row(
                [
                    ft.FilledButton("Add", icon=ft.Icons.ADD, on_click=handle_add_tag),
                    ft.OutlinedButton("Remove", icon=ft.Icons.REMOVE, on_click=handle_remove_tag),
                    ft.OutlinedButton("Remove Multiple", on_click=handle_remove_tags),
                ],
                spacing=10,
                wrap=True,
            ),
            ft.Divider(height=10),
            ft.Text("Multiple Tags (JSON)", weight=ft.FontWeight.W_500),
            ft.TextField(
                label="Tags JSON",
                hint_text='{"key1": "value1", "key2": "value2"}',
                value=tags_json,
                on_change=lambda e: set_tags_json(e.control.value),
                multiline=True,
                min_lines=2,
                max_lines=4,
            ),
            ft.Row(
                [
                    ft.FilledButton("Add Tags", on_click=handle_add_tags),
                    ft.OutlinedButton("Get All", icon=ft.Icons.LIST, on_click=handle_get_tags),
                ],
                spacing=10,
            ),
            ft.Divider(height=20),
            LogViewer(),
        ],
    )
