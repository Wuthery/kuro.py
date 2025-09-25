"""Web auth models."""

import pydantic

from kuro.models import base

__all__ = ["LoginResult", "MMTResult"]


class LoginResult(base.APIModel):
    """Login result returned by `client.login`."""

    enable_child_mode: bool
    """Whether child mode is enabled."""
    gender: int
    """User gender."""
    signature: str
    """Signature."""
    avatar_url: str = pydantic.Field(alias="headUrl")
    """PNG avatar URL."""
    avatar_code: str = pydantic.Field(alias="headCode")
    """Avatar code."""
    user_name: str
    """User name."""
    user_id: str
    """User ID."""
    is_registered: int = pydantic.Field(alias="isRegister")
    """Whether the user is registered."""
    is_official: int
    """Whether the account is official."""
    status: int
    """User status."""
    token: str
    """Cookie token used to access API."""


class MMTResult(pydantic.BaseModel):
    """MMT result model."""

    captcha_id: str
    """CAPTCHA ID."""
    lot_number: str
    """Serial number."""
    pass_token: str
    """Token of successful verification."""
    gen_time: str
    """Timestamp."""
    captcha_output: str
    """Verification output data."""

    def get_game_dict(self) -> dict[str, str]:
        """Get dictionary for game geetest verification."""
        return {
            "geetestCaptchaOutput": self.captcha_output,
            "geetestGenTime": self.gen_time,
            "geetestLotNumber": self.lot_number,
            "geetestPassToken": self.pass_token,
        }
