"""Component for game announcements."""

from __future__ import annotations

from kuro import models
from kuro.client import routes
from kuro.client.components import base

__all__ = ["GameAnnouncementClient"]


class GameAnnouncementClient(base.BaseClient):
    """Announcement Client."""

    async def get_game_announcements(self) -> models.GameAnnouncementResult:
        """Get game announcements.

        ### Returns:
            Game Announcements.
        """
        rsp = await self.request(routes.GAME_ANNOUNCEMENTS.get_url(self.region))

        return models.GameAnnouncementResult(**rsp)

    async def get_game_announcement_details(
        self, announcement_id: str
    ) -> models.GameAnnouncementDetails:
        """Get game announcement details.

        Can give either id or url from game_announcements

        ### Example:
        ```python
        announcement_list = await client.get_game_announcements()

        for announcement in announcement_list.game:
            details = await client.get_game_announcement_details(announcement.id)
            print(details.title)
        ```

        ### Args:
            id: ID of the announcement to get details for

        ### Returns:
            Game announcement details.
        """
        rsp = await self.request(
            routes.GAME_ANNOUNCEMENT_DETAILS.get_url(self.region)
            / f"{announcement_id}/{self.lang.value}.json"
        )

        return models.GameAnnouncementDetails(**rsp)
