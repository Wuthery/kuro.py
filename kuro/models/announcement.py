"""Announcement models."""

import re

import pydantic

from kuro import types
from kuro.models import base

__all__ = [
    "AnnouncementDetails",
    "AnnouncementRecord",
    "AnnouncementResult",
    "KuroBBSAnnouncementDetails",
    "KuroBBSAnnouncementListItem",
    "KuroBBSAnnouncementResult",
    "LauncherAnnouncementDetails",
    "LauncherAnnouncementGroup",
    "LauncherAnnouncementInner",
    "LauncherAnnouncementItem",
    "LauncherAnnouncementList",
    "LauncherSlideshowItem",
    "LocalisedAssetsMap",
    "LocalisedTextMap",
]


class AnnouncementDetails(base.APIModel):
    """Announcement Details."""

    announcement_id: str = pydantic.Field(alias="noticeId")
    html_content: str = pydantic.Field(alias="textContent")
    title: str = pydantic.Field(alias="textTitle")
    banner: str


class LocalisedAssetsMap(base.APIModel):
    """Languages for asset fields."""

    zh_hans: list[str] = pydantic.Field(alias="zh-Hans")
    zh_hant: list[str] = pydantic.Field(alias="zh-Hant")
    en: list[str]
    ja: list[str]
    ko: list[str]
    fr: list[str]
    de: list[str]
    es: list[str]


class LocalisedTextMap(base.APIModel):
    """Languages for text fields."""

    zh_hans: str = pydantic.Field(alias="zh-Hans")
    zh_hant: str = pydantic.Field(alias="zh-Hant")
    en: str
    ja: str
    ko: str
    fr: str
    de: str
    es: str


class AnnouncementRecord(base.APIModel):
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
    title: LocalisedTextMap = pydantic.Field(alias="tabTitle")
    """Title of announcement."""
    banner: LocalisedAssetsMap = pydantic.Field(alias="tabBanner")
    """Banner of announcement."""

    @pydantic.field_validator("details_url", mode="before")
    @classmethod
    def __details_cast(cls, v: list[str]) -> str:
        return "".join(str(item) for item in v)


class AnnouncementResult(base.APIModel):
    """Full Announcement page model."""

    game: list[AnnouncementRecord]
    """Game Announcement."""
    event: list[AnnouncementRecord] = pydantic.Field(alias="activity")
    """Event Announcement"""


class KuroBBSAnnouncementListItem(base.APIModel):
    """KuroBBS response list item."""

    cover_url: str = pydantic.Field(alias="coverUrl")
    """Banner image."""
    event_type: int = pydantic.Field(alias="eventType")
    """Event type."""
    first_publish_time: int = pydantic.Field(alias="firstPublishTime")
    """Unix publish time."""
    game_id: int = pydantic.Field(alias="gameId")
    """Game Id."""
    internal_id: str = pydantic.Field(alias="id")
    """Announcement post internal id, not particularly useful."""
    post_id: str = pydantic.Field(alias="postId")
    """Announcement post id."""
    post_title: str = pydantic.Field(alias="postTitle")
    """Announcement Post title."""
    publish_time: int = pydantic.Field(alias="publishTime")
    """Unix Publish time."""
    shelve_time: int = pydantic.Field(alias="shelveTime")
    """When to stop showing time."""


class KuroBBSAnnouncementResult(base.APIModel):
    """Full KuroBBS official post response.

    You can't actually select pages the only thing
    you can do is increase amount of posts
    """

    end_row: str = pydantic.Field(alias="endRow")
    """Amount of posts returned."""
    has_next_page: bool = pydantic.Field(alias="hasNextPage")
    """Does this page have more pages next."""
    has_previous_page: bool = pydantic.Field(alias="hasPreviousPage")
    """Does this page have more pages previous."""
    is_first_page: bool = pydantic.Field(alias="isFirstPage")
    """Is this page first page."""
    is_last_page: bool = pydantic.Field(alias="isLastPage")
    """Is this page last page."""
    post_list: list[KuroBBSAnnouncementListItem] = pydantic.Field(alias="list")
    """Announcement post List."""
    navigate_first_page: int = pydantic.Field(alias="navigateFirstPage")
    """First page number."""
    navigate_last_page: int = pydantic.Field(alias="navigateLastPage")
    """Last page number."""
    navigate_pages: int = pydantic.Field(alias="navigatePages")
    """Amount of pages."""
    navigatepage_nums: list[int] = pydantic.Field(alias="navigatepageNums")
    """Page number list."""
    next_page: int = pydantic.Field(alias="nextPage")
    """Next page."""
    page_num: int = pydantic.Field(alias="pageNum")
    """Current page number."""
    page_size: int = pydantic.Field(alias="pageSize")
    """Amount of pages."""
    pages: int
    """Amount of posts total."""
    pre_page: int = pydantic.Field(alias="prePage")
    """Pre page."""
    size: int
    """Amount of pages."""
    start_row: str = pydantic.Field(alias="startRow")
    """Start row."""
    total: str
    """Total Pages."""


class KuroBBSAnnouncementDetails(base.APIModel):
    """KuroBBS announcement post details."""

    content_type: int = pydantic.Field(alias="contentType")
    """Content type, 2 for text, 1 for image."""
    img_height: int = pydantic.Field(alias="imgHeight")
    """Image height."""
    img_width: int = pydantic.Field(alias="imgWidth")
    """Image width."""
    url: str | None = None
    """Image url."""
    content: str | None = None
    """Text."""


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
