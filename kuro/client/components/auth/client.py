"""Auth component responsible for authentication."""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuro import errors, types
from kuro.client.components.auth import subclients
from kuro.utility import geetest

if TYPE_CHECKING:
    from kuro import models

__all__ = ["AuthClient"]


class AuthClient(subclients.GameAuthClient, subclients.WebAuthClient):
    """Auth client."""

    async def demo_web_login(self, number: str, *, port: int = 5000) -> models.LoginResult:
        """Login with a phone number.

        ### Args:
            number: Chinese phone number. With or without regional prefix (`+86`).
            port: Port to use for geetest server.

        ### Returns:
            Login result.
        """
        success = await self.send_sms_code(number)
        if not success:
            mmt_result = await geetest.server.solve_geetest(
                captcha_id=types.CaptchaId.KUROBBS, lang=self.lang, port=port
            )
            await self.send_sms_code(number, mmt_result=mmt_result)

        code = input("Enter OTP code: ")  # noqa: ASYNC250
        return await self.web_login(number, code)

    async def demo_game_login(
        self, email: str, password: str, *, port: int = 5000
    ) -> models.GameLoginResult:
        """Login to game account with email and password.

        ### Args:
            email: Account email.
            password: Account password.

        ### Returns:
            Login result.
        """
        try:
            login_result = await self.game_login(email, password)
        except errors.GeetestTriggeredError:
            mmt_result = await geetest.server.solve_geetest(
                captcha_id=types.CaptchaId.GAME, lang=self.lang, port=port
            )
            login_result = await self.game_login(email, password, mmt_result=mmt_result)

        return login_result
