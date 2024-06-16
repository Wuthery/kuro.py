"""Launcher announcement models."""

import re

import pydantic

from kuro import types
from kuro.models import base

__all__ = [
    "LauncherAnnouncementDetails",
    "LauncherAnnouncementGroup",
    "LauncherAnnouncementInner",
    "LauncherAnnouncementItem",
    "LauncherAnnouncementList",
    "LauncherSlideshowItem",
]


class LauncherAnnouncementItem(base.APIModel):
    """Launcher announcment item."""

    content: str
    """Launcher box content."""
    jump_url: str = pydantic.Field(alias="jumpUrl")
    """Link to details."""
    time: str
    """Date in days of release."""

    @property
    def id(self) -> int:
        """Announcement Id."""
        m = re.search(r"/detail/(\d+)", self.jump_url)
        assert m is not None, "Failed to extract ID from jump URL"
        return int(m.group(1))

    @property
    def lang(self) -> types.Lang:
        """Announcement language."""
        m = re.search(r"/(\w+)/main/news", self.jump_url)
        assert m is not None, "Failed to extract url from jump URL"
        return types.Lang(m.group(1))


class LauncherAnnouncementGroup(base.APIModel):
    """Launcher announcement group."""

    contents: list[LauncherAnnouncementItem]
    """List of announcements."""
    title: str
    """Group title."""


class LauncherAnnouncementInner(base.APIModel):
    """Launcher announcemnt inner group."""

    activity: LauncherAnnouncementGroup
    """Activity section."""
    desc: str
    """Description."""
    news: LauncherAnnouncementGroup
    """News section."""
    notice: LauncherAnnouncementGroup
    """Notice section."""


class LauncherSlideshowItem(base.APIModel):
    """Launcher slideshow item."""

    jump_url: str = pydantic.Field(alias="jumpUrl")
    """Slideshow."""
    md5: str
    """md5 hash."""
    url: str
    """Slideshow picture url."""


class LauncherAnnouncementList(base.APIModel):
    """Launcher announcement list."""

    guidance: LauncherAnnouncementInner
    """Launcher Announcement Inner grouping."""
    slideshow: list[LauncherSlideshowItem]
    """Slideshow list."""


class LauncherAnnouncementDetails(base.APIModel):
    """Launcher announcement content."""

    article_content: str = pydantic.Field(alias="articleContent")
    """html response"""
    article_id: int = pydantic.Field(alias="articleId")
    """Article id"""
    article_title: str = pydantic.Field(alias="articleTitle")
    """Article title"""
    article_type: int = pydantic.Field(alias="articleType")
    """Article type"""
    article_type_name: str = pydantic.Field(alias="articleTypeName")
    """Article type name"""
    end_time: str = pydantic.Field(alias="endTime")
    """ISO 8601 timestamp for when not to show article"""
    game_id: str = pydantic.Field(alias="gameId")
    """Game id"""
    start_time: str = pydantic.Field(alias="startTime")
    """ISO 8601 timestamp for when not to start showing article"""
