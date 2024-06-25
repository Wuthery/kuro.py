"""Game component for fetching game data."""

from kuro import errors, models
from kuro.client import routes
from kuro.client.components import base


class GameClient(base.BaseClient):
    """Game client."""

    async def get_game_user(
        self,
        user_id: int,
        token: str,
        area: str,
        username: str,
        *,
        login_type: int = 1
    ) -> models.GameUser:
        """Get game user info.

        ### Returns:
            Game info.
        """
        params = {
            "loginType": login_type,
            "userId": user_id,
            "token": token,
            "area": area,
            "userName": username
        }
        rsp = await self.request(routes.GAME_USER_INFO.get_url().with_query(params))

        if rsp["Code"] != 0:
            errors.raise_from_data(rsp)

        return models.GameUser(**rsp)
