"""Game models."""

import datetime
import typing

import pydantic

from kuro.models import base


class GameAccount(base.APIModel):
    """User game account."""

    region: str = pydantic.Field(alias="Region")
    """Account region."""
    level: int = pydantic.Field(alias="Level")
    """Account level."""
    last_time_online: datetime.datetime = pydantic.Field(alias="LastTimeOnline")
    """Last time the user was online."""


class GameUser(base.APIModel):
    """Game user."""

    id: int = pydantic.Field(alias="UserId")
    """User ID."""
    sdk_login_code: int = pydantic.Field(alias="SdkLoginCode")
    """SDK login code."""
    accounts: typing.Sequence[GameAccount] = pydantic.Field(alias="UserInfos")
    """List of user game accounts."""
    recommended_region: str = pydantic.Field(alias="RecommendRegion")
    """Recommended region."""
