"""Component for all announcement pages."""

from __future__ import annotations

import yarl

from kuro import errors, models, types
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
        if rsp["code"] != 0:
            errors.raise_from_data(rsp)

        return models.AnnouncementResult(**rsp)

    async def get_game_announcement_details(
        self, announcement_id: str, lang: types.Lang | None, url: str
    ) -> models.AnnouncementDetails:
        """Get game announcement details.

        Can give either id or url from game_announcements

        ### Example:
        ```python
        for announcement in await client.get_game_announcements().game:
            print(get_game_announcement_details(announcement.id).title)
        # or
        for announcement in await client.get_game_announcements().game:
            print(await client.get_game_announcement_details(announcement.url).title)

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
            rsp = await self.request(yarl.URL(f"{url}/{lang}.json"), method="GET")
        else:
            rsp = await self.request(
                routes.GAME_ANNOUNCEMENT_DETAILS.get_url().with_path(
                    f"{announcement_id}/{lang}.json"
                ),
                method="GET",
            )

        if rsp["code"] != 0:
            errors.raise_from_data(rsp)

        return models.AnnouncementDetails(**rsp)
