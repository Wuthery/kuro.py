"""Auth component responsible for authentication."""

from .subclients import GameAuthClient, WebAuthClient
from ....utility.geetest import server
from .... import models

__all__ = ["AuthClient"]


class AuthClient(GameAuthClient, WebAuthClient):
    """Auth client."""

    async def login(self, number: str, *, port: int = 5000) -> models.LoginResult:
        """Login with a phone number."""
        success = await self._send_sms_code(number)
        if not success:
            mmt_result = await server.solve_geetest(lang=self.lang, port=port)
            await self._send_sms_code(number, mmt_result=mmt_result)

        code = await server.enter_code(port=port)
        return await self._web_login(number, code)
