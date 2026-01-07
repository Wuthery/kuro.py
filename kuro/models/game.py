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
    last_time_online: datetime.datetime = pydantic.Field(alias="LastOnlineTime")
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


class GamePlayerInfo(base.APIModel):
    """Game player info."""

    uid: int = pydantic.Field(alias="roleId")
    """User ID."""
    name: str = pydantic.Field(alias="roleName")
    """Player name."""
    level: int
    """Player level."""
    sex: int
    """Player sex."""
    avatar_id: int = pydantic.Field(alias="headPhoto")
    """Player avatar Id.

    See this file for more info: https://files.wuthery.com/GameData/ConfigDBParsed/PlayerHeadRe.json
    """


class BasicRoleInfo(base.APIModel):
    """Basic role info."""

    name: str = pydantic.Field(alias="Name")
    """Player name."""
    id: int = pydantic.Field(alias="Id")
    """Player ID."""
    create_time: datetime.datetime = pydantic.Field(alias="CreatTime")
    """Account creation time."""
    active_days: int = pydantic.Field(alias="ActiveDays")
    """Number of active days."""
    level: int = pydantic.Field(alias="Level")
    """Player level."""
    world_level: int = pydantic.Field(alias="WorldLevel")
    """World level."""
    character_count: int = pydantic.Field(alias="RoleNum")
    """Number of characters."""
    sonance_cascet_count: int = pydantic.Field(alias="SoundBox")
    """Number of sonance caskets."""
    waveplates: int = pydantic.Field(alias="Energy")
    """Current waveplates count."""
    max_waveplates: int = pydantic.Field(alias="MaxEnergy")
    """Maximum waveplates count."""
    refined_waveplates: int = pydantic.Field(alias="StoreEnergy")
    """Refined waveplates count."""
    max_refined_waveplates: int = pydantic.Field(alias="MaxStoreEnergy")
    """Maximum refined waveplates count."""
    refined_waveplates_replenish_time: datetime.datetime = pydantic.Field(
        alias="StoreEnergyRecoverTime"
    )
    """Refined waveplates replenish time."""
    waveplates_replenish_time: datetime.datetime = pydantic.Field(alias="EnergyRecoverTime")
    """Waveplates replenish time."""
    activity_points: int = pydantic.Field(alias="Liveness")
    """Current activity points."""
    max_activity_points: int = pydantic.Field(alias="LivenessMaxCount")
    """Maximum activity points."""
    activities_unlocked: bool = pydantic.Field(alias="LivenessUnlock")
    """Whether activities are unlocked."""
    chapter_id: int = pydantic.Field(alias="ChapterId")
    """Current chapter ID."""
    weekly_challenge: int = pydantic.Field(alias="WeeklyInstCount")
    """Weekly challenge count left."""
    chests: dict[str, int] = pydantic.Field(alias="Boxes")
    """Chests collected by the player. Key is a chest type (rarity)."""
    basic_chests: dict[str, int] = pydantic.Field(alias="BasicBoxes")
    """Basic chests collected."""
    tidal_heritages: dict[str, int] = pydantic.Field(alias="PhantomBoxes")
    """Tidal heritages collected. Key is a heritage type (rarity)."""
    birthday_month: int = pydantic.Field(alias="BirthMon")
    """Birthday month."""
    birthday_day: int = pydantic.Field(alias="BirthDay")
    """Birthday day."""


class BattlePassRoleInfo(base.APIModel):
    """Battle pass role info."""

    level: int = pydantic.Field(alias="Level")
    """Battle pass level."""
    weekly_xp: int = pydantic.Field(alias="WeekExp")
    """Weekly experience."""
    max_weekly_xp: int = pydantic.Field(alias="WeekMaxExp")
    """Maximum weekly experience."""
    is_unlocked: bool = pydantic.Field(alias="IsUnlock")
    """Whether the battle pass is unlocked."""
    is_opened: bool = pydantic.Field(alias="IsOpen")
    """Whether the battle pass is opened."""
    xp: int = pydantic.Field(alias="Exp")
    """Experience."""
    xp_limit: int = pydantic.Field(alias="ExpLimit")
    """Experience limit."""


class SkinInfo(base.APIModel):
    """Skin info."""

    id: int = pydantic.Field(alias="SkinId")
    """Skin ID."""
    quality: int = pydantic.Field(alias="Quality")
    """Skin quality."""


class BikeInfo(base.APIModel):
    """Bike info.

    For accounts that don't have bike unlocked, all int fields will be 0.
    """

    level: int = pydantic.Field(alias="Level")
    """Bike level."""
    xp: int = pydantic.Field(alias="Exp")
    """Bike experience."""
    next_xp: int = pydantic.Field(alias="NextExp")
    """Bike experience needed for next level."""
    skins: list[SkinInfo] = pydantic.Field(alias="Skins")
    """List of bike skins."""
    equipped_skin: SkinInfo = pydantic.Field(alias="EquipSkin")
    """Equipped bike skin."""


class MusicAlbum(base.APIModel):
    """Music album."""

    id: int = pydantic.Field(alias="Id")
    """Album ID."""
    count: int = pydantic.Field(alias="Count")
    """Number of songs collected in the album."""
    total_count: int = pydantic.Field(alias="TotalCount")
    """Total number of songs in the album."""


class MusicInfo(base.APIModel):
    """Music info."""

    albums: list[MusicAlbum] = pydantic.Field(alias="Albums")
    """List of music albums."""


class RoleInfo(base.APIModel):
    """Game role info."""

    basic: BasicRoleInfo = pydantic.Field(alias="Base")
    """Basic player info."""
    bike: BikeInfo = pydantic.Field(alias="MotorData")
    """Bike info."""
    music: MusicInfo = pydantic.Field(alias="MusicData")
    """Music info."""
    battle_pass: BattlePassRoleInfo = pydantic.Field(alias="BattlePass")
    """Battle pass info."""
