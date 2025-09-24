"""Launcher announcement models."""

import re
import typing

import pydantic

from kuro import types
from kuro.models import base

__all__ = [
    "LauncherAnnouncement",
    "LauncherAnnouncementDetails",
    "LauncherAnnouncementGroup",
    "LauncherAnnouncementInner",
    "LauncherAnnouncementList",
    "LauncherSlideshowItem",
]


class LauncherAnnouncement(base.APIModel):
    """Launcher announcement item."""

    content: str
    """Launcher box content."""
    jump_url: str
    """Link to details."""
    time: str
    """Date in days of release."""

    @property
    def id(self) -> int:
        """Announcement Id."""
        parts = self.jump_url.split("/")
        post_id = parts[-1] if len(parts) > 0 else None
        assert post_id is not None, "Failed to extract ID from jump URL"
        return int(post_id)

    @property
    def lang(self) -> types.Lang:
        """Announcement language."""
        m = re.search(r"/(\w+)/main/news", self.jump_url)
        assert m is not None, "Failed to extract url from jump URL"
        return types.Lang(m.group(1))


class LauncherAnnouncementGroup(base.APIModel):
    """Launcher announcement group."""

    contents: typing.Sequence[LauncherAnnouncement]
    """List of announcements."""
    title: str
    """Group title."""


class LauncherAnnouncementInner(base.APIModel):
    """Launcher announcement inner group."""

    activity: LauncherAnnouncementGroup
    """Activity section."""
    description: str = pydantic.Field(alias="desc")
    """Description."""
    news: LauncherAnnouncementGroup
    """News section."""
    notice: LauncherAnnouncementGroup
    """Notice section."""


class LauncherSlideshowItem(base.APIModel):
    """Launcher slideshow item."""

    jump_url: str
    """Slideshow."""
    md5: str
    """md5 hash."""
    url: str
    """Slideshow picture url."""


class LauncherAnnouncementList(base.APIModel):
    """Launcher announcement list."""

    guidance: LauncherAnnouncementInner
    """Launcher Announcement Inner grouping."""
    slideshow: typing.Sequence[LauncherSlideshowItem]
    """Slideshow list."""


class LauncherAnnouncementDetails(base.APIModel):
    """Launcher announcement content."""

    article_content: str
    """html response"""
    article_id: int
    """Article id"""
    article_title: str
    """Article title"""
    article_type: int
    """Article type"""
    article_type_name: str
    """Article type name"""
    game_id: str
    """Game id"""
    start_time: str
    """ISO 8601 timestamp for when not to start showing article"""
    end_time: str | None = None
    """ISO 8601 timestamp for when not to show article"""

    @property
    def game(self) -> types.Game:
        """Game type."""
        return types.Game(self.game_id)
