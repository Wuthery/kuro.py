"""Auth-related models."""

import pydantic

from kuro.models import base

__all__ = ["GameLoginResult", "GameTokenResult", "LoginResult", "MMTResult"]


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


class GameLoginResult(base.APIModel):
    """Game login result."""

    username: str
    """Username."""
    sdk_user_id: str = pydantic.Field(alias="sdkuserid")
    """SDK user ID."""
    id: int
    """User ID."""
    login_type: int
    """Login type."""
    code: str
    """Code."""
    temp_token: str
    """Temporary token."""
    id_stat: int
    """ID status (?)."""
    user_type: int
    """User type."""
    cuid: str
    """CUID. Usually same as id but in string format."""
    show_paw: bool
    """Whether to show password (?)."""
    bind_dev_stat: bool
    """Bind device status."""
    bind_dev_switch: bool
    """Bind device switch."""
    auto_token: str
    """Auto token used to login automatically."""
    first_login: bool = pydantic.Field(alias="firstLgn")
    """Whether this is the first login."""
    email: str
    """Email."""
    bind: bool
    """Whether the account is bound (?)."""


class GameTokenResult(base.APIModel):
    """Game token result."""

    access_token: str
    """Access token."""
    expires_in: int
    """Expiration time."""
