"""Gacha models."""

import datetime
import enum

import pydantic

from .. import types
from .base import APIModel

__all__ = ["GachaItemType", "GachaRecord"]


class GachaItemType(enum.IntEnum):
    """Gacha item type."""

    RESONATOR = 1
    """Resonator."""
    WEAPON = 2
    """Weapon."""


class GachaRecord(APIModel):
    """Gacha record model."""

    banner: types.WuWaBanner = pydantic.Field(alias="cardPoolType")
    """Banner type."""
    resource_id: int
    """Item ID."""
    rarity: int = pydantic.Field(alias="qualityLevel")
    """Item rarity."""
    type_name: str = pydantic.Field(alias="resourceType")
    """Localized item type name."""
    name: str
    """Name of the record item."""
    count: int
    """Count of the record item."""
    time: datetime.datetime
    """Time of the record."""

    @property
    def type(self) -> GachaItemType:
        """Item type."""
        return GachaItemType.WEAPON if self.resource_id >= 100000 else GachaItemType.RESONATOR
