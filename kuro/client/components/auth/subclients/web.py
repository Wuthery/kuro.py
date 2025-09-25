"""Web auth client."""

import typing

from kuro import errors, models
from kuro.client import routes
from kuro.client.components import base

__all__ = ["WebAuthClient"]


class WebAuthClient(base.BaseClient):
    """Web auth client."""

    @typing.overload
    async def send_sms_code(self, number: str, *, mmt_result: None = ...) -> bool: ...

    @typing.overload
    async def send_sms_code(
        self, number: str, *, mmt_result: models.MMTResult = ...
    ) -> typing.Literal[True]: ...

    async def send_sms_code(
        self, number: str, *, mmt_result: models.MMTResult | None = None
    ) -> bool:
        """Send SMS code to phone number.

        ### Args:
            number: Chinese phone number. With or without regional prefix (`+86`).
            mmt_result: MMT result with solved captcha.

        ### Returns:
            True if SMS code was sent successfully. False means geetest was triggered.
        """
        data = {
            "mobile": number if not number.startswith("+86") else number[3:],
            "geeTestData": mmt_result.model_dump_json() if mmt_result else "",
        }
        rsp = await self.request(routes.GET_SMS_CODE.get_url(), data=data, headers={"Source": "h5"})

        if not rsp["success"]:
            errors.raise_from_data(rsp)

        return not rsp["data"]["geeTest"]

    async def web_login(self, number: str, code: str) -> models.LoginResult:
        """Login with a phone number and OTP code.

        ### Args:
            number: Chinese phone number. With or without regional prefix (`+86`).
            code: OTP code.

        ### Returns:
            Login result.
        """
        data = {"mobile": number if not number.startswith("+86") else number[3:], "code": code}
        rsp = await self.request(routes.WEB_LOGIN.get_url(), data=data, headers={"Source": "h5"})

        if not rsp["success"]:
            errors.raise_from_data(rsp)

        return models.LoginResult(**rsp["data"])
