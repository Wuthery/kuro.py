"""Game component for fetching game data."""

import json

from kuro import errors, models, types
from kuro.client import decorators, routes
from kuro.client.components import base


class GameClient(base.BaseClient):
    """Game client."""

    @decorators.region_specific(types.Region.OVERSEAS)
    async def get_game_user(
        self, user_id: int, token: str, area: str, username: str, *, login_type: int = 1
    ) -> models.GameUser:
        """Get game user info.

        ### Args:
            user_id: User ID.
            token: Access (game) token.
            area: Area.
            username: Username.
            login_type: Login type. Default is 1.

        ### Returns:
            Game info.
        """
        params: dict[str, str | int] = {
            "loginType": login_type,
            "userId": user_id,
            "token": token,
            "area": area,
            "userName": username,
        }
        rsp = await self.request(routes.GAME_USER_INFO.get_url().with_query(params))

        if rsp["Code"] not in {0, 49}:
            errors.raise_from_data(rsp)

        return models.GameUser(**rsp)

    @decorators.region_specific(types.Region.OVERSEAS)
    async def get_player_info(
        self, oauth_code: str, *, max_attempts: int = 3
    ) -> dict[str, models.GamePlayerInfo]:
        """Get player info.

        ### Args:
            oauth_code: OAuth code obtained from generate_oauth_code.
            max_attempts: Maximum number of attempts to get player info if failed. Default is 3.

        ### Returns:
            Regions mapped to player info. Example region is "Europe".
        """
        data = {"oauthCode": oauth_code}
        rsp = await self.request(routes.LAUNCHER_PLAYER_INFO.get_url(), method="POST", json=data)

        if max_attempts > 0 and rsp["code"] == 1005:
            return await self.get_player_info(oauth_code, max_attempts=max_attempts - 1)

        if rsp["code"] != 0:
            errors.raise_from_data(rsp)

        return {
            region: models.GamePlayerInfo(**json.loads(info))
            for region, info in rsp["data"].items()
        }

    @decorators.region_specific(types.Region.OVERSEAS)
    async def get_player_role(
        self,
        oauth_code: str,
        player_id: int,
        region: str,
        *,
        max_attempts: int = 3,
    ) -> models.RoleInfo:
        """Get player role info.

        ### Args:
            oauth_code: OAuth code obtained from generate_oauth_code.
            player_id: Player UID.
            region: Player region.
            max_attempts: Maximum number of attempts to get player role if failed. Default is 3.

        ### Returns:
            Player role info.
        """
        data: dict[str, int | str] = {
            "oauthCode": oauth_code,
            "playerId": player_id,
            "region": region,
        }
        rsp = await self.request(routes.LAUNCHER_PLAYER_ROLE.get_url(), method="POST", json=data)

        if max_attempts > 0 and rsp["code"] == 1005:
            return await self.get_player_role(
                oauth_code, player_id, region, max_attempts=max_attempts - 1
            )

        if rsp["code"] != 0:
            errors.raise_from_data(rsp)

        json_data = json.loads(rsp["data"][region])
        return models.RoleInfo(**json_data)
