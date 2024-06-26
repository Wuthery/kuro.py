"""Constants for the lib."""

import typing

from kuro import types

__all__ = ["GEETEST_LANGS"]


GEETEST_LANGS: typing.Mapping[types.Lang, str] = {
    types.Lang.CHINESE_SIMPLIFIED: "zh-Hans",
    types.Lang.CHINESE_TRADITIONAL: "zh-Hant",
    types.Lang.ENGLISH: "en",
    types.Lang.JAPANESE: "ja",
    types.Lang.KOREAN: "ko",
    types.Lang.FRENCH: "fr",
    types.Lang.GERMAN: "de",
    types.Lang.SPANISH: "es",
}
"""Geetest languages."""

WUTHERY_CDN: str = "https://files.wuthery.com"
"""Wuthery CDN URL."""

APP_KEYS: typing.Mapping[types.Game, typing.Mapping[types.Region, str]] = {
    types.Game.WUWA: {
        types.Region.CHINESE: "",
        types.Region.OVERSEAS: "32gh5r0p35ullmxrzzwk40ly",
    }
}
"""App keys for game login."""
