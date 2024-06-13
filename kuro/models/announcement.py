"""Announcement models."""

import pydantic

from kuro.models import base

__all__ = ["AnnouncementDetails", "AnnouncementResult", "LocalizedAssetsMap", "LocalizedtextMap"]


class AnnouncementDetails(base.APIModel):
    """Announcement Details."""

    announcement_id: str = pydantic.Field(alias="noticeId")
    html_content: str = pydantic.Field(alias="textContent")
    title: str = pydantic.Field(alias="textTitle")
    banner: str


class LocalizedAssetsMap(base.APIModel):
    """Languages for componenets."""

    zh_hans: list[str] = pydantic.Field(alias="zh-Hans")
    zh_hant: list[str] = pydantic.Field(alias="zh-Hant")
    en: list[str]
    ja: list[str]
    ko: list[str]
    fr: list[str]
    de: list[str]
    es: list[str]


class LocalizedtextMap(base.APIModel):
    """Game Announcement model.

    ```json
    {
    ...
      "red": 1,
      ...
      "platform": [
        1,
        2,
        3
      ],
      "channel": [],
      "whiteList": []
    }
    ```
    This is all for whether the announcement should be shown on webview, not particularly useful

    For deconstruction
    https://discord.com/channels/1242463166592585871/1242652304168190026/1250356292946624612
    """

    details_url: str = pydantic.Field(alias="contentPrefix")
    """Url for announcement details."""
    red: int
    """Should announcement be processed."""  # needs more checking
    permanent: int
    """Permanant announcement."""
    id: str
    """Announcement id."""
    start_time_ms: int = pydantic.Field(alias="startTimeMs")
    """Unix start time stamp."""
    end_time_ms: int = pydantic.Field(alias="endTimeMs")
    """Unix end time stamp."""
    platform: list[int]
    """Platform for announcement to show on."""
    channel: list
    """If channel doesnt exist then show."""
    white_list: list = pydantic.Field(alias="whiteList")
    """if whitelist is empty then show if permanent."""
    title: LocalizedAssetsMap = pydantic.Field(alias="tabTitle")
    """Title of announcement."""
    banner: LocalizedAssetsMap = pydantic.Field(alias="tabBanner")
    """Banner of announcement."""


class AnnouncementResult(base.APIModel):
    """Full Announcement page model."""

    game: list[LocalizedtextMap]
    """Game Announcement."""
    event: list[LocalizedtextMap] = pydantic.Field(alias="game")
    """Event Announcement"""
