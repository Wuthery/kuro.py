"""Component for all announcement pages."""

from __future__ import annotations

import yarl

from kuro import models, types
from kuro.client import routes
from kuro.client.components import base

__all__ = ["AnnouncementClient"]


class AnnouncementClient(base.BaseClient):
    """Announcement Client."""

    async def get_game_announcements(self) -> models.AnnouncementResult:
        """Get game announcements.

        ### Returns:
            Game Announcements.
        """
        rsp = await self.request(routes.GAME_ANNOUNCEMENTS.get_url(), method="GET")

        return models.AnnouncementResult(**rsp)

    async def get_game_announcement_details(
        self,
        announcement_id: str | None = None,
        lang: types.Lang | None = None,
        url: str | None = None,
    ) -> models.AnnouncementDetails:
        """Get game announcement details.

        Can give either id or url from game_announcements

        ### Example:
        ```python
        game_announcement_list = (await client.get_game_announcements()).game

        for announcement in game_announcement_list:
            print((await client.get_game_announcement_details(announcement.id)).title)
        # or
        for announcement in game_announcement_list:
            print((await client.get_game_announcement_details(announcement.url)).title)
        ```

        ### Args:
            id: Announcement Id - from get_game_announcements
            url: Announcement irl - form get_game_announcements

        ### Returns:
            Game Announceent Details.
        """
        if lang is None:
            lang = self.lang

        rsp = None
        if url:
            rsp = await self.request(yarl.URL(f"{url}/{lang.value}.json"), method="GET")
        else:
            rsp = await self.request(
                routes.GAME_ANNOUNCEMENT_DETAILS.get_url() / f"{announcement_id}/{lang.value}.json",
                method="GET",
            )

        return models.AnnouncementDetails(**rsp)
