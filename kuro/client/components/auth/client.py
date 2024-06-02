"""Auth component responsible for authentication."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ....utility.geetest import server
from .subclients import GameAuthClient, WebAuthClient

if TYPE_CHECKING:
    from .... import models

__all__ = ["AuthClient"]


class AuthClient(GameAuthClient, WebAuthClient):
    """Auth client."""

    async def login(self, number: str, *, port: int = 5000) -> models.LoginResult:
        """Login with a phone number.

        ### Args:
            number: Chinese phone number. With or without regional prefix (`+86`).
            port: Port to use for geetest server.

        ### Returns:
            Login result.
        """
        success = await self._send_sms_code(number)
        if not success:
            mmt_result = await server.solve_geetest(lang=self.lang, port=port)
            await self._send_sms_code(number, mmt_result=mmt_result)

        code = await server.enter_code(port=port)
        return await self._web_login(number, code)
