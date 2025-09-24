"""Component used to fetch gacha records."""

import typing

from kuro import errors, models, types
from kuro.client import decorators, routes
from kuro.client.components import base

__all__ = ["GachaClient"]


class GachaClient(base.BaseClient):
    """Gacha client."""

    @decorators.region_specific(types.Region.OVERSEAS)
    async def get_gacha_record(
        self,
        player_id: int,
        record_id: str,
        *,
        banner: types.WuWaBanner,
        server: types.WuWaServer,
        lang: types.Lang | None = None,
    ) -> typing.Sequence[models.GachaWeapon | models.GachaCharacter]:
        """Get gacha records.

        ### Example:
        ```python
        url = "..."
        parsed = parse_gacha_url(url)
        result = await client.get_gacha_record(**parsed)
        ```

        ### Args:
            player_id: Player ID.
            record_id: Record ID (unique for each player).
            banner: Banner you want to get record for.
            server: Game server.
            lang: Language.

        ### Returns:
            Sequence of gacha records.
        """
        body: dict[str, typing.Any] = {
            "playerId": str(player_id),
            "languageCode": lang.value if lang else self.lang.value,
            "cardPoolType": int(banner),
            "recordId": record_id,
            "serverId": server.value,
            "cardPoolId": "",
        }
        rsp = await self.request(routes.GACHA_RECORD.get_url(), method="POST", json=body)

        if rsp["code"] != 0:
            errors.raise_from_data(rsp)

        return [
            models.GachaWeapon(banner=banner, **record)
            if record["resourceId"] >= 100000
            else models.GachaCharacter(banner=banner, **record)
            for record in rsp["data"]
        ]
