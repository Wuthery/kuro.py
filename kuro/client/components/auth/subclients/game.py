"""Game auth client."""

from kuro import constants, errors, models, types
from kuro.client import decorators, routes
from kuro.client.components import base
from kuro.utility import auth

__all__ = ["GameAuthClient"]


class GameAuthClient(base.BaseClient):
    """Game auth client."""

    @decorators.region_specific(types.Region.OVERSEAS)
    async def game_login(self, email: str, password: str) -> models.GameLoginResult:
        """Login with a username and password into game account.

        ### Args:
            email: Email (raw unencrypted string).
            password: Password (raw unencrypted string).

        ### Returns:
            Login result.
        """
        data = {
            "__e__": 1,
            "email": email,
            "client_id": "7rxmydkibzzsf12om5asjnoo",  # KR_PRODUCT_KEY in kr_sdk_config.json
            "deviceNum": "A227C7BA-CB16-4E62-8355-BEABE3DE10F8",  # Can be any random string
            "os": "iOS",
            "password": auth.encode_password(password),
            "platform": "iOS",
            "productId": "A1725",
            "productKey": "01433708256c41838cda8ead20b64042",  # KR_PRODUCT_KEY in kr_sdk_config.json
            "projectId": "G153",
            "redirect_uri": 1,
            "response_type": "code",
            "sdkVersion": "1.8.3h",
        }
        data["sign"] = auth.encode_md5_parameter(
            data, constants.APP_KEYS[types.Game.WUWA][self.region]
        )
        rsp = await self.request(routes.GAME_LOGIN.get_url(), data=data)

        if rsp["codes"] not in {0, None}:
            errors.raise_from_data(rsp)

        return models.GameLoginResult(**rsp)

    @decorators.region_specific(types.Region.OVERSEAS)
    async def get_game_token(self, code: str) -> models.GameTokenResult:
        """Get game access token.

        ### Args:
            code: Authorization code.

        ### Returns:
            Game token result.
        """
        data = {
            "client_id": "7rxmydkibzzsf12om5asjnoo",  # KR_PRODUCT_KEY in kr_sdk_config.json
            "deviceNum": "A227C7BA-CB16-4E62-8355-BEABE3DE10F8",
            "client_secret": "32gh5r0p35ullmxrzzwk40ly",
            "code": code,
            "productId": "A1725",
            "projectId": "G153",
            "redirect_uri": 1,
            "grant_type": "authorization_code",
        }
        data["sign"] = auth.encode_md5_parameter(
            data, constants.APP_KEYS[types.Game.WUWA][self.region]
        )
        rsp = await self.request(routes.GAME_TOKEN.get_url(), data=data)

        if rsp["codes"] not in {0, None}:
            errors.raise_from_data(rsp)

        return models.GameTokenResult(**rsp)

    @decorators.region_specific(types.Region.OVERSEAS)
    async def check_game_token(self, access_token: str) -> int:
        """Check game access token life time.

        ### Args:
            access_token: Game access token.

        ### Returns:
            Remaining life time of access token in seconds.
        """
        data = {
            "deviceNum": "A227C7BA-CB16-4E62-8355-BEABE3DE10F8",
            "access_token": access_token,
            "productId": "A1725",
            "projectId": "G153",
        }
        data["sign"] = auth.encode_md5_parameter(
            data, constants.APP_KEYS[types.Game.WUWA][self.region]
        )
        rsp = await self.request(routes.GAME_TOKEN_CHECK.get_url(), data=data)

        if rsp["codes"] not in {0, None}:
            errors.raise_from_data(rsp)

        return rsp["expireSec"]

    @decorators.region_specific(types.Region.OVERSEAS)
    async def game_auto_login(self, auto_token: str) -> models.GameLoginResult:
        """Login with an auto token.

        ### Args:
            auto_token: Auto login token.

        ### Returns:
            Login result.
        """
        data = {
            "token": auto_token,
            "client_id": "7rxmydkibzzsf12om5asjnoo",  # KR_PRODUCT_KEY in kr_sdk_config.json
            "deviceNum": "A227C7BA-CB16-4E62-8355-BEABE3DE10F8",
            "productId": "A1725",
            "projectId": "G153",
            "redirect_uri": 1,
            "response_type": "code",
        }
        data["sign"] = auth.encode_md5_parameter(
            data, constants.APP_KEYS[types.Game.WUWA][self.region]
        )
        rsp = await self.request(routes.GAME_AUTO_LOGIN.get_url(), data=data)

        if rsp["codes"] not in {0, None}:
            errors.raise_from_data(rsp)

        return models.GameLoginResult(**rsp)
