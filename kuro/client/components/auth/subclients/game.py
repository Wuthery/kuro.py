"""Game auth client."""

import typing

from kuro import constants, errors, models, types
from kuro.client import decorators, routes
from kuro.client.components import base
from kuro.utility import auth

__all__ = ["GameAuthClient"]


class GameAuthClient(base.BaseClient):
    """Game auth client."""

    @decorators.region_specific(types.Region.OVERSEAS)
    async def game_login(
        self,
        email: str,
        password: str,
        *,
        device_id: str | None = None,
        mmt_result: models.MMTResult | None = None,
    ) -> models.GameLoginResult:
        """Login with a username and password into game account.

        ### Args:
            email: Email (raw unencrypted string).
            password: Password (raw unencrypted string).
            device_id: Device ID (UUID4 uppercase). If not provided, a new UUID will be generated.
            mmt_result: MMT result from geetest.

        ### Returns:
            Login result.
        """
        data: dict[str, typing.Any] = {
            "__e__": 1,
            "email": email,
            "client_id": "7rxmydkibzzsf12om5asjnoo",  # KR_PRODUCT_KEY in kr_sdk_config.json
            "deviceNum": device_id or auth.generate_uuid_uppercase(),
            "password": auth.encode_password(password),
            "platform": "PC",
            "productId": "A1730",
            "productKey": "5c063821193f41e09f1c4fdd7567dda3",  # KR_PRODUCT_KEY in kr_sdk_config.json
            "projectId": "G153",
            "redirect_uri": 1,
            "response_type": "code",
            "sdkVersion": "2.6.0h",
            "channelId": "240",
        }
        data["sign"] = auth.encode_md5_parameter(
            data, constants.APP_KEYS[types.Game.WUWA][self.region]
        )

        if mmt_result is not None:
            data.update(mmt_result.get_game_dict())

        rsp = await self.request(routes.GAME_LOGIN.get_url(), data=data)

        if rsp["codes"] not in {0, None}:
            errors.raise_from_data(rsp)

        return models.GameLoginResult(**rsp)

    @decorators.region_specific(types.Region.OVERSEAS)
    async def get_game_token(
        self, code: str, *, device_id: str | None = None
    ) -> models.GameTokenResult:
        """Get game access token.

        ### Args:
            code: Authorization code.

        ### Returns:
            Game token result.
        """
        data: dict[str, typing.Any] = {
            "client_id": "7rxmydkibzzsf12om5asjnoo",  # KR_PRODUCT_KEY in kr_sdk_config.json
            "deviceNum": device_id or auth.generate_uuid_uppercase(),
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
    async def check_game_token(self, access_token: str, *, device_id: str | None = None) -> int:
        """Check game access token life time.

        ### Args:
            access_token: Game access token.

        ### Returns:
            Remaining life time of access token in seconds.
        """
        data = {
            "deviceNum": device_id or auth.generate_uuid_uppercase(),
            "access_token": access_token,
            "productId": "A1725",
            "projectId": "G153",
            "channelId": "171",
        }
        data["sign"] = auth.encode_md5_parameter(
            data, constants.APP_KEYS[types.Game.WUWA][self.region]
        )
        rsp = await self.request(routes.GAME_TOKEN_CHECK.get_url(), data=data)

        if rsp["codes"] not in {0, None}:
            errors.raise_from_data(rsp)

        return rsp["expireSec"]

    @decorators.region_specific(types.Region.OVERSEAS)
    async def game_auto_login(
        self, auto_token: str, *, device_id: str | None = None
    ) -> models.GameLoginResult:
        """Login with an auto token.

        ### Args:
            auto_token: Auto login token.

        ### Returns:
            Login result.
        """
        data: dict[str, typing.Any] = {
            "token": auto_token,
            "client_id": "7rxmydkibzzsf12om5asjnoo",  # KR_PRODUCT_KEY in kr_sdk_config.json
            "deviceNum": device_id or auth.generate_uuid_uppercase(),
            "sdkVersion": "2.6.0h",
            "productId": "A1730",
            "projectId": "G153",
            "redirect_uri": 1,
            "response_type": "code",
            "channelId": "171",
        }
        data["sign"] = auth.encode_md5_parameter(
            data, constants.APP_KEYS[types.Game.WUWA][self.region]
        )
        rsp = await self.request(routes.GAME_AUTO_LOGIN.get_url(), data=data)

        if rsp["codes"] not in {0, None}:
            errors.raise_from_data(rsp)

        return models.GameLoginResult(**rsp)

    @decorators.region_specific(types.Region.OVERSEAS)
    async def generate_oauth_code(self, game_token: str, *, device_id: str | None = None) -> str:
        """Generate OAuth code from game token.

        ### Args:
            game_token: Game access token.

        ### Returns:
            The generated OAuth code.
        """
        data: dict[str, int | str] = {
            "client_id": "7rxmydkibzzsf12om5asjnoo",  # KR_PRODUCT_KEY in kr_sdk_config.json
            "deviceNum": device_id or auth.generate_uuid_uppercase(),
            "client_secret": "32gh5r0p35ullmxrzzwk40ly",
            "access_token": game_token,
            "productId": "A1725",
            "projectId": "G153",
            "redirect_uri": 1,
            "scope": "launcher",
        }
        rsp = await self.request(routes.OAUTH_CODE.get_url(), data=data)

        if rsp["codes"] not in {0, None}:
            errors.raise_from_data(rsp)

        return rsp["oauthCode"]
