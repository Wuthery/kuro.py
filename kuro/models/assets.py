"""Assets-related models."""

import pydantic

__all__ = ["IconRoleHead", "IconWeapon"]


class IconRoleHead(pydantic.BaseModel):
    """Role head icon model."""

    url_150: str
    """150x150 icon URL."""

    url_175: str
    """175x175 icon URL."""

    url_256: str
    """256x256 icon URL."""


class IconWeapon(pydantic.BaseModel):
    """Weapon icon model."""

    url_80: str
    """80x80 icon URL."""

    url_160: str
    """80x80 icon URL."""

    url_256: str
    """256x256 icon URL."""
