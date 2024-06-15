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

        # Using id
        for announcement in game_announcement_list:
            print((await client.get_game_announcement_details(announcement.id)).title)

        # or
        # Using url
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

    async def get_kurobbs_announcements(
        self,
        amount_posts: int | None = 8,
    ) -> models.KuroBBSAnnouncementResult:
        """Get KuroBBS announcement list.

        ### Example:
        ```python
        announcementid_list = await client.get_kurobbs_announcements(self, 100)
        ```
        ### Args:
            amount_pages: amount of pages to return

        ### Returns:
            KuroBBS official announcements list
        """
        data = {"gameId": 3, "pageSize": amount_posts}
        rsp = await self.request(
            routes.KUROBBS_ANNOUNCEMENT_LIST.get_url(), method="POST", data=data
        )

        if not rsp["success"]:
            errors.raise_from_data(rsp)

        return models.KuroBBSAnnouncementResult(**rsp["data"])

    # FIX: endpont doesnt work for me need someone to make it work
    # async def get_kurobbs_announcement_details(self, announcement_id) -> models.KuroBB:
    #     """Get KuroBBS announcement item.
    #
    #     announcement_list = await client.get_kurobbs_announcements(self, 100)
    #     announcement_id = announcement_list.post_list[0].post_id
    #
    #     kur_announcement_details
    #
    #
    #     """

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
