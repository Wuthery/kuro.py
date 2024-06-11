"""Gacha models."""

import datetime  # noqa: TCH003
import enum

import pydantic

from kuro import constants, types
from kuro.models import assets, base

__all__ = ["GachaCharacter", "GachaItemType", "GachaRecord", "GachaWeapon"]


class GachaItemType(enum.IntEnum):
    """Gacha item type."""

    RESONATOR = 1
    """Resonator."""
    WEAPON = 2
    """Weapon."""


class GachaRecord(base.APIModel):
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


class GachaCharacter(GachaRecord):
    """Gacha character model."""

    @property
    def icon(self) -> assets.IconRoleHead:
        """Character icon."""
        return assets.IconRoleHead(
            url_150=(
                f"{constants.WUTHERY_CDN}/d/GameData/IDFiedResources/"
                f"Common/Image/IconRoleHead150/{self.resource_id}.png"
            ),
            url_175=(
                f"{constants.WUTHERY_CDN}/d/GameData/IDFiedResources/"
                f"Common/Image/IconRoleHead175/{self.resource_id}.png"
            ),
            url_256=(
                f"{constants.WUTHERY_CDN}/d/GameData/IDFiedResources/"
                f"Common/Image/IconRoleHead256/{self.resource_id}.png"
            ),
        )

    @property
    def icon_circle_url(self) -> str:
        """Character circle icon."""
        return (
            f"{constants.WUTHERY_CDN}/d/GameData/IDFiedResources/"
            f"Common/Image/IconRoleHeadCircle256/{self.resource_id}.png"
        )

    @property
    def pile_icon_url(self) -> str:
        """Character pile icon."""
        return (
            f"{constants.WUTHERY_CDN}/d/GameData/IDFiedResources/"
            f"Common/Image/IconRolePile/{self.resource_id}.png"
        )


class GachaWeapon(GachaRecord):
    """Gacha weapon model."""

    @property
    def icon(self) -> assets.IconWeapon:
        """Weapon icon."""
        return assets.IconWeapon(
            url_80=(
                f"{constants.WUTHERY_CDN}/d/GameData/UIResources/"
                f"common/image/iconweapon80/t_iconweapon80{self.resource_id}_ui.png"
            ),
            url_160=(
                f"{constants.WUTHERY_CDN}/d/GameData/UIResources/"
                f"common/image/iconweapon160/t_iconweapon160{self.resource_id}_ui.png"
            ),
            url_256=(
                f"{constants.WUTHERY_CDN}/d/GameData/UIResources/"
                f"common/image/iconweapon/t_iconweapon{self.resource_id}_ui.png"
            ),
        )
