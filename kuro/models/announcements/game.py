"""Game announcement models."""

import typing

import pydantic

from kuro.models import base

__all__ = [
    "GameAnnouncementDetails",
    "GameAnnouncementRecord",
    "GameAnnouncementResult",
    "GameLocalizedAssetsMap",
    "GameLocalizedTextMap",
]


class GameAnnouncementDetails(base.APIModel):
    """Announcement Details."""

    announcement_id: int = pydantic.Field(alias="noticeId")
    """Announcement ID."""
    html_content: str = pydantic.Field(alias="textContent")
    """HTML content."""
    title: str = pydantic.Field(alias="textTitle")
    """Announcement title."""
    banner: str
    """Banner image."""


class GameLocalizedAssetsMap(base.APIModel):
    """Languages for asset fields."""

    zh_hans: typing.Sequence[str] | None = pydantic.Field(alias="zh-Hans", default=None)
    """Chinese Simplified."""
    zh_hant: typing.Sequence[str] | None = pydantic.Field(alias="zh-Hant", default=None)
    """Chinese Traditional."""
    en: typing.Sequence[str] | None = None
    """English."""
    ja: typing.Sequence[str] | None = None
    """Japanese."""
    ko: typing.Sequence[str] | None = None
    """Korean."""
    fr: typing.Sequence[str] | None = None
    """French."""
    de: typing.Sequence[str] | None = None
    """German."""
    es: typing.Sequence[str] | None = None
    """Spanish."""


class GameLocalizedTextMap(base.APIModel):
    """Languages for text fields."""

    zh_hans: str | None = pydantic.Field(alias="zh-Hans", default=None)
    """Chinese Simplified."""
    zh_hant: str | None = pydantic.Field(alias="zh-Hant", default=None)
    """Chinese Traditional."""
    en: str | None = None
    """English."""
    ja: str | None = None
    """Japanese."""
    ko: str | None = None
    """Korean."""
    fr: str | None = None
    """French."""
    de: str | None = None
    """German."""
    es: str | None = None
    """Spanish."""


class GameAnnouncementRecord(base.APIModel):
    """Game announcement record model.

    `red`, `channel`, `platform`, `whitelist` are used to determine
    whether the announcement should be shown on webview.

    See [this message](https://discord.com/channels/1242463166592585871/1242652304168190026/1250356292946624612)
    for more details.
    """

    details_url: str = pydantic.Field(alias="contentPrefix")
    """Url for announcement details."""
    red: int
    """Should announcement be processed."""  # needs more checking
    permanent: int
    """Permanent announcement."""
    id: str
    """Announcement id."""
    start_time_ms: int
    """Unix start time stamp."""
    end_time_ms: int
    """Unix end time stamp."""
    platform: typing.Sequence[int]
    """Platform for announcement to show on."""
    channel: typing.Sequence[typing.Any]
    """If channel doesn't exist then show."""
    white_list: typing.Sequence[typing.Any]
    """If whitelist is empty then show if permanent."""
    title: GameLocalizedTextMap = pydantic.Field(alias="tabTitle")
    """Title of announcement."""
    banner: GameLocalizedAssetsMap = pydantic.Field(alias="tabBanner")
    """Banner of announcement."""

    @pydantic.field_validator("details_url", mode="before")
    @classmethod
    def __cast_details(cls, v: typing.Sequence[str]) -> str:  # type: ignore
        return "".join(str(item) for item in v)


class GameAnnouncementResult(base.APIModel):
    """Full Announcement page model."""

    game: typing.Sequence[GameAnnouncementRecord]
    """Game Announcement."""
    event: typing.Sequence[GameAnnouncementRecord] = pydantic.Field(alias="activity")
    """Event Announcement"""
