"""Web auth client."""

import typing

from ..... import errors, models
from .... import routes
from ... import base

__all__ = ["WebAuthClient"]


class WebAuthClient(base.BaseClient):
    """Web auth client."""

    @typing.overload
    async def _send_sms_code(self, number: str, *, mmt_result: None = ...) -> bool: ...

    @typing.overload
    async def _send_sms_code(
        self, number: str, *, mmt_result: models.MMTResult = ...
    ) -> typing.Literal[True]: ...

    async def _send_sms_code(
        self, number: str, *, mmt_result: models.MMTResult | None = None
    ) -> bool:
        """Send SMS code to phone number.

        Args:
            number (str): Chinese phone number.
            mmt_result (models.MMTResult, optional): MMT result with solved captcha.

        Returns:
            bool: Whether the SMS code is sent successfully. False means geetest was triggered.
        """
        data = {
            "mobile": number if not number.startswith("+86") else number[3:],
            "geeTestData": mmt_result.model_dump() if mmt_result else "",
        }
        rsp = await self.request(routes.GET_SMS_CODE.get_url(), data=data)

        if not rsp["success"]:
            errors.raise_from_data(rsp)

        return not rsp["data"]["geeTest"]

    async def _web_login(self, number: str, code: str) -> models.LoginResult:
        """Login with a phone number and OTP code.

        Args:
            number (str): Chinese phone number.
            code (str): OTP code.

        Returns:
            models.LoginResult: Login result.
        """
        data = {"mobile": number if not number.startswith("+86") else number[3:], "code": code}
        rsp = await self.request(routes.WEB_LOGIN.get_url(), data=data)

        if not rsp["success"]:
            errors.raise_from_data(rsp)

        return models.LoginResult(**rsp["data"])
