"""Announcement models."""

import pydantic

from kuro.models import base

from typing import List

__all__ = ["AnnouncementResult", "AnnouncementLangComponent", "GameAnnouncement"]


class AnnouncementLangComponent(base.APIModel):
    """Languages for componenets"""

    zh_hans: str = pydantic.Field(alias='zh-Hans')
    zh_hant: str = pydantic.Field(alias='zh-Hant')
    en: str
    ja: str
    ko: str
    fr: str
    de: str
    es: str


class AnnouncementRecord(base.APIModel):
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

    for deconstruction 
    https://discord.com/channels/1242463166592585871/1242652304168190026/1250356292946624612
    """
    # FIX:confirm waht whitelist does

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
    title: AnnouncementLangComponent = pydantic.Field(alias="tabTitle")
    """Title of announcement."""
    banner: AnnouncementLangComponent = pydantic.Field(alias="tabBanner")
    """Banner of announcement."""


class AnnouncementResult(base.APIModel):
    """Full Announcement page model."""

    game: List[AnnouncementRecord]
    """Game Announcement."""
    event: List[AnnouncementRecord] = pydantic.Field(alias="game")
    """Event Announcement"""
