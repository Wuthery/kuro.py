"""Component for launcher announcement pages."""

from __future__ import annotations

from kuro import models, types
from kuro.client import routes
from kuro.client.components import base

__all__ = ["LauncherAnnouncementClient"]


class LauncherAnnouncementClient(base.BaseClient):
    """Launcher Announcement Client."""

    async def get_launcher_announcements(
        self, lang: types.Lang | None = None
    ) -> models.LauncherAnnouncementList:
        """Get launcher announcement list.

        ### Example:
        ```python
        launcher_announcements = await client.get_launcher_announcements()
        print(launcher_announcements.guidance.activity.contents[0].content)
        ```
        ### Args:
            lang: Language

        ### Returns:
            Launcher official announcements list

        """
        if lang is None:
            lang = self.lang

        rsp = None

        if lang is types.Lang.CHINESE_SIMPLIFIED:
            rsp = await self.request(routes.LAUNCHER_ANNOUNCEMENT_LIST_CN.get_url(), method="GET")
        else:
            rsp = await self.request(
                routes.LAUNCHER_ANNOUNCEMENT_LIST_GLOBAL.get_url() / f"{lang.value}.json"
            )

        return models.LauncherAnnouncementList(**rsp)

    async def get_launcher_announcement_details(
        self, announcement_id: int, lang: types.Lang | None = None
    ) -> models.LauncherAnnouncementDetails:
        """Get Launcher official announcement details.

        Url required as each language has a different article id,
        so both are required to obtain the data

        ### Example:
        ```python
            launcher_announcements = await client.get_launcher_announcements()

            id = launcher_announcements.guidance.activity.contents[0].id
            lang = launcher_announcements.guidance.activity.contents[0].lang

            result = await client.get_launcher_announcement_details(id, lang)
        ```

        ### Args:
            url: url retrieved from get_launcher_announcements

        ### Returns:
            Launcher announcement details

        """
        if lang is None:
            lang = self.lang

        rsp = await self.request(
            routes.LAUNCHER_ANNOUNCEMENT_DETAILS_GLOBAL.get_url()
            / f"{lang.value}/article/{announcement_id}.json",
            method="GET",
        )

        return models.LauncherAnnouncementDetails(**rsp)
