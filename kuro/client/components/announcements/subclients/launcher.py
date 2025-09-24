"""Component for launcher announcements."""

from __future__ import annotations

from kuro import models, types
from kuro.client import decorators, routes
from kuro.client.components import base

__all__ = ["LauncherAnnouncementClient"]


class LauncherAnnouncementClient(base.BaseClient):
    """Launcher Announcement Client."""

    async def get_launcher_announcements(self) -> models.LauncherAnnouncementList:
        """Get launcher announcement list.

        ### Example:
        ```python
        launcher_announcements = await client.get_launcher_announcements()
        print(launcher_announcements.guidance.activity.contents[0].content)
        ```

        ### Returns:
            Launcher official announcements list
        """
        url = routes.LAUNCHER_ANNOUNCEMENT_LIST.get_url(self.region)
        if self.region is types.Region.OVERSEAS:
            url /= f"{self.lang.value}.json"

        rsp = await self.request(url)

        return models.LauncherAnnouncementList(**rsp)

    @decorators.region_specific(types.Region.OVERSEAS)
    async def get_launcher_announcement_details(
        self, announcement_id: int
    ) -> models.LauncherAnnouncementDetails:
        """Get Launcher official announcement details.

        ### Example:
        ```python
            launcher_announcements = await client.get_launcher_announcements()

            id = launcher_announcements.guidance.activity.contents[0].id
            lang = launcher_announcements.guidance.activity.contents[0].lang

            details = await client.get_launcher_announcement_details(id, lang)
            print(details.article_title)
        ```

        ### Args:
            announcement_id: ID of the announcement to get details for

        ### Returns:
            Launcher announcement details
        """
        url = routes.LAUNCHER_ANNOUNCEMENT_DETAILS.get_url()
        rsp = await self.request(url / f"{self.lang.value}/article/{announcement_id}.json")

        return models.LauncherAnnouncementDetails(**rsp)
