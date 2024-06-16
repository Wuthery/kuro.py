"""Game announcement models."""

import pydantic

from kuro.models import base

__all__ = [
    "KuroBBSAnnouncementDetails",
    "KuroBBSAnnouncementListItem",
    "KuroBBSAnnouncementResult",
]


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
