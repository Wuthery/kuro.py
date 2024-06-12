"""Announcement models."""

import pydantic

from kuro.models import base

from typing import List

__all__ = ["AnnouncementResult", "LocalizedAssetsMap", "LocalizedtextMap"]


class LocalizedAssetsMap(base.APIModel):
    """Languages for componenets"""

    zh_hans: List[str] = pydantic.Field(alias='zh-Hans')
    zh_hant: List[str] = pydantic.Field(alias='zh-Hant')
    en: List[str]
    ja: List[str]
    ko: List[str]
    fr: List[str]
    de: List[str]
    es: List[str]


class LocalizedtextMap(base.APIModel):
    """Game Announcement model.
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
    this is all for whether the announcement should be shown on webview

    for deconstruction 
    https://discord.com/channels/1242463166592585871/1242652304168190026/1250356292946624612
    """

    details_url: str = pydantic.Field(alias="contentPrefix")
    """Url for announcement details."""
    red: int
    """Should announcement be processed.""" # needs more checking
    permanent: int
    """Permanant announcement."""
    id: str
    """Announcement id."""
    start_time_ms: int = pydantic.Field(alias="startTimeMs")
    """Unix start time stamp."""
    end_time_ms: int = pydantic.Field(alias="endTimeMs")
    """Unix end time stamp."""
    platform: List[int]
    """Platform for announcement to show on."""
    channel: List
    """If channel doesnt exist then show."""
    white_list: List = pydantic.Field(alias="whiteList")
    """if whitelist is empty then show if permanent."""
    title: LocalizedAssetsMap = pydantic.Field(alias="tabTitle")
    """Title of announcement."""
    banner: LocalizedAssetsMap = pydantic.Field(alias="tabBanner")
    """Banner of announcement."""


class AnnouncementResult(base.APIModel):
    """Full Announcement page model."""

    game: List[LocalizedtextMap]
    """Game Announcement."""
    event: List[LocalizedtextMap] = pydantic.Field(alias="game")
    """Event Announcement"""
