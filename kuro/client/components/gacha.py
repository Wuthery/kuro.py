"""Auth component responsible for authentication."""

import typing

from kuro import errors, types
from kuro.client.components import base
from kuro.client.routes import GACHA_RECORD_URL
from kuro.models import GachaCharacter, GachaWeapon

__all__ = ["GachaClient"]


class GachaClient(base.BaseClient):
    """Gacha client."""

    async def get_gacha_record(
        self,
        player_id: int,
        record_id: str,
        *,
        banner: types.WuWaBanner,
        server: types.WuWaServer,
        lang: types.Lang | None = None,
    ) -> typing.Sequence[GachaWeapon | GachaCharacter]:
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
        body = {
            "playerId": str(player_id),
            "languageCode": str(lang),
            "cardPoolType": int(banner),
            "recordId": record_id,
            "serverId": str(server),
            "cardPoolId": "",
        }
        rsp = await self.request(GACHA_RECORD_URL.get_url(), method="POST", json=body)

        if rsp["code"] != 0:
            errors.raise_from_data(rsp)

        return [
            GachaWeapon(**{**record, "cardPoolType": banner})
            if record["resourceId"] >= 100000
            else GachaCharacter(**{**record, "cardPoolType": banner})
            for record in rsp["data"]
        ]
