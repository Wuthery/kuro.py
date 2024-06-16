"""Component for kurobbs announcement pages."""

from __future__ import annotations

from kuro import errors, models
from kuro.client import routes
from kuro.client.components import base

__all__ = ["KurobbsAnnouncementClient"]


class KurobbsAnnouncementClient(base.BaseClient):
    """Kurobbs Announcement Client."""

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
