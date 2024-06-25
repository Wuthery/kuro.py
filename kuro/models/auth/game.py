"""Game auth models."""

import pydantic

from kuro.models import base

__all__ = ["GameLoginResult", "GameTokenResult"]


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
